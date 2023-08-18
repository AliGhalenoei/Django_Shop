
from typing import Any
from django.shortcuts import render,redirect,HttpResponse
from django.urls import path

# FREE_URL=[
#     '/accounts/login/',
#     '/accounts/singup/',
#     '/shop/home/',
#     '/shop/list_product/',
#     '/shop/list_laptop_product/',
#     '/shop/list_mobail_product/',
#     '/shop/search_product/',
#     '/shop/detail_product/<slug:slug>/',
    
# ]

# class LoginRequiredUser:
#     def __init__(self,get_response) -> None:
#         self.get_response=get_response

#     def __call__(self, request) -> Any:
#         if not request.user.is_authenticated and request.path not in FREE_URL:
#             return redirect('login')
        
#         response=self.get_response(request)
#         return response