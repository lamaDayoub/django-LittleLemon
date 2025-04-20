from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import MenuItem, Category
from .serializers import MenuItemsSerializer, CategorySerializer
from users.permissions import IsManager
from .throttle import TenCallsPerMinute



# MenuItem ViewSet
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title']
    ordering_fields = ['price', 'title']
    ordering = ['title']
    # throttle_classes = [TenCallsPerMinute]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Any authenticated user can list or retrieve
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only managers can create, update, or delete
            return [IsAuthenticated(), IsManager()]
        return []

    @swagger_auto_schema(
        operation_description="List all menu items. **Authentication required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of menu items.",
                schema=MenuItemsSerializer(many=True)),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific menu item by ID. **Authentication required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Menu item details.",
                schema=MenuItemsSerializer),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            404: openapi.Response(
                description="Menu item not found.",
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new menu item. **Manager permission required.**",
        request_body=MenuItemsSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Menu item created successfully.",
                schema=MenuItemsSerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific menu item by ID. **Manager permission required.**",
        request_body=MenuItemsSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Menu item updated successfully.",
                schema=MenuItemsSerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Menu item not found.",
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific menu item by ID. **Manager permission required.**",
        request_body=MenuItemsSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Menu item partially updated successfully.",
                schema=MenuItemsSerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Menu item not found.",
            ),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific menu item by ID. **Manager permission required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            204: openapi.Response(
                description="Menu item deleted successfully.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Menu item not found.",
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Any authenticated user can list or retrieve
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only managers can create, update, or delete
            return [IsAuthenticated(), IsManager()]
        return []

    @swagger_auto_schema(
        operation_description="List all categories. **Authentication required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of categories.",
                schema=CategorySerializer(many=True)),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific category by ID. **Authentication required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Category details.",
                schema=CategorySerializer),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            404: openapi.Response(
                description="Category not found.",
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new category. **Manager permission required.**",
        request_body=CategorySerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Category created successfully.",
                schema=CategorySerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific category by ID. **Manager permission required.**",
        request_body=CategorySerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Category updated successfully.",
                schema=CategorySerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Category not found.",
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific category by ID. **Manager permission required.**",
        request_body=CategorySerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Category partially updated successfully.",
                schema=CategorySerializer),
            400: openapi.Response(
                description="Invalid input data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Category not found.",
            ),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific category by ID. **Manager permission required.**",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token for authentication.",
                required=True,
            ),
        ],
        responses={
            204: openapi.Response(
                description="Category deleted successfully.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication required.",
            ),
            403: openapi.Response(
                description="Forbidden. Manager permission required.",
            ),
            404: openapi.Response(
                description="Category not found.",
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)