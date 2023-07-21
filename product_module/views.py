from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpRequest, HttpResponse
from site_module.models import SiteBanner
from utils import http_service, convertors

from . import models


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = models.Products
    paginate_by = 9
    context_object_name = 'products'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        query = models.Products.objects.all()
        product: models.Products = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetailView(DetailView):
    model = models.Products
    template_name = 'product_module/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        # favorite_product_id = request.session.get("product_favorites")
        # context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        galleries = list(models.ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = convertors.group_list(galleries, 3)
        context['related_products'] = convertors.group_list(list(
            models.Products.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]),
            3)

        # -----------------
        context['comments'] = models.ProductComment.objects.filter(product_id=loaded_product.id, parent=None,
                                                                   is_read_by_admin=True).order_by(
            '-create_date').prefetch_related('productcomment_set')
        context['comments_count'] = models.ProductComment.objects.filter(product_id=loaded_product.id,
                                                                         is_read_by_admin=True).count()
        # ----------------------
        user_ip = http_service.get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = models.ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = models.ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


def product_categories_partial(request: HttpRequest):
    print('fuck you')
    product_categories = models.ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/partial_view/product_category_partial.html', context)


def product_brands_partial(request: HttpRequest):
    product_brands = models.ProductBrand.objects.annotate(products_count=Count('products')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/partial_view/product_brands_partial.html', context)


def add_product_comment(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        product_comment = request.GET.get('product_comment')
        parent_id = request.GET.get('parent_id')
        # print(article_id, article_comment, parent_id)
        new_comment = models.ProductComment(product_id=product_id, message=product_comment, user_id=request.user.id,
                                            parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': models.ProductComment.objects.filter(product_id=product_id, parent=None,
                                                             is_read_by_admin=True).order_by(
                '-create_date').prefetch_related('productcomment_set'),
            'comments_count': models.ProductComment.objects.filter(product_id=product_id, is_read_by_admin=True).count()
        }

        return render(request, 'includes/product_comment_partial.html', context)

    return HttpResponse('response')


def searcher(request):
    search = request.GET.get('search')
    # models.Products.
    products: models.Products = models.Products.objects.filter(
        Q(title__icontains=search) | Q(slug__icontains=search) | Q(short_description__icontains=search) | Q(
            keyword__icontains=search))
    context = {
        'products': products
    }

    return render(request, 'product_module/search_page.html', context=context)
