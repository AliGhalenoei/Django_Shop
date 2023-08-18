from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views import View
import random
from utils import Send_Code
from django.contrib.auth import views as auth_view
# .imports
from .models import *
from .forms import *
from .serializers import *

# DRF imports...
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

  

# Create your views here.

class LoginView(View):
    template_name='accounts/login.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        user=authenticate(
            phone=phone,
            password=password
        )
        if user is not None:
            login(request,user)
            return redirect('home')
        return HttpResponse('FuckYou')
    
class SingupView(View):
    template_name='accounts/singup.html'

    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        try:
            User.objects.get(phone=phone)
            messages.info(request , 'این شماره تلفن از قبل وجود دارد')
            return redirect('singup')
        except:
            pass

        try:
            User.objects.get(email=email)
            messages.info(request,'این ایمیل از قبل وجود دارد')
            return redirect('singup')
        except:
            pass

        try:
            User.objects.get(username=username)
            messages.info(request,'این نام کاربری از قبل وجود دارد')
            return redirect('singup')
        except:
            pass

        try:
            if password != password2:
                messages.info(request,'رمزها با هم مطابقت ندارد')
                return redirect('singup')
        except:
            pass

        create_code=random.randint(1000,9999)
        Send_Code(phone,create_code)
        OTP.objects.create(phone=phone,code=create_code)
        request.session['singup_info']={
            'phone':phone,
            'email':email,
            'username':username,
            'password':password,
        }
        return redirect('veryfy')
    
class Veryfy_Singup_View(View):
    form_class=Veryfy_Singup_Form
    template_name='accounts/veryfy_singup.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self,request):
        user_session=request.session['singup_info']
        get_phone=OTP.objects.get(phone=user_session['phone'])
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            if cd['code'] == get_phone.code:
                User.objects.create_user(
                    phone=user_session['phone'],
                    email=user_session['email'],
                    username=user_session['username'],
                    password=user_session['password'],
                )
                get_phone.delete()
                return redirect('login')
            else:
                return redirect('veryfy')
        return render(request,self.template_name,{'form':form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')
    
class Password_Reset_User_View(auth_view.PasswordResetView):
    template_name='accounts/password_reset_form.html'
    success_url=reverse_lazy('password_reset_done')
    email_template_name='accounts/password_reset_email.html'

class Password_Reset_Done_View(auth_view.PasswordResetDoneView):
    template_name='accounts/password_reset_done.html'

class Password_Reset_Confirm_View(auth_view.PasswordResetConfirmView):
    template_name='accounts/password_reset_confirm.html'
    success_url=reverse_lazy('password_reset_complete')

class Password_Reset_Complete_View(auth_view.PasswordResetCompleteView):
    template_name='accounts/password_reset_complete.html'

# Apis....

class LoginAPIView(APIView):
    serializer_class=LoginSerializer

    def post(self,request):
        srz_data=self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            vd=srz_data.validated_data
            user=authenticate(
                phone=vd['phone'],
                password=vd['password'],
            )
            if user is not None:
                login(request,user)
                return Response(data=srz_data.data)
        return Response(srz_data.errors)
    
class SingupAPIView(APIView):
    serializer_class=SingupSerializer

    def post(self,request):
        srz_data=self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            vd=srz_data.validated_data
            #srz_data.create(vd)
            User.objects.create_user(
                phone=vd['phone'],
                email=vd['email'],
                username=vd['username'],
                password=vd['password'],
            )
            return Response(data=srz_data.data)
        return Response(srz_data.errors)
    
class UserListCreateAPIView(ListCreateAPIView):
    throttle_scope=('question')
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer






        


        
        
        
