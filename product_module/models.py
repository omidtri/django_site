from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from account_module.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class ProductProperty(models.Model):
    title = models.CharField(max_length=350, verbose_name='ویژگی محصول')

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی محصولات'

    def __str__(self):
        return self.title


class DetailsProduct(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    size = models.CharField(max_length=150, null=True, blank=True, verbose_name='سایز')
    meterage = models.CharField(max_length=250, null=True, blank=True, verbose_name='متراژ')
    code_product = models.CharField(max_length=150, null=True, blank=True, verbose_name='کد محصول')
    colors = models.CharField(max_length=350, null=True, blank=True, verbose_name='رنگ محصول')
    package_type = models.CharField(max_length=150, null=True, blank=True, verbose_name='نوع بسته بندی')
    Hose_texture = models.CharField(max_length=350, null=True, blank=True, verbose_name='بافت درون شیلنگ')
    number_of_layers = models.CharField(max_length=250, null=True, blank=True, verbose_name='تعداد لایه ها')
    sex_product = models.CharField(max_length=250, null=True, blank=True, verbose_name='جنس محصول')
    country = models.CharField(max_length=250, null=True, blank=True, verbose_name='کشور تولید کننده')
    brand_product = models.CharField(max_length=250, null=True, blank=True, verbose_name='برند محصول')
    thermal_tolerance = models.CharField(max_length=250, null=True, blank=True, verbose_name='تحمل حرارتی')
    burst_border = models.CharField(max_length=250, null=True, blank=True, verbose_name='حداکثر فشار ترکیدگی')
    pressure_tolerance = models.CharField(max_length=250, null=True, blank=True, verbose_name='تحمل فشار کاری')
    print_product = models.CharField(max_length=250, null=True, blank=True, verbose_name='چاپ محصول')
    guarantee_product = models.CharField(max_length=250, null=True, blank=True, verbose_name='ضمانت و گارانتی محصول')
    category_product = models.CharField(max_length=250, null=True, blank=True, verbose_name='دسته بندی محصول')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'جزییات محصولات'


class Products(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول', db_index=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات اصلی',null=True,blank=True,db_index=True)
    # description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    keyword = models.CharField(verbose_name='کلمه کلیدی', blank=True, null=True, max_length=400, db_index=True)
    discount_price = models.IntegerField(verbose_name='تخفیف',null=True,blank=True)
    is_discount = models.BooleanField(verbose_name='تخفیف فعال',null=True,blank=True)

    property = models.ManyToManyField(ProductProperty, null=True, blank=True, verbose_name='ویژگی ها')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی ها')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    details = models.ForeignKey(DetailsProduct, on_delete=models.CASCADE, verbose_name='جزییات محصول', null=True,
                                blank=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    message = models.TextField(verbose_name='متن نظر')
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)
    parent = models.ForeignKey('ProductComment', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'
