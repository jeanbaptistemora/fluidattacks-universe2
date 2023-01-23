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
from db_model.group_comments.types import (
    GroupComment,
)
from group_comments.domain import (
    add_comment,
)
import json
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["group_name", "comment_data"],
    [
        [
            "unittesting",
            GroupComment(
                id="1672083646257",
                content="Test comment",
                creation_date=datetime.fromisoformat(
                    "2022-04-06T16:46:23+00:00"
                ),
                full_name="unittesting",
                parent_id="0",
                email="unittest@fluidattacks.com",
                group_name="unittesting",
            ),
        ],
    ],
)
@patch(
    get_mocked_path("authz.validate_handle_comment_scope"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("group_comments_model.add"), new_callable=AsyncMock)
async def test_add_comment(
    mock_group_comments_model_add: AsyncMock,
    mock_authz_validate_handle_comment_scope: AsyncMock,
    group_name: str,
    comment_data: GroupComment,
) -> None:
    loaders = get_new_context()
    mock_authz_validate_handle_comment_scope.return_value = get_mock_response(
        get_mocked_path("authz.validate_handle_comment_scope"),
        json.dumps(
            [
                comment_data.content,
                comment_data.email,
                group_name,
                comment_data.parent_id,
            ]
        ),
    )
    mock_group_comments_model_add.return_value = get_mock_response(
        get_mocked_path("group_comments_model.add"),
        json.dumps([comment_data], default=str),
    )
    await add_comment(
        loaders=loaders, group_name=group_name, comment_data=comment_data
    )
    assert mock_authz_validate_handle_comment_scope.called is True
    assert mock_group_comments_model_add.called is True
