from rest_framework import serializers

from apps.organizations.models import OrganizationMembership
from .models import Team, TeamMembership


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "organization",
            "name",
            "description",
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

    def validate_organization(self, organization):
        user = self.context["request"].user

        if not OrganizationMembership.objects.filter(
            organization=organization,
            user=user,
        ).exists():
            raise serializers.ValidationError(
                "You are not a member of this organization."
            )

        return organization

    def create(self, validated_data):
        user = self.context["request"].user

        team = Team.objects.create(
            created_by=user,
            **validated_data,
        )

        TeamMembership.objects.create(
            team=team,
            user=user,
            role=TeamMembership.Role.LEAD,
        )

        return team


class TeamMembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = TeamMembership
        fields = [
            "id",
            "user",
            "email",
            "role",
            "joined_at",
        ]

        read_only_fields = [
            "id",
            "joined_at",
        ]