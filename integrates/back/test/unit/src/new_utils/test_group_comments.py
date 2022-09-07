# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.group_comments.types import (
    GroupComment,
)
from newutils.group_comments import (
    format_group_consulting_resolve,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_format_group_consulting_resolve() -> None:
    test_data = GroupComment(
        group_name="unittesting",
        content="test content",
        creation_date="2018-12-27 16:30:28",
        email="unittesting@test.com",
        id="1582646735480",
        parent_id="0",
    )
    res_data_no_fullname = format_group_consulting_resolve(test_data)
    assert res_data_no_fullname["fullname"] == "unittesting@test.com"

    test_data = test_data._replace(full_name="")
    res_data_empty_fullname = format_group_consulting_resolve(test_data)
    assert res_data_empty_fullname["fullname"] == "unittesting@test.com"
