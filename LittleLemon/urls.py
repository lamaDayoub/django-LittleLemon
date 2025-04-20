"""
URL configuration for LittleLemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from users.views import custom_login, custom_logout  ,UserCreateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
schema_view = get_schema_view(
    openapi.Info(
        title="LittleLemon API",
        default_version='v1',
        description="API documentation for LittleLemon",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
def home(request):
       return HttpResponse("Welcome to LittleLemon API! Visit /swagger/ for documentation.")
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
   # path('__debuge__/',include('debug_toolbar.urls')),
    path('api/',include('users.urls')),
    path('api/',include('menu.urls')),
    path('api/',include('cart.urls')),
    path('api/',include('orders.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
     
   # path('api-token-auth/',obtain_auth_token),
   path('auth/signup/', UserCreateView.as_view(), name='signup'),
    path('auth/login/', custom_login,name='login'),  
    path('auth/logout/', custom_logout,name='logout'), 
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.authtoken')),
    path('api/token/',TokenObtainPairView.as_view(),name='token_pair_obtain'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    
]
