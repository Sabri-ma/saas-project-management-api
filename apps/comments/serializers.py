from rest_framework import serializers

from apps.activity.services import log_activity
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(
        source="author.email",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "task",
            "author",
            "author_email",
            "content",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "author_email",
            "created_at",
            "updated_at",
        ]

    def validate_task(self, task):
        user = self.context["request"].user

        if not task.project.organization.memberships.filter(
            user=user
        ).exists():
            raise serializers.ValidationError(
                "You do not have access to this task."
            )

        return task

    def create(self, validated_data):
        user = self.context["request"].user

        comment = Comment.objects.create(
            author=user,
            **validated_data,
        )

        log_activity(
            organization=comment.task.project.organization,
            actor=user,
            action="comment.created",
            entity=comment,
            description=(
                f"Comment added to task '{comment.task.title}'."
            ),
            metadata={
                "task_id": str(comment.task.id),
            },
        )

        return comment