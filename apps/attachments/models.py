import uuid

from django.conf import settings
from django.db import models

from apps.tasks.models import Task


def task_attachment_path(instance, filename):
    return f"tasks/{instance.task_id}/{filename}"


class Attachment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_attachments",
    )

    file = models.FileField(
        upload_to=task_attachment_path
    )

    original_name = models.CharField(
        max_length=255,
        blank=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or self.file.name