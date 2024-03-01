from django.urls import path, include
from rest_framework import routers
from . import views

# Create a router instance
router = routers.DefaultRouter()

# Register your viewsets with the router
router.register('', views.CommentViewset, 'comment')


urlpatterns = [
    path('comment/<str:field>/<str:id>/', views.CommentsListView.as_view(), name = 'show_comments'),
    path('follow/', views.FollowUnfollowView.as_view(), name = 'follow_unfollow'),
    path('followers/<str:id>/', views.ListAllFollowersView.as_view(), name = 'list_followers'),
    path('following/<str:id>/', views.ListAllFollowingView.as_view(), name = 'list_following'),
    path('like/song/', views.SongLikeDislikeView.as_view(), name = 'song_like_dislike'),
    path('like/album/', views.AlbumLikeDislikeView.as_view(), name = 'album_like_dislike'),
    path('like/playlist/', views.PlaylistLikeDislikeView.as_view(), name = 'playlist_like_dislike'),
]

urlpatterns += router.urls