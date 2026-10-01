from django.urls import path
from .views import (
    EnrollmentListCreateAPIView,
    EnrollmentDetailAPIView
)


urlpatterns = [
    path(
        '',
        EnrollmentListCreateAPIView.as_view(),
        name='enrollment-list-create'
    ),

    path(
        '<int:pk>/',
        EnrollmentDetailAPIView.as_view(),
        name='enrollment-detail'
    ),
]