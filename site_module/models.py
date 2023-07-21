from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')
    image = models.ImageField(upload_to='images/site-setting/', verbose_name='تصویر Enamad', blank=True,
                              null=True)

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='images/sliders', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات',
        product_detail = 'product_detail', 'صفحه ی جزییات محصولات',
        about_us = 'about_us', 'درباره ما'

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'


class StandardImageSite(models.Model):
    title = models.CharField(max_length=200, verbose_name='نام استاندارد')
    image = models.ImageField(upload_to='images/standard', verbose_name='تصویر استاندارد')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'استاندارد'
        verbose_name_plural = 'استاندارد ها'

    def __str__(self):
        return self.title


class AgentModel(models.Model):
    name = models.CharField(verbose_name='نام و نام خانوادگی نماینده', null=True, blank=True, max_length=250)
    city_country = models.CharField(verbose_name='شهر یا کشور نماینده', null=True, blank=True, max_length=250)
    shopping_name = models.CharField(verbose_name='نام فروشگاه', null=True, blank=True, max_length=250)
    address = models.CharField(verbose_name='آدرس', blank=True, null=True, max_length=500)
    is_internal = models.BooleanField(verbose_name='نماینده داخلی')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.city_country

    class Meta:
        verbose_name = 'نماینده'
        verbose_name_plural = 'نماینده ها'


class AboutUsModel(models.Model):
    body_text = models.TextField(verbose_name='متن اصلی صفحه درباره ما', null=True, blank=True)
    text_service = models.TextField(verbose_name='متن اصلی صفحه خدمات پس از فروش', null=True, blank=True)
    services = models.ManyToManyField(AgentModel, verbose_name='نماینده ها', null=True,
                                      blank=True)
    is_main = models.BooleanField(verbose_name='تنضیمات فعال')

    def __str__(self):
        return self.body_text

    class Meta:
        verbose_name = 'تنظیمات درباره ما '
        verbose_name_plural = 'تنظیمات صفحه درباره ما'


class HomeModel(models.Model):
    image_category = models.ImageField(upload_to='images/sliders', verbose_name='تصویر دسته بندی خانه')
    image_bottom = models.ImageField(upload_to='images/sliders', verbose_name='تصویر پایین صفحه خانه')
    is_main = models.BooleanField(verbose_name='فعال/غیرفعال')
    class Meta:
        verbose_name = 'تنظیمات خانه '
        verbose_name_plural = 'تنظیمات صفحه خانه'