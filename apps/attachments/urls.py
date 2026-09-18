from django.urls import path

from .views import (
    AttachmentDetailView,
    AttachmentListCreateView,
)


urlpatterns = [
    path(
        "",
        AttachmentListCreateView.as_view(),
        name="attachment-list-create",
    ),

    path(
        "<uuid:pk>/",
        AttachmentDetailView.as_view(),
        name="attachment-detail",
    ),
]