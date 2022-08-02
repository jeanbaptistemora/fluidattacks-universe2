from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    get_new_context,
)
from findings.domain import (
    has_access_to_finding,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_has_access_to_finding() -> None:
    loaders = get_new_context()
    wrong_data = ["unittest@fluidattacks.com", "000000000"]
    right_data = ["unittest@fluidattacks.com", "560175507"]
    with pytest.raises(FindingNotFound):
        await has_access_to_finding(loaders, wrong_data[0], wrong_data[1])
    assert await has_access_to_finding(loaders, right_data[0], right_data[1])
