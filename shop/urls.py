from django.contrib import admin
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name= "logout"),
    path('search', views.search, name="search"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]