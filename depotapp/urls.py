
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
    url(r'^API/product/list/', ProductList.as_view()),
    url(r'^API/product/detail/(?P<pk>[0-9]+)$', ProductDetail.as_view()),
    url(r'^API/cart/list/', LineItemList.as_view()),
    url(r'^API/cart/detail/(?P<pk>[0-9]+)$', LineItemDetail.as_view()),
    url(r'^API/product/list_old/$', product_list),
    url(r'^API/product/detail_old/(?P<pk>[0-9]+)/$', product_detail),
    url(r'^API/product/list_api_view/$', product_list_api_view),
    url(r'^API/product/detail_api_view/(?P<pk>[0-9]+)/$', product_detail_api_view),
    url(r'^API/product/list_api_class/', ProductListAPIVIEW.as_view()),
    url(r'^API/product/detail_api_class/(?P<pk>[0-9]+)$', ProductDetailAPIVIEW.as_view()),
    url(r'^API/product/cart_list_session/$', cart_list_session),


]
