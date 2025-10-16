from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crop/<str:crop_name>/', views.crop_price, name='crop_price'),
    ]