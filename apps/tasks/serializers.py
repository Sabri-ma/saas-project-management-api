from django.utils import timezone
from rest_framework import serializers

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
        return Task.objects.create(
            reporter=self.context["request"].user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        old_status = instance.status

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

        return instance