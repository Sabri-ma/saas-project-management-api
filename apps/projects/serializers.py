from rest_framework import serializers

from apps.organizations.models import OrganizationMembership
from apps.organizations.permissions import user_can_manage_organization
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "organization",
            "team",
            "name",
            "description",
            "status",
            "start_date",
            "due_date",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]

        organization = attrs.get(
            "organization",
            getattr(self.instance, "organization", None),
        )

        team = attrs.get(
            "team",
            getattr(self.instance, "team", None),
        )

        if organization and not OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
        ).exists():
            raise serializers.ValidationError(
                {
                    "organization": (
                        "You are not a member of this organization."
                    )
                }
            )

        if self.instance is None and not user_can_manage_organization(
            request.user,
            organization,
        ):
            raise serializers.ValidationError(
                {
                    "organization": (
                        "Only organization owners or admins can create projects."
                    )
                }
            )

        if team and team.organization_id != organization.id:
            raise serializers.ValidationError(
                {
                    "team": (
                        "This team does not belong to the selected organization."
                    )
                }
            )

        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )

        due_date = attrs.get(
            "due_date",
            getattr(self.instance, "due_date", None),
        )

        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError(
                {
                    "due_date": (
                        "Due date cannot be before start date."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        return Project.objects.create(
            created_by=self.context["request"].user,
            **validated_data,
        )