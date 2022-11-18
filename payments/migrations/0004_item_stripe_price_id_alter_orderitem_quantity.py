# Generated by Django 4.1.1 on 2022-09-18 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_cart_result_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stripe_price_id',
            field=models.CharField(default=1, max_length=50, verbose_name='id цены на Stripe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество Товаров'),
        ),
    ]