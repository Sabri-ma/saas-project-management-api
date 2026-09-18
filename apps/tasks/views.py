from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from .models import Task
from .serializers import TaskSerializer
from apps.organizations.permissions import IsOrganizationContributor

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "project",
        "status",
        "priority",
        "assignee",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Task.objects.filter(
                project__organization__memberships__user=self.request.user
            )
            .select_related(
                "project",
                "project__organization",
                "assignee",
                "reporter",
            )
            .distinct()
        )

        if self.request.query_params.get("assignee") == "me":
            queryset = queryset.filter(
                assignee=self.request.user
            )

        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsOrganizationContributor,]

    def get_queryset(self):
        return (
            Task.objects.filter(
                project__organization__memberships__user=self.request.user
            )
            .select_related(
                "project",
                "project__organization",
                "assignee",
                "reporter",
            )
            .distinct()
        )