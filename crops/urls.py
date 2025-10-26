from django.urls import path
from . import views
import os

urlpatterns = [
    path('', views.health),
    path('platinum/', lambda r: views.get_price_endpoint(r, 'platinum')),
    path('oat/', lambda r: views.get_price_endpoint(r, 'oat')),
    path('rough-rice/', lambda r: views.get_price_endpoint(r, 'rough_rice')),
    path('micro-gold/', lambda r: views.get_price_endpoint(r, 'micro_gold')),
    path('submit-price/', views.submit_price),
]