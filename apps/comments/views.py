from rest_framework import generics, permissions

from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Comment.objects.filter(
                task__project__organization__memberships__user=self.request.user
            )
            .select_related(
                "task",
                "author",
            )
            .distinct()
            .order_by("created_at")
        )

        task_id = self.request.query_params.get("task")

        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset


class CommentDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            author=self.request.user,
            task__project__organization__memberships__user=self.request.user,
        ).distinct()