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
    path('songs/guest/', views.GuestUserSongListView.as_view(), name='guest_user_songs_list'),
    path('songs/artist/<str:id>/',views.ArtistSongListView.as_view(), name='artist_songs_list'),
    path('songs/album/<str:id>/',views.AlbumSongListView.as_view(), name='album_songs_list'),
    path('songs/playlist/<str:id>/',views.PlaylistSongListView.as_view(), name='playlist_songs_list'),
    path('songs/playlist/',views.AddDeleteSongsFromPlaylistView.as_view(), name='add_delete_songsfromPlaylist'),
    path('songs/album/', views.AddDeleteSongsFromAlbumView.as_view(), name = 'add_delete_songsfromPlaylist'),
    path('songs/recents/add/', views.AddToRecentsView.as_view(), name = 'add_to_recents'),
    path('songs/recents/', views.RecentSongsListView.as_view(), name = 'list_recent_songs'),
    path('playlist/liked/',views.LikedPlaylistListView.as_view(), name='liked_playlists'),
    path('album/liked/',views.LikedAlbumListView.as_view(), name='liked_albums'),
    path('songs/liked/<str:id>/', views.LikedSongsListView.as_view(), name='liked_songs'),
    path('playlist/list/<str:id>/', views.ListUserPlaylistView.as_view(), name = 'user_playlist_songs'),
    path('genre/recents/', views.RecentGenreListView.as_view(), name = 'recent_genres'),
    path('playlist/global/', views.GlobalPlaylistAPIView.as_view(), name = 'global_playlist_details'),
    # path('global/playlist/songs/<str:id>/', views.GetSongsInGlobalPlaylist.as_view(), name = 'get_songs_in_global_playlist'),
    # path('playlist/global/songs/<str:id>/', views.AddSongsInGlobalPlaylistAPIView.as_view(), name = 'add_gloabal_playlist'),
    path('genre/', views.GenreFilterAPIView.as_view(), name = 'top_three_genres'),
    path('router/', include(router.urls))
]
