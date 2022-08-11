from custom_exceptions import (
    EventNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_exception_event_not_found() -> None:
    loaders: Dataloaders = get_new_context()
    with pytest.raises(EventNotFound):
        await loaders.event.load("000001111")
