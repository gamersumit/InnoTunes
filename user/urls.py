from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.user_register_view, name = 'register'),
    path('logout/', views.user_logout_view, name = 'logout'),
    path('login/', views.user_login_view, name='login'),
    path('list/<str:id>/', views.user_detail_view, name = 'user_detail'),
    path('list/', views.user_list_view, name = 'list_user'),
    path('artists/', views.artist_list_view, name = 'list_artists'),
    path('artists/<str:pk>/', views.artist_detail_view, name = 'detail_artist')
]
