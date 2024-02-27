from django.urls import path, include
from rest_framework import routers
from . import views

# Create a router instance
router = routers.DefaultRouter()

# Register your viewsets with the router
router.register('', views.CommentViewset, 'comment')


urlpatterns = [
    path('<str:field>/<str:id>/', views.CommentsListView.as_view(), name = 'show_comments'),
    path('follow/', views.FollowUnfollowView, name = 'follow_unfollow'),
    path('followers/<str:id>/', views.ListAllFollowersView, name = 'list_followers'),
    path('like/', views.LikeDislikeView, name = 'like_dislike'),
]

urlpatterns += router.urls