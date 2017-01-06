
from django.conf.urls import url
from .views import *

urlpatterns =[

    url(r'^product/create/$', create_product, name='create_product'),
    url(r'^product/list/$', list_product, name='list_product'),
    url(r'^product/edit/(?P<id>[^/]+)/$', edit_product, name='edit_product'),
    url(r'^product/view/(?P<id>[^/]+)/$', view_product, name='view_product'),
    url(r'store/$', store_view, name='store_view'),
    url(r'cart/view/', view_cart, name='view_cart'),
    url(r'cart/add/(?P<id>[^/]+)/$', add_to_cart, name='add_to_cart'),
    url(r'cart/clean/', clean_cart, name='clean_cart'),
    
]
