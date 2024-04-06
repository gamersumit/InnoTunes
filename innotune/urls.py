"""innotune URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from user import routing

from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from user.views import PatchLogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="Mock Test APIs",
        default_version="v1",
    ),
    public = False, # shows views which can be accessed by current user
    # permission_classes= [permissions.IsAuthenticated],
    # authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('music/', include('music.urls')),
    path('reach/', include('comment.urls')),
    path('colab/', include('colab.urls')),


    # rest framework overridden logout
    path('rest/logout/', PatchLogoutView.as_view(), name="logout"),
    # rest framework inbuilt
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
   
    # Swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
