from .models import ActivityLog


def log_activity(
    *,
    organization,
    actor,
    action,
    entity=None,
    description="",
    metadata=None,
):
    entity_type = ""
    entity_id = ""

    if entity is not None:
        entity_type = entity.__class__.__name__
        entity_id = str(entity.pk)

    return ActivityLog.objects.create(
        organization=organization,
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        metadata=metadata or {},
    )