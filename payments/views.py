from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, render, reverse, redirect
from more_itertools import chunked
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import stripe
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist


stripe.api_key = settings.STRIPE_SEC_KEY


from .serializers import AddToCartSerializer



def serialize_item(item):
    serialized_item = {
        'name': item.name,
        'price': item.price,
        'id': item.id,
        'description': item.description}

    discount = Discount.objects.first()
    if discount:
        if discount.absolute_discount:
            serialized_item['absolute_discount'] = discount.absolute_discount
            serialized_item['percent_discount'] = None
            serialized_item['price_with_discount'] = item.price - discount.absolute_discount
        else:
            serialized_item['absolute_discount'] = None
            serialized_item['percent_discount'] = discount.percent_discount
            serialized_item['price_with_discount'] = item.price * (100 - discount.percent_discount) / 100

    else:
        serialized_item['absolute_discount'] = None
        serialized_item['percent_discount'] = None

    return serialized_item



def all_items(request):
    try:
        cart_id = request.session.get('cart', None)
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create()
        request.session['cart'] = cart.id

    items = Item.objects.all()
    serialized_items = [serialize_item(item) for item in items]

    chunked_items = list(chunked(serialized_items, 2))
    return render(request, template_name='all_items.html',
                  context={'items': chunked_items})



def view_item(request, item_id):
    try:
        cart_id = request.session.get('cart', None)
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create()
        request.session['cart'] = cart.id

    item = get_object_or_404(Item, id=item_id)

    return render(request, template_name='item.html',
                  context={
                            'item': serialize_item(item)
                           })


def view_cart(request):
    cart_id = request.session.get('cart', None)
    if not cart_id:
        return render(request, template_name='empty_cart.html')

    cart = Cart.objects.filter(id=cart_id).prefetch_related(Prefetch(('order_items'), queryset=OrderItem.objects.select_related('item')))
    cart = cart.fetch_with_result_price()
    cart = cart.first()
    cart_items = [{'name': order_item.item.name,
                   'quantity': order_item.quantity,
                   'price': order_item.quantity*order_item.item.price,
                   'item_price': order_item.item.price} for order_item in cart.order_items.all()]
    if not len(cart_items):
        return render(request, template_name='empty_cart.html')

    return render(request, template_name='cart.html',
                  context={
                      'result_price': cart.result_price,
                      'items': cart_items,
                      'STRIPE_SECRET_TOKEN': settings.STRIPE_SEC_KEY
                  })


@api_view(['POST'])
def add_to_cart(request):

    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        try:
            cart_id = request.session.get('cart', None)
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
            request.session['cart'] = cart.id

        item = get_object_or_404(Item, id=serializer.data['item_id'])

        for order_item in cart.order_items.select_related('item'):
            if item.id == order_item.item.id:
                order_item.quantity += 1
                order_item.save()
                break
        else:
            OrderItem.objects.create(item=item, cart=cart)

        return Response(status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def create_stripe_checkout(request):
    cart_id = request.session['cart']
    cart = Cart.objects.filter(id=cart_id).fetch_with_result_price().first()
    discount = Discount.objects.first()
    if discount:
        discount = [{'coupon': f'discount_{discount.id}'}]

    order_items_data = [{"price_data": {
                    "currency": "rub",
                    "unit_amount": int(order_item.item.price * 100),
                    "product_data": {
                        "name": order_item.item.name,
                    },
                 }, "quantity": order_item.quantity,} for order_item in cart.order_items.select_related('item')]

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=order_items_data,
        client_reference_id=cart_id,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments:successful_payment')),
        cancel_url=request.build_absolute_uri(reverse('payments:view_cart')),
        discounts=discount if discount else []
    )

    last_checkout_id = request.session.get('last_checkout', 0)

    if last_checkout_id:
        last_checkout = stripe.checkout.Session.retrieve(last_checkout_id)

        if last_checkout['payment_status'] == 'open':
            stripe.checkout.Session.expire(last_checkout_id)

    request.session['last_checkout'] = checkout_session['id']

    return redirect(checkout_session.url)


def get_successful_payment(request):
    last_checkout_id = request.session.get('last_checkout', 0)
    if not last_checkout_id:
        return redirect('payments:all_items')

    cart_id = request.session['cart']
    cart = Cart.objects.filter(id=cart_id).fetch_with_result_price().first()

    last_checkout = stripe.checkout.Session.retrieve(last_checkout_id)
    if last_checkout["payment_status"] == 'paid':
        cart.is_payed = True
        cart.payment_id = last_checkout_id
        cart.save()
        del request.session['last_checkout']
        del request.session['cart']

    return render(request, template_name='successful_payment.html',
                  context={})