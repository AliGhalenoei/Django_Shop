from typing import Any
from django import http
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.views import View
from django.core.mail import send_mail
import random
import datetime
# .imports...
from .cart import Cart
from .models import *
from .forms import *
from .serializers import *
# imports DRF...
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# Create your views here.

class HomeView(View):
    template_name='shop/home.html'

    def get(self,request,slug=None):
        products=Product.objects.all()  #order_by('-id')[:3]
        category_laptop=Category.objects.get(name='Laptop')
        laptops=Product.objects.filter(category=category_laptop)[:3]

        category_mobail=Category.objects.get(name='Mobail')
        mobails=Product.objects.filter(category=category_mobail)[:3]

        category_sub=Category.objects.filter(is_sub=True)
        category_not_sub=Category.objects.filter(is_sub=False)

        if slug:
            category=Category.objects.get(slug=slug)
            products=products.filter(category=category)

        return render(request,self.template_name,{
            'products':products,
            'laptops':laptops,
            'mobails':mobails,
            'category_sub':category_sub,
            'category_not_sub':category_not_sub,
        })
    
class List_Product_View(View):
    template_name='shop/list_product.html'

    def get(self,request):
        products=Product.objects.all()
        paginator=Paginator(products,3)
        get_paginator=request.GET.get('page')
        list_product=paginator.get_page(get_paginator)
        return render(request,self.template_name,{
            'products':list_product,
        })

class List_Laptop_product_View(View):
    template_name='shop/list_laptop_product.html'

    def get(self,request):
        category_laptop=Category.objects.get(name='Laptop')
        products=Product.objects.filter(category=category_laptop)
        paginator=Paginator(products,1)
        get_paginator=request.GET.get('page')
        list_product=paginator.get_page(get_paginator)
        return render(request,self.template_name,{
            'products':list_product,
        })
    
class List_Mobail_product_View(View):
    template_name='shop/list_mobail_product.html'

    def get(self,request):
        category_mobail=Category.objects.get(name='Mobail')
        products=Product.objects.filter(category=category_mobail)
        paginator=Paginator(products,1)
        get_paginator=request.GET.get('page')
        list_product=paginator.get_page(get_paginator)
        return render(request,self.template_name,{
            'products':list_product,
        })
    
class Filter_Category_Img(View):
    template_name='shop/filter_category_img.html'

    def get(self,request,slug):
        category=Category.objects.get(slug=slug)
        products=Product.objects.filter(category=category)
        return render(request,self.template_name,{'products':products})
    
class Call_Me(View):
    form_class=Call_Me_Form
    template_name='shop/call_me.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            name=cd['name']
            subject=cd['subject']
            massage=cd['massage']
            email=cd['email']
            phone=cd['phone']
            msg='name:{0}\nsubject:{1}\nmassage:{2}\nemail:{3}\nphone:{4}'.format(name,subject,massage,email,phone)
            send_mail(cd['subject'],msg,'alighalenoei8383@gmail.com',['alighalenoei8383@gmail.com'],fail_silently=False)
            return redirect('home')
        return render(request,self.template_name,{'form':form})
    
class Search_ProductView(View):
    template_name='shop/search_product.html'

    def get(self,request):
        products=Product.objects.all()
        # paginator=Paginator(products,2)
        # get_paginator=request.GET.get('page')
        # list_products=paginator.get_page(get_paginator)
        if request.GET.get('search'):
            products=products.filter(name__contains=request.GET['search'])
        return render(request,self.template_name,{'products':products})

    
# Detail Products...

