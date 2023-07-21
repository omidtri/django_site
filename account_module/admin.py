from django.contrib import admin
from . import models


class NewsEmailAdmin(admin.ModelAdmin):
    list_display = ['email']


admin.site.register(models.User)
admin.site.register(models.Newsletters, NewsEmailAdmin)
admin.site.register(models.Warranty)
admin.site.register(models.DiscountCode)
