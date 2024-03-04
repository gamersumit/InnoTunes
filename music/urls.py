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
    path('songs/', views.AllSongListView.as_view(), name='all_songs_list'),
    path('songs/artist/<str:id>/',views.ArtistSongListView.as_view(), name='songs_list'),
    path('songs/playlist/<str:id>/',views.PlaylistSongListView.as_view(), name='artist_songs_list'),
    path('songs/album/<str:id>/',views.AlbumSongListView.as_view(), name='album_songs_list'),
    path('songs/playlist/<str:id>/',views.PlaylistSongListView.as_view(), name='playlist_songs_list'),
    path('songs/playlist/',views.AddDeleteSongsFromPlaylistView.as_view(), name='add_delete_songsfromPlaylist'),
    path('songs/album/', views.AddDeleteSongsFromAlbumView.as_view(), name = 'add_delete_songsfromPlaylist'),
    path('songs/recents/add/', views.AddToRecentsView.as_view(), name = 'add_to_recents'),
    path('songs/recents/', views.RecentSongsListView.as_view(), name = 'list_recent_songs'),
    path('playlist/liked/',views.LikedPlaylistListView.as_view(), name='liked_playlists'),
    path('album/liked/',views.LikedAlbumListView.as_view(), name='liked_albums'),
    path('router/', include(router.urls))
]
