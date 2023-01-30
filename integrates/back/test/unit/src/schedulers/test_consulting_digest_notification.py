from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.group_comments.types import (
    GroupComment,
)
from freezegun import (
    freeze_time,
)
import pytest
from pytz import (
    UTC,
)
from schedulers.consulting_digest_notification import (
    _get_days_since_comment,
    CommentsDataType,
    digest_comments,
    finding_comments,
    format_comment,
    group_comments,
    group_instance_comments,
    instance_comments,
    last_comments,
    unique_emails,
)
from typing import (
    Any,
    Union,
)

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2022-12-07T00:00:00.0")
def test_get_days_since_comment() -> None:
    assert (
        _get_days_since_comment(datetime(2022, 12, 1).replace(tzinfo=UTC)) == 6
    )


@pytest.mark.parametrize(
    ["comments"],
    [
        [
            (
                GroupComment(
                    group_name="unittesting",
                    id="1545946228675",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 1, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
                GroupComment(
                    group_name="unittesting",
                    id="1545946228676",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 2, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
                GroupComment(
                    group_name="unittesting",
                    id="1545946228677",
                    parent_id="0",
                    creation_date=datetime(2022, 12, 4, 22, 0, 0, tzinfo=UTC),
                    content="Now we can post comments on groups",
                    email="unittest@fluidattacks.com",
                    full_name="Miguel de Orellana",
                ),
            )
        ],
    ],
)
@freeze_time("2022-12-05T06:00:00.0")
def test_last_comments(
    *,
    comments: tuple[Union[GroupComment, EventComment, FindingComment], ...],
) -> None:
    assert len(last_comments(comments)) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
    ],
    [
        [
            "unittesting",
        ],
    ],
)
@freeze_time("2018-12-28T06:00:00.0")
async def test_group_comments(
    group_name: str,
) -> None:
    comments = await group_comments(get_new_context(), group_name)
    assert len(comments) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["instance_id", "instance_type"],
    [
        ["422286126", "finding"],
    ],
)
@freeze_time("2019-08-21T06:00:00.0")
async def test_instance_comments(instance_id: str, instance_type: str) -> None:
    comments = await instance_comments(
        get_new_context(), instance_id, instance_type
    )
    assert len(comments) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["group_name", "instance_type"],
    [
        ["unittesting", "finding"],
    ],
)
@freeze_time("2019-08-21T06:00:00.0")
async def test_group_instance_comments(
    group_name: str, instance_type: str
) -> None:
    loaders = get_new_context()
    group_findings = await loaders.group_findings.load(group_name)
    comments = await group_instance_comments(
        loaders, tuple(group_findings), instance_type
    )
    assert len(comments) == 1


@pytest.mark.parametrize(
    ["groups_data"],
    [
        [
            {
                "oneshottest": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "customer_manager@fluidattacks.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "integratesuser@gmail.com",
                    ),
                    "group_comments": (),
                    "event_comments": {},
                    "finding_comments": {},
                },
                "unittesting": {
                    "org_name": "okada",
                    "email_to": (
                        "continuoushack2@gmail.com",
                        "continuoushacking@gmail.com",
                        "integratesmanager@fluidattacks.com",
                        "integratesmanager@gmail.com",
                        "integratesresourcer@fluidattacks.com",
                        "integratesuser2@gmail.com",
                        "unittest2@fluidattacks.com",
                    ),
                    "group_comments": (),
                    "event_comments": {},
                    "finding_comments": {},
                },
            }
        ],
    ],
)
def test_unique_emails(
    groups_data: dict[str, CommentsDataType],
) -> None:
    emails = unique_emails(dict(groups_data), ())
    assert len(emails) == 9


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "finding_id",
    ],
    [
        [
            "422286126",
        ],
    ],
)
@freeze_time("2019-08-21T06:00:00.0")
async def test_finding_comments(
    finding_id: str,
) -> None:
    comments = await finding_comments(get_new_context(), finding_id)
    assert len(comments) == 1


