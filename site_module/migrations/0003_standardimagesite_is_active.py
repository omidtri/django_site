# Generated by Django 4.0.6 on 2022-08-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0002_standardimagesite_sitesetting_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardimagesite',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال / غیرفعال'),
        ),
    ]