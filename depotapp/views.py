# -*- coding: utf-8 -*-
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from rest_framework.views import APIView

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import datetime
# app specific files

from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import mixins
from rest_framework import versioning
from rest_framework import viewsets

from .models import Product
from .serializer import ProductSerializer, LineItemSerializer


@csrf_exempt
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    t = get_template('depotapp/create_product.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def list_product(request):
  
    list_items = Product.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depotapp/list_product.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def view_product(request, id):
    product_instance = Product.objects.get(id = id)

    t=get_template('depotapp/view_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


@csrf_exempt
def edit_product(request, id):

    product_instance = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance = product_instance)

    if form.is_valid():
        form.save()

    t=get_template('depotapp/edit_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def store_view(request):
    products = Product.objects.filter(date_available__gt=datetime.datetime.now().date()).order_by("-date_available")
    t = get_template('depotapp/store.html')
    cart = request.session.get("cart",None)
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def view_cart(request):
    cart = request.session.get("cart",None)
    t = get_template('depotapp/view_cart.html')
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    cart = request.session.get("cart", None)
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    return view_cart(request)


def clean_cart(request):
    request.session['cart'] = Cart()
    return view_cart(request)



class ProductListAPIVIEW(APIView):
    """
    展示所有存在的snippet, 或建立新的snippet
    """
    def get(self, request, format=None):
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIVIEW(APIView):
    """
    展示, 更新或删除一个snippet
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductSerializer(snippet, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductList(generics.ListCreateAPIView):
    """
    使用基于class的view
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#这是两种方式 上面采用generics简单，
#下面采用mixins实现

class LineItemList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        print 'faaaaaaaaaaaaaa',request.data
        #product = Product.objects.get(id=request.POST['product'])
        #cart = request.session['cart']
        #cart.add_product(product)
        #request.session['cart'] = cart
        #return request.session['cart'].items
        return self.create(request, *args, **kwargs)


class LineItemDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def product_list(request):
    """
    List all code snippets, or create a new snippet. #例子1基于function based views.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        #products =  request.session['cart'].items
        #serializer = LineItemSerializer(products, many=True)
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def product_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    """
    List all snippets, or create a new snippet. #例子2基于function based views.
    """
    if request.method == 'GET':
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True) #如果没有many=ture会出错的
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        snippet = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(snippet, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def cart_list_session(request):
    """
    List all code snippets, or create a new snippet. #例子1基于function based views.
    """
    if request.method == 'GET':
        carts = request.session['cart'].items
        serializer = LineItemSerializer(carts, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        print request.POST['product']
        product = Product.objects.get(id=request.POST['product'])
        cart = request.session['cart']
        cart.add_product(product)
        request.session['cart'] = cart
        carts=request.session['cart'].items
        serializer = LineItemSerializer(carts, many=True)
        return JSONResponse(serializer.data)

        #data = JSONParser().parse(request)
        #serializer = LineItemSerializer(data=data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return JSONResponse(serializer.data, status=201)
        #else:
        #    return JSONResponse(serializer.errors, status=400)





