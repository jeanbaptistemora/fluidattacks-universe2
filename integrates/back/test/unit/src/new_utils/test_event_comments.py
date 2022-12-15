from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from newutils.event_comments import (
    format_event_consulting_resolve,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_format_event_consulting_resolve() -> None:
    test_data = EventComment(
        event_id="422286126",
        id="1566336916294",
        parent_id="0",
        creation_date=datetime.fromisoformat("2019-08-20T21:35:16+00:00"),
        content="This is a comenting test",
        email="unittest@fluidattacks.com",
        full_name="Unit Test",
    )

    res_data_fullname = format_event_consulting_resolve(test_data)
    assert res_data_fullname["fullname"] == "Fluid Attacks"

    test_data = test_data._replace(
        email="unittest@gmail.com",
    )
    res_data_empty_fullname = format_event_consulting_resolve(test_data)
    assert res_data_empty_fullname["fullname"] == "Unit Test"

    test_data = test_data._replace(full_name=None)
    res_data_empty_fullname = format_event_consulting_resolve(test_data)
    assert res_data_empty_fullname["fullname"] == "unittest@gmail.com"
