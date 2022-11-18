# Generated by Django 4.1.1 on 2022-09-18 15:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_cart_alter_item_options_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='result_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Полная цена заказа'),
        ),
    ]
