from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.CreateCommentView.as_view(), name = 'add-comment'),
    path('usercomment/', views.UserCommentView.as_view(), name = 'user-view-comment'),
    path('songcomment/', views.SongCommentView.as_view(), name = 'song-view-comment'),
]