from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    GitCloningStatus,
)
import pytest
from roots import (
    domain as roots_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_root_id_by_nickname() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    group_roots_loader = loaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
    root_id = roots_domain.get_root_id_by_nickname(
        "universe", tuple(group_roots), only_git_roots=True
    )
    assert root_id == "4039d098-ffc5-4984-8ed3-eb17bca98e19"


async def test_get_last_cloning_successful() -> None:
    loaders = get_new_context()
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    item = await roots_domain.get_last_cloning_successful(loaders, root_id)
    assert item
    assert item.status == GitCloningStatus.OK
