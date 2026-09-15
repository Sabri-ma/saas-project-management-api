from django.utils.text import slugify
from rest_framework import serializers

from .models import Organization, OrganizationMembership


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        name = validated_data["name"]

        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        organization = Organization.objects.create(
            created_by=user,
            slug=slug,
            **validated_data,
        )

        OrganizationMembership.objects.create(
            organization=organization,
            user=user,
            role=OrganizationMembership.Role.OWNER,
        )

        return organization


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = OrganizationMembership
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