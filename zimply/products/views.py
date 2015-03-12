import sys
import json
import requests
import pprint
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from models import Product, Category, Seller, shipping
from django.db.models import Q
from decimal import *
from django.template import RequestContext, loader
from rest_framework.decorators import api_view
from forms import DocumentForm
# Create your views here.

import os
path = os.path.join(settings.BASE_DIR, 'static/images').replace('\\', '/')

def homepage(request):
    template = loader.get_template('product/homepage.html')
    context = RequestContext(request, { })
    return HttpResponse(template.render(context))

def products(request):
    form = DocumentForm() 
    shipping_details = shipping
    categories = Category.objects.all().values_list('id','name')
    seller = Seller.objects.all().values_list('id','name')
    template = loader.get_template('product/add_product.html')
    context = RequestContext(request, {
        'shipping_details': shipping_details,
        'categories' : categories,
        'seller' : seller,
        'form' : form,
    })
    return HttpResponse(template.render(context))

def view_products(request):
    products = Product.objects.all().values('id','name','price','image','dimensions')#,'category__name','shipping_details','sold_by__name')
    for product in products:
        product['price'] = str(product['price'])
        product['dimensions'] = ' x '.join(product['dimensions'])
        #product['shipping_details'] = dict(shipping)[product['shipping_details']]

    template = loader.get_template('product/view_products.html')
    context = RequestContext(request, {
        'products' : products,
    })
    return HttpResponse(template.render(context))

def product_details(request, *args, **kwargs):
    product_id = kwargs.get('id')
    products = Product.objects.filter(id=product_id).values('id','name','price','image','dimensions','category__name','shipping_details','sold_by__name')
    for product in products:
        product['price'] = str(product['price'])
        product['dimensions'] = ' x '.join(product['dimensions'])
        #product['shipping_details'] = dict(shipping)[product['shipping_details']]

    template = loader.get_template('product/product_detail.html')
    context = RequestContext(request, {
        'products' : products,
    })
    return HttpResponse(template.render(context))

#psql -h localhost -U postgres
#\connect zimply;

@api_view(['POST'])
@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        import pdb;pdb.set_trace()
    	product = {}
        product['name'] = request.data.get('pr_name')
        #product['image'] = 'images/%s' % (request.data.get('docfile'),)
        product['image'] = str(request.data.get('docfile'))
        product['price'] = request.data.get('pr_price')
        product['category_id'] = int(request.data.get('pr_category'))
        product['dimensions'] = request.data.get('pr_dimension').split(',')
        product['shipping_details'] = request.data.get('pr_ship_details')
        product['sold_by_id'] = int(request.data.get('pr_seller'))

        form = DocumentForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                filelist = request.FILES.getlist('docfile')
                for files in filelist:
                    filepath = os.path.join(path,files.name)
                    fout = open(filepath, 'wb+')
                    filecontent = ContentFile( files.read() )
                    for chunks in filecontent.chunks():
                        fout.write(chunks)
                    fout.close()
        except:
            return HttpResponse(json.dumps("Error Saving the File"))	

    Product.objects.create(**product)   
    template = loader.get_template('product/homepage.html')
    context = RequestContext(request, { })
    return HttpResponse(template.render(context))
