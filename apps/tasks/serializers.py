from django.utils import timezone
from rest_framework import serializers

from apps.activity.services import log_activity
from apps.organizations.models import OrganizationMembership
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reporter",
            "due_date",
            "completed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reporter",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]

        project = attrs.get(
            "project",
            getattr(self.instance, "project", None),
        )

        assignee = attrs.get(
            "assignee",
            getattr(self.instance, "assignee", None),
        )

        if project and not OrganizationMembership.objects.filter(
            organization=project.organization,
            user=request.user,
        ).exists():
            raise serializers.ValidationError(
                {
                    "project": (
                        "You do not have access to this project."
                    )
                }
            )

        membership = OrganizationMembership.objects.filter(
            organization=project.organization,
            user=request.user,
        ).first()

        if (
            self.instance is None
            and membership
            and membership.role
            == OrganizationMembership.Role.VIEWER
        ):
            raise serializers.ValidationError(
                {
                    "project": (
                        "Viewers cannot create tasks."
                    )
                }
            )

        if assignee and not OrganizationMembership.objects.filter(
            organization=project.organization,
            user=assignee,
        ).exists():
            raise serializers.ValidationError(
                {
                    "assignee": (
                        "The assignee must belong to the same organization."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user

        task = Task.objects.create(
            reporter=user,
            **validated_data,
        )

        log_activity(
            organization=task.project.organization,
            actor=user,
            action="task.created",
            entity=task,
            description=f"Task '{task.title}' was created.",
            metadata={
                "status": task.status,
                "priority": task.priority,
            },
        )

        return task

    def update(self, instance, validated_data):
        user = self.context["request"].user

        old_status = instance.status
        old_priority = instance.priority

        instance = super().update(
            instance,
            validated_data,
        )

        if (
            old_status != Task.Status.DONE
            and instance.status == Task.Status.DONE
        ):
            instance.completed_at = timezone.now()
            instance.save(update_fields=["completed_at"])

        elif (
            old_status == Task.Status.DONE
            and instance.status != Task.Status.DONE
        ):
            instance.completed_at = None
            instance.save(update_fields=["completed_at"])

        metadata = {}

        if old_status != instance.status:
            metadata["old_status"] = old_status
            metadata["new_status"] = instance.status

        if old_priority != instance.priority:
            metadata["old_priority"] = old_priority
            metadata["new_priority"] = instance.priority

        log_activity(
            organization=instance.project.organization,
            actor=user,
            action="task.updated",
            entity=instance,
            description=f"Task '{instance.title}' was updated.",
            metadata=metadata,
        )

        return instance