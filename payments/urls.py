from .views import *
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path("buy/", create_stripe_checkout, name='create_stripe_checkout'),
    path("", all_items, name='all_items'),
    path("item/<int:item_id>/", view_item, name='view_item'),
    path("cart/", view_cart, name='view_cart'),
    path("add_to_cart/", add_to_cart, name='add_to_cart'),
    path("successful_payment/", get_successful_payment, name='successful_payment'),

]