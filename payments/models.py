from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
import stripe
from contextlib import suppress

stripe.api_key = settings.STRIPE_SEC_KEY


class Item(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )

    description = models.CharField(
        'Описание',
        max_length=100
    )

    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def clean(self):
        discount = Discount.objects.first()
        if discount and discount.absolute_discount >= self.price:
            raise ValidationError('Скидка превышает цену товара')
    def __str__(self):
        return f'Товар {self.name}'


class CartQuerySet(models.QuerySet):
    def fetch_with_result_price(self):
        for cart in self:

            result_price = 0
            for order_item in cart.order_items.all():
                result_price += order_item.quantity * order_item.item.price

            cart.result_price = result_price
            cart.save()

        return self



class Cart(models.Model):
    result_price = models.DecimalField(
        'Полная цена заказа',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = CartQuerySet.as_manager()
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


    def __str__(self):
        return f'Корзина {self.id}'


class OrderItem(models.Model):
    item = models.ForeignKey(Item,
                             related_name='order_items',
                             verbose_name="Товар",
                             on_delete=models.CASCADE)

    cart = models.ForeignKey(Cart,
                             related_name='order_items',
                             verbose_name="Корзина",
                             on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField('Количество Товаров', default=1)


    class Meta:
        verbose_name = 'Позиция в заказе'
        verbose_name_plural = 'Позиции в заказе'


    def __str__(self):
        return f'{self.quantity} {self.item}-ов для {self.cart}'


class Discount(models.Model):

    percent_discount = models.IntegerField(
        'Скидка в процентах',
        validators=[MaxValueValidator(99), MinValueValidator(1)],
        null=True,
        blank=True
    )

    absolute_discount = models.IntegerField(
        'Скидка в рублях',
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )
    def clean(self):
        if not self.pk and Discount.objects.exists():
            raise ValidationError('Может быть только 1 скидка')

        if self.absolute_discount:
            items = Item.objects.all()
            for item in items:
                if item.price <= self.absolute_discount:
                    raise ValidationError(f'Скидка превышает цену товара {item}')

    def save(self, *args, **kwargs):
        super(Discount, self).save(*args, **kwargs)

        if self.absolute_discount:
            with suppress(stripe.error.InvalidRequestError):
                stripe.Coupon.delete(f"discount_{self.id}")
            stripe.Coupon.create(duration="forever", id=f"discount_{self.id}", amount_off=self.absolute_discount*100, currency='rub')


        else:
            with suppress(stripe.error.InvalidRequestError):
                stripe.Coupon.delete(f"discount_{self.id}")
            stripe.Coupon.create(duration="forever", id=f"discount_{self.id}", percent_off=self.percent_discount)




    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        constraints = [
            models.CheckConstraint(
                check=(
                              Q(absolute_discount__isnull=False) &
                              Q(percent_discount__isnull=True)
                      ) | (
                              Q(absolute_discount__isnull=True) &
                              Q(percent_discount__isnull=False)
                      ),
                name='only_one_discount',
            ),
        ]

    def __str__(self):

        if self.absolute_discount:
            return f'Скидка на {self.absolute_discount} рублей'
        return f'Скидка на {self.percent_discount} %'
