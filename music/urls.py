from django.urls import path
from rest_framework import routers
from . import views

# Create a router instance
router = routers.DefaultRouter()

# Register your viewsets with the router
router.register('playlist/', views.PlayListViewSet, basename = 'playlist')

urlpatterns = [
    path('', views.SongView.as_view(), name = 'song-view'),
    path('list/', views.SongListAPIView.as_view(), name = 'song-list'),
]


# Include the router URLs
urlpatterns += router.urls