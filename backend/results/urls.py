from django.urls import path
from .views import (
    ResultListCreateAPIView,
    ResultDetailAPIView
)


urlpatterns = [
    path(
        '',
        ResultListCreateAPIView.as_view(),
        name='result-list-create'
    ),

    path(
        '<int:pk>/',
        ResultDetailAPIView.as_view(),
        name='result-detail'
    ),
]