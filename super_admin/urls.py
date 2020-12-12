from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='admin_login'),
    path('logout/', views.logout, name='admin_logout'),
    path('options/', views.options, name='options'),
    path('products/', views.products, name='products'),

    path('products/create/', views.create_product, name='create_product'),
    path('products/edit/<int:id>', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>', views.delete_product, name='delete_product'),

    path('options/category/create/', views.create_category, name='create_category'),
    path('options/brand/create/', views.create_brand, name='create_brand'),
    path('options/processor/create/', views.create_processor, name='create_processor'),
    path('options/ram/create/', views.create_ram, name='create_ram'),
    path('options/storage/create/', views.create_storage, name='create_storage'),

    path('options/category/edit/<int:id>', views.edit_category, name='edit_category'),
    path('options/brand/edit/<int:id>', views.edit_brand, name='edit_brand'),
    path('options/processor/edit/<int:id>', views.edit_processor, name='edit_processor'),
    path('options/ram/edit/<int:id>', views.edit_ram, name='edit_ram'),
    path('options/storage/edit/<int:id>', views.edit_storage, name='edit_storage'),

    path('options/category/delete/<int:id>', views.delete_category, name='delete_category'),
    path('options/brand/delete/<int:id>', views.delete_brand, name='delete_brand'),
    path('options/processor/delete/<int:id>', views.delete_processor, name='delete_processor'),
    path('options/ram/delete/<int:id>', views.delete_ram, name='delete_ram'),
    path('options/storage/delete/<int:id>', views.delete_storage, name='delete_storage'),
]
