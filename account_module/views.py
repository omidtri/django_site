from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, Http404
from django.utils.crypto import get_random_string
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout

from utils.email_service import send_email
from . import forms, models


class RegisterView(View):
    def get(self, request: HttpRequest):
        form = forms.RegisterForm()
        context = {'form': form}
        return render(request, 'account_module/register_view.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')
            user: bool = models.User.objects.filter(email__iexact=user_email).first()
            if user:
                form.add_error(field='email', error='ایمیل وارد شده تکراری می باشد')
            else:
                new_user = models.User(
                    email=user_email,
                    active_email_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')

                return redirect(reverse('login_page'))

        context = {
            'register_form': form
        }

        return render(request, 'account_module/register_view.html', context=context)


class LoginView(View):
    def get(self, request: HttpRequest):
        form = forms.LoginForm()
        context = {'form': form}
        return render(request, 'account_module/login_view.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')
            user: models.User = models.User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    form.add_error('email', error='حساب کاربری فعال نمی باشد')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('user_panel_dashboard'))
                    else:
                        form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
            else:
                form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
        context = {'form': form}
        return render(request, 'account_module/login_view.html', context=context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse('home_page'))


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        form = forms.ForgotPasswordForm()
        context = {'form': form}
        return render(request, 'account_module/forget_password_view.html', context=context)

    def post(self, request: HttpRequest):
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            email_user = form.cleaned_data.get('email')
            user: models.User = models.User.objects.filter(email__iexact=email_user).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('home_page'))

        context = {'form': form}
        return render(request, 'account_module/forget_password_view.html', context=context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: models.User = models.User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = forms.ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = forms.ResetPasswordForm(request.POST)
        user: models.User = models.User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: models.User = models.User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show success message to user
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated message to user
                pass

        raise Http404


def email_news(request: HttpRequest):
    email = request.GET.get('email')
    if email is not None:
        all_email_current = models.Newsletters.objects.filter(email__iexact=email).first()
        if all_email_current:
            context = {'text': 'مشکلی در فرآیند پیش آمده است'}
            return render(request, 'account_module/includes/news_page.html', context)
        news_email = models.Newsletters(email=email)
        news_email.save()
        context = {'text': 'ایمیل شما ثبت شد'}
        return render(request, 'account_module/includes/news_page.html', context)
    else:
        context = {'text': 'مشکلی در فرآیند پیش آمده است'}
        return render(request, 'account_module/includes/news_page.html', context)
