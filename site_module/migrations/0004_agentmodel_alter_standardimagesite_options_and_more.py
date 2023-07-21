# Generated by Django 4.0.6 on 2022-09-01 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_standardimagesite_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='نام و نام خانوادگی نماینده')),
                ('city_country', models.CharField(blank=True, max_length=250, null=True, verbose_name='شهر یا کشور نماینده')),
                ('shopping_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='نام فروشگاه')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('is_internal', models.BooleanField(verbose_name='نماینده داخلی')),
            ],
            options={
                'verbose_name': 'نماینده',
                'verbose_name_plural': 'نماینده ها',
            },
        ),
        migrations.AlterModelOptions(
            name='standardimagesite',
            options={'verbose_name': 'استاندارد', 'verbose_name_plural': 'استاندارد ها'},
        ),
        migrations.CreateModel(
            name='AboutUsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_text', models.TextField(verbose_name='متن اصلی صفحه درباره ما')),
                ('text_service', models.TextField(verbose_name='متن اصلی صفحه خدمات پس از فروش')),
                ('is_main', models.BooleanField(verbose_name='تنضیمات فعال')),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_module.agentmodel', verbose_name='نماینده ها')),
            ],
            options={
                'verbose_name': 'تنظیمات',
                'verbose_name_plural': 'تنظیمات صفحه درباره ما',
            },
        ),
    ]