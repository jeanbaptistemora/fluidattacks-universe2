# Third party libraries
import pytest

# Local libraries
from backend.api import get_new_context
from newutils import (
    roots as roots_utils,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_root_id_by_filename():
    loaders = get_new_context()
    group_name = 'unittesting'
    group_roots_loader = loaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
    root_id = roots_utils.get_root_id_by_filename(
        'product/integrates/test.config.json',
        group_roots
    )
    assert root_id == '4039d098-ffc5-4984-8ed3-eb17bca98e19'
