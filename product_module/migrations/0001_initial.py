# Generated by Django 4.0.6 on 2022-07-14 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailsProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=150, null=True, verbose_name='سایز')),
                ('meterage', models.CharField(blank=True, max_length=250, null=True, verbose_name='متراژ')),
                ('code_product', models.CharField(blank=True, max_length=150, null=True, verbose_name='کد محصول')),
                ('colors', models.CharField(blank=True, max_length=350, null=True, verbose_name='رنگ محصول')),
                ('package_type', models.CharField(blank=True, max_length=150, null=True, verbose_name='نوع بسته بندی')),
                ('Hose_texture', models.CharField(blank=True, max_length=350, null=True, verbose_name='بافت درون شیلنگ')),
                ('number_of_layers', models.CharField(blank=True, max_length=250, null=True, verbose_name='تعداد لایه ها')),
                ('sex_product', models.CharField(blank=True, max_length=250, null=True, verbose_name='جنس محصول')),
                ('country', models.CharField(blank=True, max_length=250, null=True, verbose_name='کشور تولید کننده')),
                ('brand_product', models.CharField(blank=True, max_length=250, null=True, verbose_name='برند محصول')),
                ('thermal_tolerance', models.CharField(blank=True, max_length=250, null=True, verbose_name='تحمل حرارتی')),
                ('burst_border', models.CharField(blank=True, max_length=250, null=True, verbose_name='حداکثر فشار ترکیدگی')),
                ('pressure_tolerance', models.CharField(blank=True, max_length=250, null=True, verbose_name='تحمل فشار کاری')),
                ('print_product', models.CharField(blank=True, max_length=250, null=True, verbose_name='چاپ محصول')),
                ('guarantee_product', models.CharField(blank=True, max_length=250, null=True, verbose_name='ضمانت و گارانتی محصول')),
                ('category_product', models.CharField(blank=True, max_length=250, null=True, verbose_name='دسته بندی محصول')),
            ],
            options={
                'verbose_name': 'جزییات محصول',
                'verbose_name_plural': 'جزییات محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='نام برند')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='نام در url')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350, verbose_name='ویژگی محصول')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی محصولات',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='نام محصول')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('short_description', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه')),
                ('description', models.TextField(db_index=True, verbose_name='توضیحات اصلی')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
                ('slug', models.SlugField(blank=True, default='', max_length=200, unique=True, verbose_name='عنوان در url')),
                ('keyword', models.CharField(blank=True, max_length=400, null=True, verbose_name='')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productbrand', verbose_name='برند')),
                ('category', models.ManyToManyField(related_name='product_categories', to='product_module.productcategory', verbose_name='دسته بندی ها')),
                ('details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.detailsproduct', verbose_name='جزییات محصول')),
                ('property', models.ManyToManyField(blank=True, null=True, to='product_module.productproperty', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tags', to='product_module.products')),
            ],
            options={
                'verbose_name': 'تگ محصول',
                'verbose_name_plural': 'تگ های محصولات',
            },
        ),
    ]
