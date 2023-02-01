from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)
import functools
from newutils.validations import (
    get_attr_value,
)
from typing import (
    Any,
    Callable,
)


def validate_type(event_type: EventType) -> None:
    if event_type in {
        EventType.CLIENT_CANCELS_PROJECT_MILESTONE,
        EventType.INCORRECT_MISSING_SUPPLIES,
    }:
        raise InvalidParameter("eventType")


def validate_type_deco(event_type_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            event_type: EventType = get_attr_value(
                field=event_type_field, kwargs=kwargs, obj_type=EventType
            )
            if event_type in {
                EventType.CLIENT_CANCELS_PROJECT_MILESTONE,
                EventType.INCORRECT_MISSING_SUPPLIES,
            }:
                raise InvalidParameter("eventType")
            return func(*args, **kwargs)

        return decorated

    return wrapper
