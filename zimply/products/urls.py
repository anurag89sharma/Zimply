from django.conf.urls import patterns, include, url
from views import homepage, add_product, products, view_products, product_details
from cart.views import add_to_cart,remove_from_cart, view_cart


urlpatterns = [
	#url(r'^invoice/(?P<id>[-\w]+)/$', 'delete_invoice'),
	url(r'^products/$', products),
	url(r'^view-products/$', view_products),
	url(r'^view-cart/$', view_cart),
	url(r'^api/add-product/$', add_product),
	url(r'^product/(?P<id>[-\w]+)/$', product_details),
	url(r'^api/add-to-cart/$', add_to_cart),
	url(r'^api/remove-from-cart/$', remove_from_cart),

	url( r'', homepage),
]