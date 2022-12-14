# Generated by Django 4.1.1 on 2022-09-21 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_remove_item_stripe_price_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_discount', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Скидка в процентах')),
                ('absolute_discount', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Скидка в рублях')),
            ],
        ),
        migrations.AddConstraint(
            model_name='discount',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('absolute_discount__isnull', False), ('percent_discount__isnull', True)), models.Q(('absolute_discount__isnull', True), ('percent_discount__isnull', False)), _connector='OR'), name='only_one_discount'),
        ),
    ]
