from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_side_effects,
)
from custom_exceptions import (
    GroupNotFound,
)
from db_model.groups.get import (
    GroupLoader,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["group_name", "group_name_bad"],
    [["unittesting", "does-not-exist"]],
)
@patch(MODULE_AT_TEST + "_get_group", new_callable=AsyncMock)
async def test_grouploader(
    mock__get_group: AsyncMock,
    group_name: str,
    group_name_bad: str,
) -> None:
    assert set_mocks_side_effects(
        mocks_args=[[group_name, group_name_bad]],
        mocked_objects=[mock__get_group],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_get_group"],
    )
    group = GroupLoader()
    assert isinstance(group, GroupLoader)
    test_group = await group.load(group_name)
    assert test_group.name is group_name
    assert mock__get_group.called is True
    with pytest.raises(GroupNotFound):
        await group.load(group_name_bad)
    assert mock__get_group.called is True
