# Generated by Django 4.0.6 on 2022-07-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsproduct',
            name='title',
            field=models.CharField(default='test', max_length=300, verbose_name='نام محصول'),
            preserve_default=False,
        ),
    ]
