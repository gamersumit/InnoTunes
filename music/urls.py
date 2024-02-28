from django.urls import path, include, re_path
from rest_framework import routers
from . import views

# Create a router instance
router = routers.DefaultRouter()

# Register your viewsets with the router
router.register('playlist', views.PlaylistViewSet, 'playlist')
router.register('album', views.AlbumViewSet, 'album')


urlpatterns = [
    path('songs/add/', views.SongCreateView.as_view(), name='add_song_view'),
    path('songs/<str:field>/<str:id>/',views.SongListView.as_view(), name='songs_list'),
    path('songs/', views.SongListView.as_view(), name='all_songs_list'),
    path('songs/playlist/',views.AddDeleteSongsFromPlaylistView.as_view(), name='add_delete_songsfromPlaylist'),
    path('songs/album/', views.AddDeleteSongsFromAlbumView.as_view(), name = 'add_delete_songsfromPlaylist'),
    path('router/', include(router.urls))
]
