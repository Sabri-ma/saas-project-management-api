from rest_framework import generics, permissions

from .models import Organization, OrganizationMembership
from .serializers import (
    OrganizationMembershipSerializer,
    OrganizationSerializer,
)


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Organization.objects.filter(
                memberships__user=self.request.user
            )
            .distinct()
            .order_by("-created_at")
        )


class OrganizationDetailView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user
        ).distinct()


class OrganizationMembersView(generics.ListAPIView):
    serializer_class = OrganizationMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrganizationMembership.objects.filter(
            organization_id=self.kwargs["organization_id"],
            organization__memberships__user=self.request.user,
        ).select_related("user")