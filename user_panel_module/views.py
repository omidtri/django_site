from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, ListView
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth import logout
from account_module import models
from django.utils.decorators import method_decorator
from . import forms
from order_module.models import Order, OrderDetail

@method_decorator(login_required, name='dispatch')
class UserPanelDashboardView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard.html'

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        form = forms.ChangePasswordForm()
        context = {'form': form}
        return render(request, 'user_panel_module/change_password_page.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: models.User = models.User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('home_page'))
            else:
                form.add_error('new_password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': form
        }

        return render(request, 'user_panel_module/change_password_page.html', context)

@method_decorator(login_required, name='dispatch')
class EditUserProfileView(View):
    def get(self, request: HttpRequest):
        current_user = models.User.objects.filter(id=request.user.id).first()
        form = forms.EditProfileForm(instance=current_user)
        context = {'form': form, 'current_user': current_user}
        return render(request, 'user_panel_module/edit_profile_page.html', context=context)

    def post(self, request: HttpRequest):
        current_user = models.User.objects.filter(id=request.user.id).first()
        form = forms.EditProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
        context = {
            'form': form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context=context)


@login_required
def user_panel_menu_partial(request: HttpRequest):
    return render(request, 'user_panel_module/partial/user_panel_partial.html')


@method_decorator(login_required, name='dispatch')
class MyShopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)
        return queryset


@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })

@login_required
def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'user_panel_module/user_shopping_detail.html', {
        'order': order
    })

@method_decorator(login_required, name='dispatch')
class WarrantyView(View):
    def get(self, request: HttpRequest):
        form = forms.WarrantyForm()
        warranty = models.Warranty.objects.filter(user__warranty__exact=request.user.id)
        context = {'form': form, 'warranty': warranty}
        return render(request, 'user_panel_module/warranty_page.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.WarrantyForm(request.POST)
        if form.is_valid():
            warranty = models.Warranty.objects.filter(
                code_validity__iexact=form.cleaned_data.get('code_validity')).first()
            current_user: models.User = models.User.objects.filter(id=request.user.id).first()
            if warranty is not None:
                warranty.user = current_user
                warranty.detail = form.cleaned_data.get('detail')
                warranty.save()
                return redirect('user_panel_dashboard')
            else:
                form.add_error('code_validity', 'لطفا کد درست را وارد کنید')
        else:
            context = {'form': form}
            return render(request, 'user_panel_module/warranty_page.html', context=context)

@method_decorator(login_required, name='dispatch')
class DiscountView(View):
    def get(self, request: HttpRequest):
        form = forms.DiscountForm()
        discount = models.DiscountCode.objects.filter(user__discountcode__exact=request.user.id)
        context = {'form': form, 'discount': discount}
        return render(request, 'user_panel_module/discount_page.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.DiscountForm(request.POST)

        if form.is_valid():
            discount = models.DiscountCode.objects.filter(
                code_discount__iexact=form.cleaned_data.get('code_discount')).first()
            current_user: models.User = models.User.objects.filter(id=request.user.id).first()
            if discount is not None:
                discount.user = current_user
                discount.detail = form.cleaned_data.get('detail')
                discount.save()
                return redirect('user_panel_dashboard')
            else:
                print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                form.add_error('code_discount', 'لطفا کد درست را وارد کنید')
                context = {'form': form}
                return render(request, 'user_panel_module/discount_page.html', context=context)
        else:
            print('wwwwwwwwwwwwww')
            context = {'form': form}
            return render(request, 'user_panel_module/discount_page.html', context=context)
