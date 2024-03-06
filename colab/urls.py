from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('add/', views.ColabView.as_view(), name = 'add_colab'),
    path('list/<str:field>/<str:id>/', views.GetColabsView.as_view(), name = 'get_user_and_song_colabs'),
    path('user/delete/<str:pk>/', views.UserDeleteColabView.as_view(), name = 'user_delete_colab'),
    path('artist/delete/<str:pk>/', views.ArtistDeleteColabView.as_view(), name = 'artist_delete_colab'),
]