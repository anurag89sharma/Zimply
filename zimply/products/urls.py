from django.conf.urls import patterns, include, url
from views import homepage, add_product, products, view_products, product_details

urlpatterns = [
	#url(r'^invoice/(?P<id>[-\w]+)/$', 'delete_invoice'),
	url(r'^products/$', products),
	url(r'^view-products/$', view_products),
	url(r'^api/add-product/$', add_product),
	url(r'^product/(?P<id>[-\w]+)/$', product_details),
    url( r'', homepage),
]