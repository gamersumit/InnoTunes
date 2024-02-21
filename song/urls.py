from django.urls import path
from . import views

urlpatterns = [
    path('', views.SongView.as_view(), name = 'song-view'),
    path('list/', views.SongListAPIView.as_view(), name = 'song-list'),
]