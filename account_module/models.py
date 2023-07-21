from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='عکس آواتار', null=True, blank=True)
    active_email_code = models.CharField(max_length=100, verbose_name='کد فعال ساز ایمیل')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.email


class Newsletters(models.Model):
    email = models.CharField(max_length=250, unique=True, verbose_name='ایمیل')

    class Meta:
        verbose_name = 'ایمیل'
        verbose_name_plural = 'ایمیل های خبر نامه'

    def __str__(self):
        return self.email


class Warranty(models.Model):
    code_validity = models.CharField(max_length=200, verbose_name='کد گارانتی', unique=True)
    product_name = models.CharField(max_length=350, verbose_name='اسم محصول')
    detail = models.CharField(max_length=400, verbose_name='اطلاعات بیشتر', null=True, blank=True)
    validity_date = models.CharField(max_length=250, verbose_name='مدت اعتبار گارانتی', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)

    class Meta:
        verbose_name = 'گارانتی'
        verbose_name_plural = 'کد های گارانتی'

    def __str__(self):
        return self.code_validity


class DiscountCode(models.Model):
    code_discount = models.CharField(max_length=200, verbose_name='کد تخفیف', unique=True)
    product_name = models.CharField(max_length=350, verbose_name='اسم محصول', null=True, blank=True)
    detail = models.CharField(max_length=400, verbose_name='اطلاعات بیشتر', null=True, blank=True)
    validity_date = models.CharField(max_length=250, verbose_name='مدت اعتبار تخفیف', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)
    diccount_price = models.CharField(max_length=500,verbose_name='قیمت کد تخفیف')

    class Meta:
        verbose_name = 'تخیفات'
        verbose_name_plural = 'کد های تخفیفات'

    def __str__(self):
        return self.code_discount
