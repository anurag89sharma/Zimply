import sys
import json
import requests
import pprint
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.shortcuts import render
from products.models import Product, Category, Seller, shipping
from models import cart
from django.template import RequestContext, loader
from rest_framework.decorators import api_view
from collections import Counter
# Create your views here.
@csrf_exempt
@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        obj, created = cart.objects.get_or_create(user=request.user)
        if obj.cart_details: obj.cart_details.append(product_id)
        else: obj.cart_details = list(product_id)
        obj.save()
        data = {'remove_flag':1}
        return HttpResponse(json.dumps(data))


@csrf_exempt
@api_view(['POST'])
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = str(request.data.get('product_id'))
        obj = cart.objects.filter(user=request.user, cart_details__contains=[product_id])
        #import pdb;pdb.set_trace();
        if obj.exists():
            # This didnt work....
            #obj[0].cart_details.remove(product_id)
            #obj[0].save()
            #print obj[0].cart_details

            # This works....
            cart_object = obj[0]
            cart_object.cart_details.remove(product_id)
            cart_object.save()
            #print cart_object.cart_details

            if product_id in cart_object.cart_details:
                data = {'remove_flag':1}
            else:
                data = {'remove_flag':0}
            return HttpResponse(json.dumps(data))


def view_cart(request):
    obj = cart.objects.filter(user=request.user)
    if obj.exists():
        cart_details = obj[0].cart_details
        items_count = Counter(cart_details)
        products = items_count.keys()
        product_details = Product.objects.filter(id__in=items_count.keys()).values('id','name','price','image','dimensions')
        total_price = 0.0
        for items in product_details:
            items['total_quantity'] = float(items_count[str(items['id'])])
            items['total_item_price'] =  float(items_count[str(items['id'])] * items['price'])
            total_price += items['total_item_price']

        template = loader.get_template('cart/view_my_cart.html')
        context = RequestContext(request, {
            'products' : product_details,
            'total_price' : total_price,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponse(json.dumps("Please login first to view your cart details"))


