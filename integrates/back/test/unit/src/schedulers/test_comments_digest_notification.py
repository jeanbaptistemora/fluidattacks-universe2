from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
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
from schedulers.comments_digest_notification import (
    _get_days_since_comment,
    CommentsDataType,
    group_comments,
    group_instance_comments,
    instance_comments,
    last_comments,
    unique_emails,
)
from typing import (
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
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    comments = await group_instance_comments(
        loaders, group_findings, instance_type
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
async def test_unique_emails(
    groups_data: dict[str, CommentsDataType],
) -> None:
    emails = unique_emails(dict(groups_data), ())
    assert len(emails) == 9
