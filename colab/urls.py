from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('colab', views.ColabViewSet, 'colab')
urlpatterns = [
    path('', include(router.urls)),
    path('<str:field>/<str:id>/', views.GetColabsView.as_view(), name = 'get_user_and_song_colabs'),
    path('delete/<str:field>/<str:id>/', views.DeleteColabView.as_view(), name = 'delete_colab'),
    path('delete/<str:field1>/<str:id1>/<str:field2>/<str:id2>', views.DeleteColabView.as_view(), name = 'delete_colab'),
]
