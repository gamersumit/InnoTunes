from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.CreateCommentView.as_view(), name = 'add-comment'),
    path('<str:field>/<str:id>/', views.CommentsListView.as_view(), name = 'show-comments'),
    
]