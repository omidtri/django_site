from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView
from product_module import models
from site_module.models import Slider, SiteSetting, FooterLinkBox, StandardImageSite, AgentModel, HomeModel, \
    AboutUsModel
from utils import convertors
from account_module.models import User
from article_module.models import Article


class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_product: models.Products = models.Products.objects.filter(is_active=True, is_delete=False).order_by('-id')[
                                        :12]
        context['last_product'] = last_product
        # ----------------------------------
        slider = Slider.objects.filter(is_active=True)
        context['sliders'] = slider
        # ----------------------------------
        most_visit_products = models.Products.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:6]
        context['most_visit'] = most_visit_products
        # ----------------------------------
        standart_image: StandardImageSite = StandardImageSite.objects.filter(is_active=True).order_by('-id')[
                                            :3]
        context['standards'] = standart_image
        context['img_category'] = HomeModel.objects.filter(is_main=True).first()
        context['category'] = models.ProductCategory.objects.filter(is_active=True, is_delete=False)
        context['about_us'] = SiteSetting.objects.filter(is_main_setting=True).first()
        context['articles'] = Article.objects.filter(is_active=True).order_by('-id')[:6]
        return context


def site_header_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    category = models.ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'site_setting': site_setting,
        'categorys': category
    }
    return render(request, 'shared/site_header_partial.html', context=context)


def site_footer_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer: FooterLinkBox = FooterLinkBox.objects.all()
    context = {
        'site_setting': site_setting,
        'footer_link_boxes': footer
    }
    return render(request, 'shared/site_footer_partial.html', context=context)


class AboutUsView(TemplateView):
    template_name = 'home_module/about_us_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context['site_setting'] = SiteSetting.objects.filter(is_main_setting=True).first()
        context['admin_user'] = User.objects.filter(is_staff=True)
        context['aboutus'] = AboutUsModel.objects.filter(is_main=True).first()
        context['img'] = HomeModel.objects.filter(is_main=True).first()
        return context


def ServiceView(request: HttpRequest):
    if request.method == 'GET':
        text_servie = AboutUsModel.objects.filter(is_main=True).first()
        context = {'text': text_servie}
        return render(request, 'home_module/sevice_page.html', context=context)


def AgentView(request: HttpRequest):
    if request.method == 'GET':
        agent_internal = AgentModel.objects.filter(is_internal=True)
        agent_national = AgentModel.objects.filter(is_internal=False)

        context = {
            'a_inter': agent_internal,
            'a_national': agent_national
        }

        return render(request, 'home_module/agent_page.html', context=context)
