from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    GroupEventsRequest,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_list_events() -> None:
    group_name = "unittesting"
    expected_output = [
        "418900971",
        "463578352",
        "484763304",
        "538745942",
        "540462628",
        "540462638",
    ]
    loaders: Dataloaders = get_new_context()
    events_group = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    assert expected_output == sorted([event.id for event in events_group])
