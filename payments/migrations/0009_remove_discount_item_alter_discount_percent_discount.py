# Generated by Django 4.1.1 on 2022-11-18 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0008_alter_discount_options_alter_discount_item"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="discount",
            name="item",
        ),
        migrations.AlterField(
            model_name="discount",
            name="percent_discount",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(99),
                    django.core.validators.MinValueValidator(1),
                ],
                verbose_name="Скидка в процентах",
            ),
        ),
    ]
