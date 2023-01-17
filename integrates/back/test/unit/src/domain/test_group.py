from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
from findings.domain import (
    get_pending_verification_findings,
)
from group_comments.domain import (
    get_comments,
)
from groups.domain import (
    remove_pending_deletion_date,
    send_mail_devsecops_agent,
    set_pending_deletion_date,
)
from newutils.group_comments import (
    format_group_consulting_resolve,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_list_comments() -> None:
    group_name = "unittesting"
    test_data = await get_comments(get_new_context(), group_name, "admin")
    expected_output = GroupComment(
        group_name="unittesting",
        content="Now we can post comments on groups",
        parent_id="0",
        creation_date=datetime.fromisoformat("2018-12-27T21:30:28+00:00"),
        id="1545946228675",
        full_name="Miguel de Orellana",
        email="unittest@fluidattacks.com",
    )
    expected_output_to_resolve = {
        "content": "Now we can post comments on groups",
        "parent": "0",
        "created": "2018/12/27 16:30:28",
        "id": "1545946228675",
        "fullname": "Fluid Attacks",
        "email": "help@fluidattacks.com",
        "modified": "2018/12/27 16:30:28",
    }
    assert test_data[0] == expected_output

    assert (
        format_group_consulting_resolve(test_data[0])
        == expected_output_to_resolve
    )


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
    test_date = datetime.fromisoformat("2022-04-06T16:46:23+00:00")
    group: Group = await loaders.group.load(group_name)
    assert group.state.pending_deletion_date is None

    await set_pending_deletion_date(
        group=group, modified_by=user_email, pending_deletion_date=test_date
    )
    loaders.group.clear(group_name)
    group_updated: Group = await loaders.group.load(group_name)
    assert group_updated.state.pending_deletion_date is not None
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
