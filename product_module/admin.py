from django.contrib import admin
from . import models


class ProductModelAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    list_filter = ['is_active', 'is_delete']
    list_display = ['title', 'price', 'is_active', 'slug']
    list_editable = ['price', 'is_active']


admin.site.register(models.Products,ProductModelAdmin)
admin.site.register(models.DetailsProduct)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductProperty)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductComment)
