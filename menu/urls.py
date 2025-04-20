from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, CategoryViewSet

# Define URL patterns for MenuItemViewSet
menu_item_list = MenuItemViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

menu_item_detail = MenuItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

# Define URL patterns for CategoryViewSet
category_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    # MenuItem endpoints
    path('menu-items/', menu_item_list, name='menu-item-list'),
    path('menu-items/<int:pk>/', menu_item_detail, name='menu-item-detail'),

    # Category endpoints
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
]