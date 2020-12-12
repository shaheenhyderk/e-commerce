from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    path('sign-up/', views.signup, name='user_signup'),
    path('product/<int:id>', views.view_product, name='view_product'),
]
