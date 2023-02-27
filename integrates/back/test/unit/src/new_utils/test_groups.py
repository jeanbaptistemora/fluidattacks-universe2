from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from newutils.groups import (
    filter_active_groups,
)
import pytest


@pytest.mark.parametrize(
    ["managed", "status", "expected"],
    [
        # Active
        (GroupManaged.MANAGED, GroupStateStatus.ACTIVE, True),
        # Inactive
        (GroupManaged.MANAGED, GroupStateStatus.DELETED, False),
    ],
)
def test_filter_active_groups(
    managed: GroupManaged, status: GroupStateStatus, expected: bool
) -> None:
    group = Group(
        created_by="johndoe@fluidattacks.com",
        created_date=datetime.fromisoformat(
            "2022-10-21T15:58:31.280182+00:00"
        ),
        description="test description",
        language=GroupLanguage.EN,
        name="testgroup",
        organization_id="",
        state=GroupState(
            has_machine=True,
            has_squad=False,
            managed=managed,
            modified_by="johndoe@fluidattacks.com",
            modified_date=datetime.fromisoformat(
                "2022-10-21T15:58:31.280182+00:00"
            ),
            service=GroupService.WHITE,
            status=status,
            tier=GroupTier.FREE,
            type=GroupSubscriptionType.CONTINUOUS,
        ),
    )
    filtered = filter_active_groups([group])
    assert bool(filtered) == expected
