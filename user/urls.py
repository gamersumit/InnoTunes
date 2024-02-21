from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.user_register_view, name = 'register'),
    path('logout/', views.user_logout_view, name = 'logout'),
    path('login/', obtain_auth_token, name='login'),
]