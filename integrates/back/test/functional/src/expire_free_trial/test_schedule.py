# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    get_new_context,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers import (
    expire_free_trial,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("expire_free_trial")
@pytest.mark.parametrize(
    [
        "group_name",
        "email",
        "completed_before",
        "managed_before",
        "completed_after",
        "managed_after",
    ],
    [
        # Reached trial limit
        [
            "testgroup",
            "johndoe@fluidattacks.com",
            False,
            GroupManaged.TRIAL,
            True,
            GroupManaged.UNDER_REVIEW,
        ],
        # Still has remaining days
        [
            "testgroup2",
            "janedoe@fluidattacks.com",
            False,
            GroupManaged.TRIAL,
            False,
            GroupManaged.TRIAL,
        ],
    ],
)
@freeze_time("2022-11-11T15:58:31.280182")
async def test_expire_free_trial(
    *,
    populate: bool,
    group_name: str,
    email: str,
    completed_before: bool,
    managed_before: GroupManaged,
    completed_after: bool,
    managed_after: GroupManaged,
) -> None:
    assert populate
    loaders = get_new_context()

    enrollment_before: Enrollment = await loaders.enrollment.load(email)
    assert enrollment_before.trial.completed == completed_before
    group_before: Group = await loaders.group.load(group_name)
    assert group_before.state.managed == managed_before

    await expire_free_trial.main()
    loaders.enrollment.clear_all()
    loaders.group.clear_all()

    enrollment_after: Enrollment = await loaders.enrollment.load(email)
    assert enrollment_after.trial.completed == completed_after
    group_after: Group = await loaders.group.load(group_name)
    assert group_after.state.managed == managed_after
