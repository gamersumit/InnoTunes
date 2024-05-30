from django.urls import path
from . import views



urlpatterns = [
    path('add/', views.PostColabView.as_view(), name = 'add_colab'),
    path('list/<str:field>/<str:id>/', views.GetColabsView.as_view(), name = 'get_user_and_song_colabs'),
    path('user/delete/<str:pk>/', views.UserDeleteColabView.as_view(), name = 'user_delete_colab'),
    path('artist/delete/<str:pk>/', views.ArtistDeleteColabView.as_view(), name = 'artist_delete_colab'),
]