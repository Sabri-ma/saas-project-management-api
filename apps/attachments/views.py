from rest_framework import generics, permissions
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        queryset = (
            Attachment.objects.filter(
                task__project__organization__memberships__user=self.request.user
            )
            .select_related(
                "task",
                "uploaded_by",
            )
            .distinct()
            .order_by("-uploaded_at")
        )

        task_id = self.request.query_params.get("task")

        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset


class AttachmentDetailView(
    generics.RetrieveDestroyAPIView
):
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attachment.objects.filter(
            uploaded_by=self.request.user,
            task__project__organization__memberships__user=self.request.user,
        ).distinct()