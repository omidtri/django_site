from django.contrib import admin
from . import models


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_active']
    list_editable = ['url', 'is_active']


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'position']


admin.site.register(models.SiteSetting)
admin.site.register(models.FooterLinkBox)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.SiteBanner, SiteBannerAdmin)
admin.site.register(models.StandardImageSite)
admin.site.register(models.AgentModel)
admin.site.register(models.AboutUsModel)
admin.site.register(models.HomeModel)
