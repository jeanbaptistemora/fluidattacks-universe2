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
@freeze_time("2022-11-11T15:58:31.280182")
async def test_should_expire_group(populate: bool) -> None:
    assert populate
    loaders = get_new_context()
    group_name = "testgroup"
    email = "johndoe@fluidattacks.com"

    enrollment_before: Enrollment = await loaders.enrollment.load(email)
    assert enrollment_before.trial.completed is False
    group_before: Group = await loaders.group.load(group_name)
    assert group_before.state.managed == GroupManaged.TRIAL

    await expire_free_trial.main()
    loaders.enrollment.clear_all()
    loaders.group.clear_all()

    enrollment_after: Enrollment = await loaders.enrollment.load(email)
    assert enrollment_after.trial.completed is True
    group_after: Group = await loaders.group.load(group_name)
    assert group_after.state.managed == GroupManaged.UNDER_REVIEW
