from groups import (
    domain as groups_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)
import pytest
from schedulers import (
    delete_obsolete_groups,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("delete_obsolete_groups")
async def test_get_group(populate: bool) -> None:
    assert populate
    group_attributes = {
        "project_name",
        "project_status",
        "pending_deletion_date",
    }
    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 3
    expected_groups = [
        {
            "project_status": "SUSPENDED",
            "group_name": "setpendingdeletion",
            "project_name": "setpendingdeletion",
        },
        {
            "group_name": "deletegroup",
            "project_name": "deletegroup",
            "project_status": "ACTIVE",
            "pending_deletion_date": "2020-12-22 14:36:29",
        },
    ]
    for expected_group in expected_groups:
        assert expected_group in alive_groups

    await delete_obsolete_groups.main()

    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 2
    groups = await groups_domain.get_all(group_attributes)
    setpendingdeletion = [
        group
        for group in groups
        if get_key_or_fallback(group) == "setpendingdeletion"
    ][0]
    assert setpendingdeletion["project_status"] == "SUSPENDED"
    assert "pending_deletion_date" in setpendingdeletion
    deletegroup = [
        group
        for group in groups
        if get_key_or_fallback(group) == "deletegroup"
    ][0]
    assert deletegroup["project_status"] == "DELETED"
