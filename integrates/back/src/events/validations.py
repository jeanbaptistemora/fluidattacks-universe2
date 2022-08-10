from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)


def validate_type(event_type: EventType) -> None:
    if event_type in {
        EventType.CLIENT_CANCELS_PROJECT_MILESTONE,
        EventType.INCORRECT_MISSING_SUPPLIES,
    }:
        raise InvalidParameter("eventType")
