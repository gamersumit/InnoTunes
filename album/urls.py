from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router2 = routers.DefaultRouter()
router.register('album/', views.AlbumViewSet, basename='album')
router2.register('songs/', views.SongsInAlbumViewSet, basename='songs')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router2.urls)),
]

