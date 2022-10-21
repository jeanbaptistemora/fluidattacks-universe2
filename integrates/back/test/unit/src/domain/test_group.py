# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.group_comments.types import (
    GroupComment,
)
from db_model.groups.types import (
    Group,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_pending_verification_findings,
)
from freezegun import (
    freeze_time,
)
from group_comments.domain import (
    add_comment,
    get_comments,
)
from groups.domain import (
    get_mean_remediate_severity_cvssf,
    remove_pending_deletion_date,
    send_mail_devsecops_agent,
    set_pending_deletion_date,
)
from newutils.datetime import (
    convert_from_iso_str,
    is_valid_format,
)
from newutils.group_comments import (
    format_group_consulting_resolve,
)
import pytest
import time

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("376.001")),
        (30, Decimal("0")),
        (90, Decimal("82.000")),
    ),
)
async def test_get_mean_remediate_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    mean_remediate_cvssf = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        Decimal("0.0"),
        Decimal("10.0"),
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_cvssf == expected_output


async def test_list_comments() -> None:
    group_name = "unittesting"
    test_data = await get_comments(get_new_context(), group_name, "admin")
    expected_output = GroupComment(
        group_name="unittesting",
        content="Now we can post comments on groups",
        parent_id="0",
        creation_date="2018-12-27T21:30:28+00:00",
        id="1545946228675",
        full_name="Miguel de Orellana",
        email="unittest@fluidattacks.com",
    )
    expected_output_to_resolve = {
        "content": "Now we can post comments on groups",
        "parent": "0",
        "created": "2018/12/27 16:30:28",
        "id": "1545946228675",
        "fullname": "Miguel de Orellana at Fluid Attacks",
        "email": "unittest@fluidattacks.com",
        "modified": "2018/12/27 16:30:28",
    }
    assert test_data[0] == expected_output

    assert (
        format_group_consulting_resolve(test_data[0])
        == expected_output_to_resolve
    )


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
        comment_data,
    )
    loaders = get_new_context()
    group_comments: list[GroupComment] = await loaders.group_comments.load(
        group_name
    )
    assert group_comments[-1].content == "Test comment"
    assert group_comments[-1].id == comment_data.id
    assert group_comments[-1].full_name == comment_data.full_name


async def test_list_events() -> None:
    group_name = "unittesting"
    expected_output = [
        "418900971",
        "463578352",
        "484763304",
        "538745942",
        "540462628",
        "540462638",
    ]
    loaders: Dataloaders = get_new_context()
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    assert expected_output == sorted([event.id for event in events_group])


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("152.580")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
async def test_get_mean_remediate_severity_medium_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("4")
    max_severity = Decimal("6.9")
    mean_remediate_medium_severity = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_medium_severity == expected_output


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("364.485")),
        (30, Decimal("0.0")),
        (90, Decimal("82.0")),
    ),
)
async def test_get_mean_remediate_severity_low_cvssf(
    min_days: int, expected_output: Decimal
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    mean_remediate_low_severity = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime.now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_low_severity == expected_output


async def test_get_pending_verification_findings() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    findings = await get_pending_verification_findings(loaders, group_name)
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"


@pytest.mark.changes_db
async def test_set_pending_deletion_date() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    user_email = "integratesmanager@gmail.com"
    test_date = "2022-04-06T16:46:23+00:00"
    group: Group = await loaders.group.load(group_name)
    assert group.state.pending_deletion_date is None

    await set_pending_deletion_date(
        group=group, modified_by=user_email, pending_deletion_date=test_date
    )
    loaders.group.clear(group_name)
    group_updated: Group = await loaders.group.load(group_name)
    assert is_valid_format(
        convert_from_iso_str(
            group_updated.state.pending_deletion_date  # type: ignore
        )
    )
    assert group_updated.state.pending_deletion_date == test_date
    assert group_updated.state.modified_by == user_email


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "responsible",
        "had_token",
    ],
    [
        [
            "unittesting",
            "integratesmanager@gmail.com",
            True,
        ],
        [
            "unittesting",
            "integratesmanager@gmail.com",
            False,
        ],
    ],
)
async def test_send_mail_devsecops_agent(
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    await send_mail_devsecops_agent(
        loaders=get_new_context(),
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )


@pytest.mark.changes_db
async def test_clear_pending_deletion_date() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    user_email = "integratesmanager@gmail.com"
    group: Group = await loaders.group.load(group_name)
    assert group.state.pending_deletion_date

    await remove_pending_deletion_date(group=group, modified_by=user_email)
    loaders.group.clear(group_name)
    group_updated: Group = await loaders.group.load(group_name)
    assert group_updated.state.pending_deletion_date is None
    assert group_updated.state.modified_by == user_email
