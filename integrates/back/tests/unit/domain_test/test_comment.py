from back.tests.unit import (
    MIGRATION,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from comments import (
    domain as comments_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_list_comments() -> None:
    finding_id = "422286126"
    user_email = "unittest@fluidattacks.com"
    request = await create_dummy_session(user_email)
    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, request
    )
    test_data = await comments_domain.get_comments(
        "unittesting", finding_id, user_email, info
    )
    expected_output = [
        {
            "parent": "0",
            "created": "2019/08/20 16:35:16",
            "modified": "2019/08/20 16:35:16",
            "content": "This is a comenting test",
            "email": "unittest@fluidattacks.com",
            "fullname": "unit test at Fluid Attacks",
            "id": "1566336916294",
        }
    ]
    assert isinstance(test_data, list)
    assert isinstance(test_data[0], dict)
    assert test_data[0] is not None
    assert sorted(test_data) == sorted(expected_output)  # type: ignore


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
