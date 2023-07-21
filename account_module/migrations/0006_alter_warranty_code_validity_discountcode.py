# Generated by Django 4.0.6 on 2022-09-27 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0005_alter_warranty_detail_alter_warranty_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warranty',
            name='code_validity',
            field=models.CharField(max_length=200, unique=True, verbose_name='کد گارانتی'),
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_discount', models.CharField(max_length=200, unique=True, verbose_name='کد گارانتی')),
                ('product_name', models.CharField(blank=True, max_length=350, null=True, verbose_name='اسم محصول')),
                ('detail', models.CharField(blank=True, max_length=400, null=True, verbose_name='اطلاعات بیشتر')),
                ('validity_date', models.CharField(blank=True, max_length=250, null=True, verbose_name='مدت اعتبار گارانتی')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تخیفات',
                'verbose_name_plural': 'کد های تخفیفات',
            },
        ),
    ]