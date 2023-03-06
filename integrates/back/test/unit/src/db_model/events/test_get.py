from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_side_effects,
)
from db_model.events.get import (
    EventLoader,
)
from db_model.events.types import (
    Event,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["event_id", "event_id_not_found"],
    [["418900971", "123456789"]],
)
@patch(MODULE_AT_TEST + "_get_event", new_callable=AsyncMock)
async def test_eventloader(
    mock__get_event: AsyncMock,
    event_id: str,
    event_id_not_found: str,
) -> None:
    assert set_mocks_side_effects(
        mocks_args=[[event_id]],
        mocked_objects=[mock__get_event],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_get_event"],
    )
    event = EventLoader()
    result = await event.load(event_id)
    assert isinstance(result, Event)
    assert result.client == "Fluid"
    assert result.id == event_id
    assert mock__get_event.call_count == 1

    mock__get_event.side_effect = [None]
    event_not_found = await event.load(event_id_not_found)
    assert not isinstance(event_not_found, Event)
    assert not event_not_found
    assert mock__get_event.call_count == 2
