from django.urls import path

from .views import (
    OrganizationDetailView,
    OrganizationListCreateView,
    OrganizationMembersView,
)


urlpatterns = [
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organization-list-create",
    ),

    path(
        "<uuid:pk>/",
        OrganizationDetailView.as_view(),
        name="organization-detail",
    ),

    path(
        "<uuid:organization_id>/members/",
        OrganizationMembersView.as_view(),
        name="organization-members",
    ),
]