@pytest.mark.parametrize(
    ["comments"],
    [
        [
            [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                + " Maecenas at tincidunt sapien. Ut vel ante augue. Vivamus"
                + " nisl felis, mollis vitae risus vel, faucibus tincidunt"
                + " nibh. Nunc pretium ut enim finibus mattis. Sed molestie"
                + " justo tortor, non convallis ligula bibendum at."
                + " Suspendisse augue odio, commodo quis sem et, lobortis"
                + " feugiat nisi. Vivamus fringilla auctor auctor. Nam"
                + " pellentesque, mauris et ultrices mollis, ipsum tellus"
                + " consectetur mauris, eu pharetra nisl nulla at elit. Nunc"
                + " facilisis est sed nibh ornare, non lobortis odio posuere."
                + " Donec finibus semper purus, ut facilisis lorem.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                + " Maecenas at tincidunt sapien. Ut vel ante augue. Vivamus"
                + " nisl felis, mollis vitae risus vel, faucibus tincidunt"
                + " nibh. Nunc pretium ut enim finibus mattis. Sed molestie"
                + " justo tortor, non convallis ligula bibendum at."
                + " Suspendisse augue odio, commodo quis sem et, lobortis"
                + " feugiat nisi. Vivamus fringilla auctor",
            ],
        ],
    ],
)
def test_format_comment(
    comments: list[str],
) -> None:
    assert len(format_comment(comments[0])) == 503
    assert len(format_comment(comments[1])) == 365


@pytest.mark.parametrize(
    ["items", "outputs"],
    [
        [
            [
                (
                    GroupComment(
                        group_name="unittesting",
                        id="1670952875435",
                        parent_id="0",
                        creation_date=datetime(
                            2022,
                            12,
                            13,
                            17,
                            34,
                            35,
                            434861,
                            tzinfo=UTC,
                        ),
                        content="Testing comment",
                        email="integratesuser2@testing.com",
                        full_name="Testing User",
                    ),
                ),
                (
                    EventComment(
                        event_id="141919677",
                        id="1670952924164",
                        parent_id="0",
                        creation_date=datetime(
                            2022,
                            12,
                            13,
                            17,
                            35,
                            24,
                            164124,
                            tzinfo=UTC,
                        ),
                        content="Testing comment",
                        email="integratesuser2@testing.com",
                        full_name="Testing User",
                    ),
                ),
                (
                    FindingComment(
                        comment_type=CommentType.COMMENT,
                        content="Testing comment",
                        creation_date=datetime(
                            2022,
                            12,
                            13,
                            17,
                            34,
                            15,
                            641328,
                            tzinfo=UTC,
                        ),
                        email="integratesuser2@testing.com",
                        finding_id="bcffefa2-91e4-48fc-ad7a-ea0840a3d47b",
                        id="1670952855641",
                        parent_id="0",
                        full_name="Testing User",
                    ),
                    FindingComment(
                        comment_type=CommentType.COMMENT,
                        content="Testing reply",
                        creation_date=datetime(
                            2022,
                            12,
                            13,
                            17,
                            34,
                            23,
                            70498,
                            tzinfo=UTC,
                        ),
                        email="integratesuser@fluidattacks.com",
                        finding_id="bcffefa2-91e4-48fc-ad7a-ea0840a3d47b",
                        id="1670952863070",
                        parent_id="1670952855641",
                        full_name="Testing User",
                    ),
                ),
            ],
            [
                [
                    {
                        "comment": "Testing comment",
                        "date": "2022-12-13 12:34",
                        "instance_id": None,
                        "name": "Testing User",
                    }
                ],
                [
                    {
                        "comment": "Testing comment",
                        "date": "2022-12-13 12:35",
                        "instance_id": None,
                        "name": "Testing User",
                    }
                ],
                [
                    {
                        "comment": "Testing comment",
                        "date": "2022-12-13 12:34",
                        "instance_id": "bcffefa2-91e4-48fc-ad7a-ea0840a3d47b",
                        "name": "Testing User",
                    },
                    {
                        "comment": "Testing reply",
                        "date": "2022-12-13 12:34",
                        "instance_id": "bcffefa2-91e4-48fc-ad7a-ea0840a3d47b",
                        "name": "Fluid Attacks",
                    },
                ],
            ],
        ],
    ],
)
def test_digest_comments(
    items: Any,
    outputs: Any,
) -> None:
    assert digest_comments(items[0]) == outputs[0]
    assert digest_comments(items[1]) == outputs[1]
    assert digest_comments(items[2]) == outputs[2]
