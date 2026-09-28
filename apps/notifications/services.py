from .models import Notification


def create_notification(
    *,
    recipient,
    notification_type,
    title,
    message,
    entity=None,
):
    entity_type = ""
    entity_id = ""

    if entity is not None:
        entity_type = entity.__class__.__name__
        entity_id = str(entity.pk)

    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        entity_type=entity_type,
        entity_id=entity_id,
    )