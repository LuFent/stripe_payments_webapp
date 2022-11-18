from django.contrib import admin
from .models import *


class CartInline(admin.StackedInline):
    model = OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass



@admin.register(Cart)
class Cart(admin.ModelAdmin):
    inlines = (CartInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass