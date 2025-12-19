from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
    path('<str:category_slug>/<str:product_slug>/', views.product_detail, name='product_detail'),
]