class DetailProductView(View):
    form_class=CartForm
    form_class_comment=Comment_Product_Form
    template_name='shop/detail_product.html'

    def setup(self, request, *args, **kwargs) -> None:
        self.product_ins=Product.objects.get(slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self,request,slug):
        product=self.product_ins #Product.objects.get(slug=slug)
        products=Product.objects.all()
        random_products=random.sample(list(products),k=5)
        comments=product.product_comment.filter(is_sub=True)

        return render(request,self.template_name,{
            'product':product,
            'random_products':random_products,
            'form':self.form_class,
            'form_comment':self.form_class_comment,
            'comments':comments
        })
    def post(self,request,slug):
        form=self.form_class_comment(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new=form.save(commit=False)
            new.user=request.user
            new.product=self.product_ins
            new.save()
            return redirect('detail_product' , slug)
        return render(request,self.template_name,{'form':form})
    
# Views Cart...

class CartView(View):
    template_name='shop/cart.html'

    def get(self,request):
        cart=Cart(request)
        return render(request,self.template_name,{'cart':cart})
    
class Add_Cart_View(View):
    form_class=CartForm

    def post(self,request,pk):
        cart=Cart(request)
        product=Product.objects.get(id=pk)
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            cart.Add_To_Cart(product,cd['tedad'])
        return redirect('cart')
    
class Delete_In_Cart_View(View):

    def get(self,request,pk):
        cart=Cart(request)
        product=Product.objects.get(id=pk)
        cart.Delete_in_Cart(product)
        return redirect('cart')
    
class CreateCheckoutView(View):

    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user)
        
        for i in cart:
            OrderIten.objects.create(
                order=order,
                product=i['product'],
                price=i['price'],
                tedad=i['tedad'],
            )
        cart.Clear_Cart()
        return redirect('detail_checkout',order.pk)
    
class DetailCheckoutView(View):
    form_class=CuponForm
    template_name='shop/detail_checkout.html'

    def get(self,request,pk):
        order=Order.objects.get(id=pk)
        #orderitem=OrderIten.objects.get(id=pk)
        return render(request,self.template_name,{'order':order,'form':self.form_class})
    
class CuponView(View):
    form_class=CuponForm

    def post(self,request,pk):
        now=datetime.datetime.now()
        form=self.form_class(request.POST)
        if form.is_valid():
            code=form.cleaned_data['code']
            try:
                cupon=Cupon.objects.get(
                    code__exact=code,
                    start__lte=now,
                    end__gte=now,
                    is_active=True,
                )
            except Cupon.DoesNotExist:
                # return redirect('detail_checkout', pk)
                return redirect('detail_checkout' , pk)
        order=Order.objects.get(id=pk)
        order.discount = cupon.discount
        order.save()
        return redirect('detail_checkout' , pk)

# Django===> Rest_Framework
# Api Views...

class ListCategoryAPIView(APIView):
    serializer_class=CategorySerializer

    def get(self,request):
        queryset=Category.objects.all()
        srz_data=self.serializer_class(instance=queryset,many=True)
        return Response(data=srz_data.data)
    
class RetrieveCategoryAPIView(APIView):
    serializer_class=CategorySerializer

    def get(self,request,slug):
        queryset=Category.objects.get(slug=slug)
        srz_data=self.serializer_class(instance=queryset)
        return Response(data=srz_data.data)
    
class CreateCategoryAPIView(APIView):
    serializer_class=CategorySerializer

    def post(self,request):
        srz_data=self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            vd=srz_data.validated_data
            Category.objects.create(
                name=vd['name'],
                slug=vd['slug'],
            )
            return Response(data=srz_data.data)
        return Response(srz_data.errors)
    
class UpdateCategoryAPIView(APIView):
    serializer_class=CategorySerializer

    def put(self,request,slug):
        queryset=Category.objects.get(slug=slug)
        srz_data=self.serializer_class(instance=queryset,data=request.data,partial=True)
        if srz_data.is_valid():
            srz_data.validated_data
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(srz_data.errors)
    
class DestroyCategoryAPIView(APIView):
    serializer_class=CategorySerializer

    def get(self,request,slug):
        queryset=Category.objects.get(slug=slug)
        queryset.delete()
        return Response({'massage':'Category Deleted'})
    
class ProductApiViewset(viewsets.ViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def list(self, request):
        #queryset=self.queryset
        srz_data=self.serializer_class(instance=self.queryset,many=True)
        return Response(data=srz_data.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset=self.queryset.get(id=pk)
        srz_data=self.serializer_class(instance=queryset)
        return Response(data=srz_data.data)

    def partial_update(self, request, pk=None):
        queryset=self.queryset.get(id=pk)
        srz_data=self.serializer_class(instance=queryset,data=request.POST,partial=True)
        if srz_data.is_valid():
            vd=srz_data.validated_data
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(srz_data.errors)

    def destroy(self, request, pk=None):
        queryset=Product.objects.get(id=pk)
        queryset.is_avalable=False
        queryset.save()
        return Response({'massage':'Product is_available Falsed... '})
    



    



        

    
