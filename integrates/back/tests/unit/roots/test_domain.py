from dataloaders import (
    get_new_context,
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
    root_id = roots_domain.get_root_id_by_nickname("product", group_roots)
    assert root_id == "4039d098-ffc5-4984-8ed3-eb17bca98e19"
