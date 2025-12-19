from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.vendor_register, name='vendor_register'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('membership/', views.membership, name='membership'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('', views.vendors_list, name='vendors_list'),
    path('<str:slug>/', views.vendor_store, name='vendor_store'),
]
