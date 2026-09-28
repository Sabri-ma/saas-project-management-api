from rest_framework import serializers

from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(
        source="actor.email",
        read_only=True,
    )

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "organization",
            "actor",
            "actor_email",
            "action",
            "entity_type",
            "entity_id",
            "description",
            "metadata",
            "created_at",
        ]

        read_only_fields = fields