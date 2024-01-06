from http.client import HTTPResponse
from smtplib import SMTPResponseException
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Record, val
from .forms import addrecord
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import os

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ItemSerializer

# Create your views here.
# LOGIN FUNCTION
def home(request):
    #records=api1(request)
    records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        val.v = request.POST.get('user_type1')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            

            messages.success(request,'You have login succesfully!')
            return redirect('home')
        else:
            messages.success(request,"We couldn't find an account with that username. Try another, or get a new  account.") 
            return redirect('home')
    else:
        if val.v == 'Ops':
            return render(request,'home.html',{'message1':'You can upload record by clicking on add record.'})
        else:
            return render(request,'home.html',{'records':records})

        #return render(request,'home.html')

# LOGOUT FUNCTION   
def logout_user(request):
    logout(request) 
    messages.success(request,"You have been logout succesfully") 
    return redirect('home')

#activate
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 
    

# REGISTER FUNCTION
def Register_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
      
        if form.is_valid():
            user = form.save(commit=False)

            user_type = request.POST.get('user_type')
            if user_type == 'Ops':
                user.is_active = True  
                user.save()  
                return HttpResponse('Thank you for registering. Now you can login your account.')
            else:
                user.is_active = False
                user.save()
            
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'   
                message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })  
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage(  
                    mail_subject, message, to=[to_email]  
                    )  
                email.send()  
                messages.success(request,"Please confirm your email address to complete the registration") 
                return redirect('home')
       
        else:  
            form = SignUpForm()
            return render(request, 'register.html', {'form': form})

    return render(request, 'register.html')

# Customer Records
@api_view(['GET'])
def down(request,pk):
  if request.user.is_authenticated:
    uploaded_file=Record.objects.get(id=pk)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response
  else:
        messages.success(request,"You must have to login to download!") 
        return redirect('home')

# ADD RECORD FUNCTION
def add_record(request):
    form=addrecord()
    if request.user.is_authenticated:
     if request.method=='POST':
        #form=api2(request)
        form=addrecord(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          messages.success(request,'Record added succesfully.....') 
          return redirect('home')
    else:
        messages.success(request,"You must have to login to add record!") 
        return redirect('home')
    return render(request,'addrecord.html',{'form':form})