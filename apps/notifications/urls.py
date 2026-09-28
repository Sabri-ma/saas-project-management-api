from django.urls import path

from .views import (
    MarkAllNotificationsReadView,
    NotificationDetailView,
    NotificationListView,
)


urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification-list",
    ),

    path(
        "read-all/",
        MarkAllNotificationsReadView.as_view(),
        name="notification-read-all",
    ),

    path(
        "<uuid:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
]