from django.urls import path, include, re_path
from rest_framework import routers
from . import views

# Create a router instance
router = routers.DefaultRouter()

# Register your viewsets with the router
router.register('playlist', views.PlaylistViewSet, 'playlist')
router.register('album', views.AlbumViewSet, 'album')


urlpatterns = [
    path('songs/', views.SongCreateView.as_view(), name='add_song_view'),
    path('songs/<str:field>/<str:id>/',
         views.SongListView.as_view(), name='songs_list'),
    path('playlist/<str:playlist_id>/<str:song_id>',
         views.AddDeleteSongsFromPlaylistView.as_view(), name='add_delete_songsfromPlaylist'),
    path('album/<str:album_id>/<str:song_id>', views.AddDeleteSongsFromAlbumView.as_view(), name = 'add_delete_songsfromPlaylist'),
    path('router/', include(router.urls))
]
