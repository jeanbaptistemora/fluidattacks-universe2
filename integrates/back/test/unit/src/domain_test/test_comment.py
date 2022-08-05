# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from finding_comments import (
    domain as comments_domain,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_list_comments() -> None:
    finding_id = "422286126"
    user_email = "unittest@fluidattacks.com"
    request = await create_dummy_session(user_email)
    info = create_dummy_info(request)
    test_data = await comments_domain.get_comments(
        loaders=info.context.loaders,
        group_name="unittesting",
        finding_id=finding_id,
        user_email=user_email,
    )
    expected_output = [
        FindingComment(
            finding_id="422286126",
            id="1566336916294",
            parent_id="0",
            comment_type="comment",
            creation_date="2019-08-20T21:35:16+00:00",
            content="This is a comenting test",
            email="unittest@fluidattacks.com",
            full_name="unit test",
        )
    ]
    assert isinstance(test_data, tuple)
    assert isinstance(test_data[0], FindingComment)
    assert test_data[0] is not None
    assert sorted(test_data) == sorted(expected_output)


async def test_fill_comment_data() -> None:
    test_data = {
        "comment_id": "1582646735480",
        "content": "test content",
        "created": "2018-12-27 16:30:28",
        "email": "unittesting@test.com",
        "modified": "2020-02-25 11:05:35",
        "parent": "0",
    }
    # pylint: disable=protected-access
    res_data_no_fullname = await comments_domain._fill_comment_data(test_data)
    assert res_data_no_fullname["fullname"] == "unittesting@test.com"

    test_data["fullname"] = ""
    # pylint: disable=protected-access
    res_data_empty_fullname = await comments_domain._fill_comment_data(
        test_data
    )

    assert res_data_empty_fullname["fullname"] == "unittesting@test.com"
