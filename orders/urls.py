from django.urls import path
from .views import OrderViewSet

# Define views for each action
order_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

order_detail = OrderViewSet.as_view({
    #'get': 'retrieve',
    'put': 'update',
    #'patch': 'partial_update',
    'delete': 'destroy',
})

retrieve_order_items = OrderViewSet.as_view({
    'get': 'retrieve_order_items',
})

update_order_status = OrderViewSet.as_view({
    'patch': 'update_order_status',
})

urlpatterns = [
    # List and create orders
    path('orders/', order_list, name='order-list'),

    # Retrieve, update, or delete a specific order
    path('orders/<int:pk>/', order_detail, name='order-detail'),

    # Retrieve order items for a specific order
    path('orders/<int:pk>/items/', retrieve_order_items, name='retrieve-order-items'),
    

    # Update order status (for delivery crew)
    path('orders/<int:pk>/status/', update_order_status, name='update-order-status'),
]