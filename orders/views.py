from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer, OrderItemSerializer
from users.permissions import IsManager
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.permissions import IsManager,IsDeliveryCrew,IsCustomer
from rest_framework.decorators import action
from django.http import Http404
from django.contrib.auth.models import User

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    @swagger_auto_schema(
        operation_description="List orders. Customers see their own orders, managers see all orders, and delivery crew see orders assigned to them.",
        responses={
            200: openapi.Response(
                description="List of orders.",
                schema=OrderSerializer(many=True)),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            # Manager: Return all orders
            return Order.objects.all()
        elif user.groups.filter(name='Delivery').exists():
            # Delivery Crew: Return orders assigned to them
            return Order.objects.filter(delivery_crew=user)
        else:
            # Customer: Return their own orders
            return Order.objects.filter(user=user)
      
    @swagger_auto_schema(
    operation_description="Retrieve all items for a specific order. Only accessible by the customer who placed the order.",
    responses={
        200: OrderItemSerializer(many=True),  # Success response
        403: openapi.Response(description="Forbidden: You do not have permission to view this order."),
        404: openapi.Response(description="Not Found: The order does not exist."),
    },
    manual_parameters=[
        openapi.Parameter(
            name='id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the order to retrieve items for.",
            required=True,
        ),
    ],
    )
    
    @action(detail=True,methods=['get'],permission_classes=[IsAuthenticated,IsCustomer])
    def retrieve_order_items(self, request, pk=None):
        user=request.user
        try:
            order = self.get_object()  
        except Http404:
            return Response(
                {"detail": "Not Found: The order does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        
        if order.user!=user:
            return Response({"detail": "You do not have permission to view this order."}, 
                            status=status.HTTP_403_FORBIDDEN)
        order_items=order.order_items.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Update an order. Only accessible by managers. Can update delivery crew and order status.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'delivery_crew': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the delivery crew user.",
                ),
                'status': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Order status (0 = Out for delivery, 1 = Delivered).",
                ),
            },
        ),
        responses={
            200: openapi.Response("Order updated successfully.", OrderSerializer),
            403: openapi.Response("Forbidden: Only managers can update orders."),
            404: openapi.Response("Not Found: The order does not exist."),
        },
    )
    
    def update(self, request, *args, **kwargs):
        order=self.get_object()
        user=request.user
        
        if not user.groups.filter(name='Manager').exists():
            return Response({"detail": "Only managers can update orders."}, 
                            status=status.HTTP_403_FORBIDDEN)
            
        delivery_crew_id=request.data.get('delivery_crew')
        order_status=request.data.get('status')
        if delivery_crew_id:
            try:
                delivery_crew_user = User.objects.get(id=delivery_crew_id)
                order.delivery_crew = delivery_crew_user
            except User.DoesNotExist:
                return Response(
                {"detail": "Invalid delivery crew user ID."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
            
        if status:
            order.status=order_status
        order.save()
        serializer=self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Delete an order. Only accessible by managers.",
        responses={
            204: openapi.Response("Order deleted successfully."),
            403: openapi.Response("Forbidden: Only managers can delete orders."),
            404: openapi.Response("Not Found: The order does not exist."),
        },
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the order to delete.",
                required=True,
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        # Only managers can delete orders
        if not user.groups.filter(name='Manager').exists():
            return Response({"detail": "Only managers can delete orders."}, status=status.HTTP_403_FORBIDDEN)

        order.delete()
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
    @swagger_auto_schema(
        operation_description="Update the status of an order. Only accessible by the delivery crew assigned to the order.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Order status (0 = Out for delivery, 1 = Delivered).",
                ),
            },
            required=['status'],
        ),
        responses={
            200: openapi.Response("Order status updated successfully.", OrderSerializer),
            400: openapi.Response("Bad Request: Invalid status value. Must be 0 or 1."),
            403: openapi.Response("Forbidden: You are not assigned to this order."),
            404: openapi.Response("Not Found: The order does not exist."),
        },
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the order to update.",
                required=True,
            ),
        ],
    )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsDeliveryCrew])
    def update_order_status(self, request, pk=None):
        order = self.get_object()
        user = request.user

        # Check if the delivery crew is assigned to this order
        if order.delivery_crew != user:
            return Response({"detail": "You are not assigned to this order."}, status=status.HTTP_403_FORBIDDEN)

        # Only allow updating the status
        status_value = request.data.get('status')
        if status_value not in [0, 1]:
            return Response({"detail": "Invalid status value. Must be 0 or 1."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

      
    @swagger_auto_schema(
        operation_description="Create a new order from the current user's cart. Only customers can create orders.",
        responses={
            201: openapi.Response(
                description="Order created successfully.",
                schema=OrderSerializer),
            400: openapi.Response(
                description="Invalid input data or empty cart.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Only customers can create orders.",
            ),
        }
    )
    
        
    def create(self,request,*args,**kwargs):
        user=request.user
        
        if user.groups.filter(name='Customers').exists():
            cart_items=Cart.objects.filter(user=user)
            
            if not cart_items.exists():
                return Response({"detail": "Your cart is empty."},
                                status=status.HTTP_400_BAD_REQUEST)
                
            order=Order.objects.create(
                user=user,
                total=sum(item.price for item in cart_items),
                status=False
            )
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menuitem=cart_item.menuitem,  # Copy the menu item from the cart
                    quantity=cart_item.quantity,  # Copy the quantity from the cart
                    unit_price=cart_item.unit_price,  # Copy the unit price from the cart
                    price=cart_item.price,  
                )
            cart_items.delete()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Only customers can create orders."}, status=status.HTTP_403_FORBIDDEN)
                
