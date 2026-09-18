from rest_framework import serializers

from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(
        source="uploaded_by.email",
        read_only=True,
    )

    class Meta:
        model = Attachment
        fields = [
            "id",
            "task",
            "file",
            "original_name",
            "uploaded_by",
            "uploaded_by_email",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "original_name",
            "uploaded_by",
            "uploaded_by_email",
            "uploaded_at",
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

    def validate_file(self, file):
        max_size = 10 * 1024 * 1024

        if file.size > max_size:
            raise serializers.ValidationError(
                "Maximum file size is 10 MB."
            )

        allowed_extensions = {
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "doc",
            "docx",
            "txt",
            "zip",
        }

        extension = (
            file.name.rsplit(".", 1)[-1].lower()
            if "." in file.name
            else ""
        )

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "This file type is not allowed."
            )

        return file

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        return Attachment.objects.create(
            uploaded_by=self.context["request"].user,
            original_name=uploaded_file.name,
            **validated_data,
        )