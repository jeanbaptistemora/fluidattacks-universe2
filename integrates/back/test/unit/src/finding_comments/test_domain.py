# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
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
            comment_type=CommentType.COMMENT,
            creation_date=datetime.fromisoformat("2019-08-20T21:35:16+00:00"),
            content="This is a comenting test",
            email="unittest@fluidattacks.com",
            full_name="unit test",
        )
    ]
    assert isinstance(test_data, tuple)
    assert isinstance(test_data[0], FindingComment)
    assert test_data[0] is not None
    assert sorted(test_data) == sorted(expected_output)
