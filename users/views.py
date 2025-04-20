from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from .permissions import IsManager
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from .serializers import UserCreateSerializer,CustomerListSerializer
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view, permission_classes,authentication_classes,throttle_classes
from .authentication import CsrfExemptSessionAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied
from menu.throttle import TenCallsPerMinute
# Create your views here.




def get_highest_priority_role(user):
    if user.groups.filter(name='Manager').exists():
        return 'Manager'
    elif user.groups.filter(name='Delivery').exists():
        return 'Delivery'
    return 'Customer'  # Default role

@swagger_auto_schema(
    method='GET',
    operation_description="Get user's highest-priority role",
    responses={
        200: openapi.Response(
            description="Successfully retrieved user role",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'role': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=['manager', 'delivery', 'customer']
                    ),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        401: openapi.Response(
            description="Unauthorized",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Authentication credentials were not provided."
                    )
                }
            )
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response({
        'role': get_highest_priority_role(request.user),
        'username': request.user.username
    })
    

class ManagerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserCreateSerializer
    # throttle_classes=[TenCallsPerMinute]

    @swagger_auto_schema(
        operation_description="List all users in the Manager group. Only managers can access this endpoint.",
        responses={
            200: openapi.Response(
                description="List of users in the Manager group.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "username": "manager_user1",
                            "email": "manager1@example.com"
                        },
                        {
                            "id": 2,
                            "username": "manager_user2",
                            "email": "manager2@example.com"
                        }
                    ]
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        return manager_group.user_set.all()
    
class ManagerDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserCreateSerializer
    # throttle_classes=[TenCallsPerMinute]

    @swagger_auto_schema(
        operation_description="Add a user to the Manager group. Only managers can perform this action.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='The ID of the user to add to the Manager group.',
                    example=2
                ),
            },
            required=['user_id']
        ),
        responses={
            201: openapi.Response(
                description="User added to Manager group.",
                examples={
                    "application/json": {
                        "message": "User added to Manager group."
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "error": "User not found."
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name='Manager')
        user.groups.add(manager_group)
        return Response({"message": "User added to Manager group."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove a user from the Manager group. Only managers can perform this action.",
        responses={
            200: openapi.Response(
                description="User removed from Manager group.",
                examples={
                    "application/json": {
                        "message": "User removed from Manager group."
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "error": "User not found."
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('userId')
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name='Manager')
        user.groups.remove(manager_group)
        return Response({"message": "User removed from Manager group."}, status=status.HTTP_200_OK)







class DeliveryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserCreateSerializer
    # throttle_classes=[TenCallsPerMinute]

    @swagger_auto_schema(
        operation_description="List all users in the Delivery group. Only managers can access this endpoint.",
        responses={
            200: openapi.Response(
                description="List of users in the Delivery group.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "username": "delivery_user1",
                            "email": "delivery1@example.com"
                        },
                        {
                            "id": 2,
                            "username": "delivery_user2",
                            "email": "delivery2@example.com"
                        }
                    ]
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        delivery_group = Group.objects.get(name='Delivery')
        return delivery_group.user_set.all()
    
class DeliveryDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserCreateSerializer
    # throttle_classes=[TenCallsPerMinute]

    @swagger_auto_schema(
        operation_description="Add a user to the Delivery group. Only managers can perform this action.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='The ID of the user to add to the Delivery group.',
                    example=2
                ),
            },
            required=['user_id']
        ),
        responses={
            201: openapi.Response(
                description="User added to Delivery group.",
                examples={
                    "application/json": {
                        "message": "User added to Delivery group."
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "error": "User not found."
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        delivery_group = Group.objects.get(name='Delivery')
        user.groups.add(delivery_group)
        return Response({"message": "User added to Delivery group."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove a user from the Delivery group. Only managers can perform this action.",
        responses={
            200: openapi.Response(
                description="User removed from Delivery group.",
                examples={
                    "application/json": {
                        "message": "User removed from Delivery group."
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "error": "User not found."
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied. Only managers can perform this action.",
                examples={
                    "application/json": {
                        "error": "You do not have permission to perform this action."
                    }
                }
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('userId')
        user = get_object_or_404(User, id=user_id)
        delivery_group = Group.objects.get(name='Delivery')
        user.groups.remove(delivery_group)
        return Response({"message": "User removed from Delivery group."}, status=status.HTTP_200_OK)
    


@swagger_auto_schema(
    method='post',
    operation_description="Log out the currently authenticated user.",
    responses={
        200: openapi.Response(
            description="Logout successful.",
            examples={
                "application/json": {
                    "message": "Log out successfully."
                }
            }
        ),
        403: openapi.Response(
            description="Permission denied. User is not authenticated.",
            examples={
                "application/json": {
                    "error": "You do not have permission to perform this action."
                }
            }
        ),
    }
)
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
# @throttle_classes([TenCallsPerMinute])
def custom_logout(request):
    logout(request)
    return Response({"message":"log out succesfully"}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='post',
    operation_description="Authenticate a user and log them in.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The username of the user.',
                example='testuser'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The password of the user.',
                example='testpassword'
            ),
        },
        required=['username', 'password']
    ),
    responses={
        200: openapi.Response(
            description="Login successful.",
            examples={
                "application/json": {
                    "message": "You have logged in."
                }
            }
        ),
        400: openapi.Response(
            description="Invalid credentials.",
            examples={
                "application/json": {
                    "error": "Invalid username or password."
                }
            }
        ),
    }
)

@api_view(['POST'])
@permission_classes([AllowAny])
#@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([CsrfExemptSessionAuthentication])
# @throttle_classes([TenCallsPerMinute])
def custom_login(request):
    username = request.data.get('username')  # Use 'username' instead of 'email'
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message":"log in successfuly"},status=status.HTTP_200_OK)
    return Response({"message":"your informations are wrong"},status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Sign up a new user and add them to the Customer group.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the new user.'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the new user.'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the new user.'),
            },
            required=['username', 'email', 'password']
        ),
        responses={
            201: openapi.Response(
                description="User created and logged in successfully.",
                examples={
                    "application/json": {
                        "username": "newuser",
                        "email": "newuser@example.com",
                        "message": "User created and logged in successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input data.",
                examples={
                    "application/json": {
                        "error": "Invalid input data."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Log in the user after sign-up
        login(request, user)

        # Return the user data
        return Response({
            'username': user.username,
            'email': user.email,
            'message': 'User created and logged in successfully.'
        }, status=status.HTTP_201_CREATED)
        





class CustomerOnlyUsersView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = CustomerListSerializer
    # throttle_classes = [TenCallsPerMinute]

    @swagger_auto_schema(
        operation_description="Get users only in Customer group (excludes Delivery/Manager)",
        responses={
            200: openapi.Response(
                description="Success - List of customers",
                schema=CustomerListSerializer(many=True),
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={"application/json": {"detail": "Authentication credentials were not provided."}}
            ),
            403: openapi.Response(
                description="Forbidden - Manager access required",
                examples={"application/json": {"detail": "You do not have permission to perform this action."}}
            ),
            404: openapi.Response(
                description="Customer group not found",
                examples={"application/json": {"error": "Customer group does not exist"}}
            )
        },
        
    )
    def list(self, request, *args, **kwargs):
        # Handle 401 - Done automatically by IsAuthenticated
        
        # Handle 403 - Must check manually since IsManager is custom
        if not request.user.groups.filter(name='Manager').exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle 404 - Customer group check
        if not Group.objects.filter(name='Customers').exists():
            return Response(
                {"error": "Customer group does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Handle 200 - Success case
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """Returns queryset of pure customers"""
        customer_group = Group.objects.get(name='Customers')
        queryset = User.objects.filter(groups=customer_group)
        
        # Exclude users in other groups if they exist
        if Group.objects.filter(name='Delivery').exists():
            queryset = queryset.exclude(groups__name='Delivery')
        if Group.objects.filter(name='Manager').exists():
            queryset = queryset.exclude(groups__name='Manager')
            
        return queryset 