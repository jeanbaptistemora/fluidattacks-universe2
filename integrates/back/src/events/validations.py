from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)


def validate_type(event_type: EventType) -> None:
    if event_type is EventType.CLIENT_CANCELS_PROJECT_MILESTONE:
        raise InvalidParameter("eventType")
