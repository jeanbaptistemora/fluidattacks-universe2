from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from newutils.finding_comments import (
    format_finding_consulting_resolve,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_fill_comment_data() -> None:
    test_data = FindingComment(
        finding_id="422286126",
        id="1566336916294",
        parent_id="0",
        comment_type=CommentType.COMMENT,
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
