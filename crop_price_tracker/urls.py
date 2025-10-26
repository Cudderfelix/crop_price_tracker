from django.contrib import admin
from django.urls import path, include
from crops import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/', include('crops.urls')),
    path('crop/<str:crop_name>/', views.crop_price, name='crop_price'),
]