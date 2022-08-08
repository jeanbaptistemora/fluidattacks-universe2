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
from newutils.finding_comments import (
    format_finding_consulting_resolve,
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
    test_data = FindingComment(
        finding_id="422286126",
        id="1566336916294",
        parent_id="0",
        comment_type="comment",
        creation_date="2019-08-20T21:35:16+00:00",
        content="This is a comenting test",
        email="unittest@fluidattacks.com",
        full_name="Unit Test",
    )

    res_data_fullname = format_finding_consulting_resolve(test_data)
    assert res_data_fullname["fullname"] == "Unit Test at Fluid Attacks"

    test_data = test_data._replace(
        email="unittest@gmail.com",
    )
    res_data_empty_fullname = format_finding_consulting_resolve(test_data)
    assert res_data_empty_fullname["fullname"] == "Unit Test"

    test_data = test_data._replace(full_name=None)
    res_data_empty_fullname = format_finding_consulting_resolve(test_data)
    assert res_data_empty_fullname["fullname"] == "unittest@gmail.com"
