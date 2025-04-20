from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    

    @swagger_auto_schema(
        operation_description="List all items in the cart for the current authenticated user.",
        responses={
            200: openapi.Response(
                description="List of cart items.",
                schema=CartSerializer(many=True)),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        # Return only the cart items for the current user
        return Cart.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Add a menu item to the cart for the current authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'menuitem': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the menu item to add."),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the menu item."),
            },
            required=['menuitem', 'quantity']
        ),
        responses={
            201: openapi.Response(
                description="Menu item added to the cart successfully.",
                schema=CartSerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)  
    def create(self, request, *args, **kwargs):
        # Add an item to the cart
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Delete all items in the cart for the current authenticated user.",
        responses={
            204: openapi.Response(
                description="All cart items deleted successfully.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        # Delete all items in the cart for the current user
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)