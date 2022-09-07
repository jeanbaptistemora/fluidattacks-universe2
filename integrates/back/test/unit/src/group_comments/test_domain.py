# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
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
import pytest
import time

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_comment() -> None:
    group_name = "unittesting"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = int(round(time.time() * 1000))
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    comment_data = GroupComment(
        id=str(comment_id),
        content="Test comment",
        creation_date=current_time,
        full_name="unittesting",
        parent_id="0",
        email="unittest@fluidattacks.com",
        group_name=group_name,
    )
    await add_comment(
        info.context.loaders,
        group_name,
        "unittest@fluidattacks.com",
        comment_data,
    )
    loaders = get_new_context()
    group_comments: list[GroupComment] = await loaders.group_comments.load(
        group_name
    )
    assert group_comments[-1].content == "Test comment"
    assert group_comments[-1].id == comment_data.id
    assert group_comments[-1].full_name == comment_data.full_name
