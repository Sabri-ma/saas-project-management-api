from rest_framework import generics, permissions

from .models import Project
from .serializers import ProjectSerializer
from apps.organizations.permissions import IsOrganizationAdminOrOwner

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Project.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "team",
                "created_by",
            )
            .distinct()
            .order_by("-created_at")
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,IsOrganizationAdminOrOwner,]
    def get_queryset(self):
        return (
            Project.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "team",
                "created_by",
            )
            .distinct()
        )