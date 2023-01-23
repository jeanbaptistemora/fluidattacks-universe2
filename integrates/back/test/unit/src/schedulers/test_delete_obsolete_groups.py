from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from schedulers import (
    delete_obsolete_groups,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_remove_obsolete_groups() -> None:
    loaders: Dataloaders = get_new_context()
    test_group_name_1 = "setpendingdeletion"
    test_group_name_2 = "deletegroup"
    all_active_groups_names = await orgs_domain.get_all_active_group_names(
        loaders
    )
    assert len(all_active_groups_names) == 14
    assert test_group_name_1 in all_active_groups_names
    assert test_group_name_2 in all_active_groups_names

    await delete_obsolete_groups.main()

    loaders = get_new_context()
    all_active_groups_names = await orgs_domain.get_all_active_group_names(
        loaders
    )
    assert len(all_active_groups_names) == 13
    assert test_group_name_1 in all_active_groups_names
    assert test_group_name_2 not in all_active_groups_names

    test_group_1: Group = await loaders.group.load(test_group_name_1)
    assert test_group_1.state.status == GroupStateStatus.ACTIVE
    assert test_group_1.state.pending_deletion_date

    with pytest.raises(GroupNotFound):
        await loaders.group.load(test_group_name_2)
