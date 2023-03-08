from dataloaders import (
    get_new_context,
)
from db_model.groups.enums import (
    GroupManaged,
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
async def test_expire_free_trial(*, populate: bool) -> None:
    assert populate
    loaders = get_new_context()
    cases = [
        # Reached trial limit
        {
            "email": "johndoe@johndoe.com",
            "group_name": "testgroup",
            "completed_before": False,
            "managed_before": GroupManaged.TRIAL,
            "completed_after": True,
            "managed_after": GroupManaged.UNDER_REVIEW,
        },
        # Still has remaining days
        {
            "email": "janedoe@janedoe.com",
            "group_name": "testgroup2",
            "completed_before": False,
            "managed_before": GroupManaged.TRIAL,
            "completed_after": False,
            "managed_after": GroupManaged.TRIAL,
        },
        # Reached trial limit but was granted an extension
        {
            "email": "uiguaran@uiguaran.com",
            "group_name": "testgroup3",
            "completed_before": False,
            "managed_before": GroupManaged.TRIAL,
            "completed_after": False,
            "managed_after": GroupManaged.TRIAL,
        },
        # Has already completed the trial
        {
            "email": "abuendia@abuendia.com",
            "group_name": "testgroup4",
            "completed_before": True,
            "managed_before": GroupManaged.MANAGED,
            "completed_after": True,
            "managed_after": GroupManaged.MANAGED,
        },
    ]

    for case in cases:
        trial_before = await loaders.trial.load(str(case["email"]))
        group_before = await loaders.group.load(str(case["group_name"]))
        assert trial_before
        assert group_before
        assert trial_before.completed == case["completed_before"]
        assert group_before.state.managed == case["managed_before"]

    await expire_free_trial.main()
    loaders.trial.clear_all()
    loaders.group.clear_all()

    for case in cases:
        trial_after = await loaders.trial.load(str(case["email"]))
        group_after = await loaders.group.load(str(case["group_name"]))
        assert trial_after
        assert group_after
        assert trial_after.completed == case["completed_after"]
        assert group_after.state.managed == case["managed_after"]
