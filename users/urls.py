from django.urls import path
from .views import ManagerListView, ManagerDetailView,CustomerOnlyUsersView,DeliveryListView,DeliveryDetailView,get_user_role

urlpatterns = [
    path('role/', get_user_role, name='user-role'),
    path('users/',CustomerOnlyUsersView.as_view({'get': 'list'}),name='get-customerse'),
    path('groups/manager/users/', ManagerListView.as_view(http_method_names=['get']), name='manager-group-listing'),
    path('groups/manager/users/<int:userId>/', ManagerDetailView.as_view(http_method_names=['post', 'delete']), name='manager-group-detail'),
    path('groups/delivery-crew/users/', DeliveryListView.as_view(http_method_names=['get']), name='delivery-crew-group-listing'),
    path('groups/delivery-crew/users/<int:userId>/', DeliveryDetailView.as_view(http_method_names=['post', 'delete']), name='delivery-crew-group-detail'),
]