from dataloaders import (
    get_new_context,
)
from events.domain import (
    has_access_to_event,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_has_access_to_event() -> None:
    loaders = get_new_context()
    assert await has_access_to_event(
        loaders, "unittest@fluidattacks.com", "418900971"
    )
