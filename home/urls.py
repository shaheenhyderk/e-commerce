from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    path('sign-up/', views.signup, name='user_signup'),
    path('profile/', views.view_profile, name='user_profile'),
    path('address/', views.view_address, name='user_address'),
    path('address/create', views.create_address, name='create_address'),
    path('product/<int:id>', views.view_product, name='view_product'),
    path('add-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/edit/<int:id>', views.cart_edit, name='cart_edit'),
    path('cart/delete/<int:id>', views.cart_delete, name='cart_delete'),
]
