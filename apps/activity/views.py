from rest_framework import generics, permissions

from .models import ActivityLog
from .serializers import ActivityLogSerializer


class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = (
            ActivityLog.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "actor",
            )
            .distinct()
        )

        organization_id = self.request.query_params.get(
            "organization"
        )

        if organization_id:
            queryset = queryset.filter(
                organization_id=organization_id
            )

        action = self.request.query_params.get("action")

        if action:
            queryset = queryset.filter(action=action)

        return queryset