from django.contrib import admin
from django.urls import path
from ezapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home,name='home'),
    path('logout/', views.logout_user,name='logout'),
    path('Register/', views.Register_user,name='Register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('record/<int:pk>', views.down,name='record'),
    path('add_record/', views.add_record,name='add_record'),
]