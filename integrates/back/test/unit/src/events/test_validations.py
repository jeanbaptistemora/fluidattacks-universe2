from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)
from events.validations import (
    validate_type,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_type() -> None:
    validate_type(event_type=EventType.CLONING_ISSUES)
    with pytest.raises(InvalidParameter):
        validate_type(event_type=EventType.INCORRECT_MISSING_SUPPLIES)
