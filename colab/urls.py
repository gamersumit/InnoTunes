from django.urls import path
from .views import UserColabListViewSet

urlpatterns = [
    path('', UserColabListViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='colabs-list'),

    path('<int:pk>/', UserColabListViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='colab-detail'),
]
