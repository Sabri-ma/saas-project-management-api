from rest_framework import generics, permissions

from .models import Team, TeamMembership
from .serializers import (
    TeamMembershipSerializer,
    TeamSerializer,
)
from apps.organizations.permissions import IsOrganizationAdminOrOwner

class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Team.objects.filter(
                organization__memberships__user=self.request.user
            )
            .distinct()
            .order_by("-created_at")
        )


class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated,IsOrganizationAdminOrOwner,]

    def get_queryset(self):
        return Team.objects.filter(
            organization__memberships__user=self.request.user
        ).distinct()


class TeamMembersView(generics.ListAPIView):
    serializer_class = TeamMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TeamMembership.objects.filter(
            team_id=self.kwargs["team_id"],
            team__organization__memberships__user=self.request.user,
        ).select_related("user")