# pylint: disable=import-error
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from custom_exceptions import (
    InvalidCommentParent,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from events.domain import (
    add_comment,
    add_event,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
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
    ["comment_data", "group"],
    [
        [
            EventComment(
                event_id="538745942",
                parent_id="0",
                creation_date=datetime.fromisoformat(
                    "2022-12-29 14:14:19.182591+00:00"
                ),
                content="comment test",
                id="1672323259183",
                email="integratesmanager@gmail.com",
                full_name="John Doe",
            ),
            "unittesting",
        ],
    ],
)
@patch(get_mocked_path("loaders.event_comments.load"), new_callable=AsyncMock)
@patch(get_mocked_path("event_comments_domain.add"), new_callable=AsyncMock)
@patch(
    get_mocked_path("authz.validate_handle_comment_scope"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("loaders.event.load"), new_callable=AsyncMock)
async def test_add_comment(
    mock_event_loader: AsyncMock,
    mock_authz_validate_handle_comment_scope: AsyncMock,
    mock_event_comments_domain_add: AsyncMock,
    mock_event_comments_loader: AsyncMock,
    comment_data: EventComment,
    group: str,
) -> None:
    mock_event_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event.load"),
        json.dumps([comment_data.event_id]),
    )
    mock_authz_validate_handle_comment_scope.return_value = get_mock_response(
        get_mocked_path("authz.validate_handle_comment_scope"),
        json.dumps(
            [
                comment_data.content,
                comment_data.email,
                group,
                comment_data.parent_id,
            ]
        ),
    )
    mock_event_comments_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event_comments.load"),
        json.dumps([comment_data.event_id]),
    )
    mock_event_comments_domain_add.return_value = get_mock_response(
        get_mocked_path("event_comments_domain.add"),
        json.dumps([comment_data], default=str),
    )
    loaders = get_new_context()

    await add_comment(
        loaders,
        comment_data,
        comment_data.email,
        comment_data.event_id,
        comment_data.parent_id,
    )

    with pytest.raises(InvalidCommentParent):
        await add_comment(
            loaders,
            comment_data,
            comment_data.email,
            comment_data.event_id,
            parent_comment=str(int(comment_data.parent_id) + 1),
        )

    assert mock_event_loader.called is True
    assert mock_authz_validate_handle_comment_scope.called is True
    assert mock_event_comments_loader.called is True
    assert mock_event_comments_domain_add.called is True


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
    assert isinstance(event_id, str)
    assert mock_group_loader.called is True
    assert mock_organization_loader.called is True
    assert mock_root_loader.called is True


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
@pytest.mark.parametrize(
    ["group", "hacker_email", "attrs", "file_name", "image_name"],
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
            "test-file-records.csv",
            "test-anim.webm",
        ],
    ],
)
@patch(get_mocked_path("update_evidence"), new_callable=AsyncMock)
@patch(get_mocked_path("validate_evidence"), new_callable=AsyncMock)
@patch(get_mocked_path("events_model.update_state"), new_callable=AsyncMock)
@patch(get_mocked_path("events_model.add"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.root.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.organization.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.group.load"), new_callable=AsyncMock)
async def test_add_event_file_image(
    mock_group_loader: AsyncMock,
    mock_organization_loader: AsyncMock,
    mock_root_loader: AsyncMock,
    mock_db_model_event_add: AsyncMock,
    mock_db_model_event_update_state: AsyncMock,
    mock_validate_evidence: AsyncMock,
    mock_update_evidence: AsyncMock,
    group: str,
    hacker_email: str,
    attrs: Any,
    file_name: str,
    image_name: str,
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
    mock_validate_evidence.return_value = get_mock_response(
        get_mocked_path("validate_evidence"),
        json.dumps([group, file_name]),
    )
    mock_validate_evidence.return_value = get_mock_response(
        get_mocked_path("validate_evidence"),
        json.dumps([group, image_name]),
    )
    mock_validate_evidence.return_value = get_mock_response(
        get_mocked_path("update_evidence"),
        json.dumps([file_name]),
    )
    mock_validate_evidence.return_value = get_mock_response(
        get_mocked_path("update_evidence"),
        json.dumps([image_name]),
    )
    loaders = get_new_context()
    files_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(files_path, "./mock/" + file_name)
    imagename = os.path.join(files_path, "./mock/" + image_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "okada-unittesting-0123456789.csv", test_file, "text/csv"
        )
        with open(imagename, "rb") as test_image:
            uploaded_image = UploadFile(
                "okada-unittesting-0987654321.webm", test_image, "video/webm"
            )
            event_id = await add_event(
                loaders,
                hacker_email=hacker_email,
                group_name=group,
                file=uploaded_file,
                image=uploaded_image,
                **attrs,
            )
    assert isinstance(event_id, str)
    assert mock_group_loader.called is True
    assert mock_organization_loader.called is True
    assert mock_root_loader.called is True
    assert mock_validate_evidence.called is True
    assert mock_update_evidence.called is True
