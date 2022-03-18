from itertools import product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

from . utils import cookieCart, cartData, guestOrder

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    

    # code moved to utils.py
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
        
        #deleted code

        # items = []
        # order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']



    # code moved to utils.py
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']

        #deleted code after else

        # try:
        #     cart = json.loads(request.COOKIES['cart'])
        # except:
        #     cart = {}
        # print('Cart:', cart)
        # items = []
        # order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # cartItems = order['get_cart_items']

        # for i in cart:
        #     try:
        #         cartItems += cart[i]["quantity"]

        #         product = Product.objects.get(id=i)
        #         total = (product.price * cart[i]["quantity"])

        #         order['get_cart_total'] += total
        #         order['get_cart_items'] += cart[i]["quantity"]

        #         item = {
        #             'product':{
        #                 'id':product.id,
        #                 'name':product.name,
        #                 'price':product.price,
        #                 'imageURL':product.imageURL,
        #             },
        #             'quantity':cart[i]["quantity"],
        #             'get_total':total
        #         }
        #         items.append(item)

        #         if product.digital == False:
        #             order['shipping'] = True
        #     except:
        #         pass


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    # code moved to utils.py

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

        #deleted code

        # items = []
        # order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        # cartItems = order['get_cart_items']
        

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



# make changes here
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id

        # if total == float(order.get_cart_total):
        #     order.complete = True
        # order.save()

        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #     customer=customer,
        #     order=order,
        #     address=data['shipping']['address'],
        #     city=data['shipping']['city'],
        #     state=data['shipping']['state'],
        #     zipcode=data['shipping']['zipcode'],
        # )
    else:
        customer, order = guestOrder(request, data)

        # print('User is not logged in..')

        # print('COOKIES:', request.COOKIES)
        # name = data['form']['name']
        # email = data['form']['email']

        # cookieData = cookieCart(request)
        # items = cookieData['items']

        # customer, created = customer.objects.get_or_create(
        #     email=email,
        # )

        # customer.name = name
        # customer.save()

        # order = Order.objects.create(
        #     customer=customer,
        #     complete=False,
        # )

        # for item in items:
        #     product = Product.objects.get(id=item['product']['id'])

        #     orderItem = OrderItem.objects.create(
        #     product=product,
        #     order=order,
        #     quantity=item['quantity']
        #     )

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete', safe=False)
 