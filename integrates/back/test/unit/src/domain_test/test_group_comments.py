from decimal import (
    Decimal,
)
from group_comments import (
    domain as group_comments_domain,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_fill_comment_data() -> None:
    test_data = {
        "content": "test content",
        "created": "2018-12-27 16:30:28",
        "email": "unittesting@test.com",
        "user_id": Decimal("1582646735480"),
        "modified": "2020-02-25 11:05:35",
        "parent": Decimal("0"),
    }
    # pylint: disable=protected-access
    res_data_no_fullname = await group_comments_domain._fill_comment_data(
        test_data
    )
    assert res_data_no_fullname["fullname"] == "unittesting@test.com"

    test_data["fullname"] = ""
    # pylint: disable=protected-access
    res_data_empty_fullname = await group_comments_domain._fill_comment_data(
        test_data
    )

    assert res_data_empty_fullname["fullname"] == "unittesting@test.com"
