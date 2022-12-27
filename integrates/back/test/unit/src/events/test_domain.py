# pylint: disable=import-error
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from events.domain import (
    add_event,
)
import json
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


# pylint: disable=too-many-arguments
@pytest.mark.parametrize(
    ["group", "hacker_email", "attrs"],
    [
        [
            "unittesting",
            "unittesting@fluidattacks.com",
            {
                "context": "OTHER",
                "detail": "Something happened.",
                "event_date": datetime.fromisoformat(
                    "2019-12-09T05:00:00+00:00"
                ),
                "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
                "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            },
        ],
    ],
)
@patch(get_mocked_path("events_model.update_state"), new_callable=AsyncMock)
@patch(get_mocked_path("events_model.add"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.root.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.organization.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.group.load"), new_callable=AsyncMock)
async def test_add_event(
    mock_group_loader: AsyncMock,
    mock_organization_loader: AsyncMock,
    mock_root_loader: AsyncMock,
    mock_db_model_event_add: AsyncMock,
    mock_db_model_event_update_state: AsyncMock,
    group: str,
    hacker_email: str,
    attrs: Any,
) -> None:
    mock_group_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group.load"),
        json.dumps([group]),
    )
    mock_organization_loader.return_value = get_mock_response(
        get_mocked_path("loaders.organization.load"),
        json.dumps([group]),
    )
    mock_root_loader.return_value = get_mock_response(
        get_mocked_path("loaders.root.load"),
        json.dumps([group, attrs.get("root_id")]),
    )
    mock_db_model_event_add.return_value = get_mock_response(
        get_mocked_path("events_model.add"),
        json.dumps([group, hacker_email, attrs.get("root_id")]),
    )
    mock_db_model_event_update_state.return_value = get_mock_response(
        get_mocked_path("events_model.update_state"),
        json.dumps([group, hacker_email, attrs.get("root_id")]),
    )
    loaders = get_new_context()
    event_id = await add_event(
        loaders,
        hacker_email=hacker_email,
        group_name=group,
        **attrs,
    )
    assert event_id
    assert mock_group_loader.called is True
    assert mock_organization_loader.called is True
    assert mock_root_loader.called is True
