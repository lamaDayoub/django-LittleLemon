from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns = [
    path('cart/menu-items/', cart_list, name='cart-list'),
]