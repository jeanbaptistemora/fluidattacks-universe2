from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    get_new_context,
)
from events.domain import (
    has_access_to_event,
)
from findings.domain import (
    has_access_to_finding,
)
import pytest
from users.domain import (
    has_valid_access_token,
)

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


async def test_has_access_to_event() -> None:
    assert await has_access_to_event("unittest@fluidattacks.com", "418900971")


async def test_has_valid_access_token() -> None:
    jti = "ff6273146a0e4ed82715cdb4db7f5915b30dfa4bccc54c0d2cda17a61a44a5f6"
    assert await has_valid_access_token(
        "unittest@fluidattacks.com",
        {"test_context": "test_context_value"},
        jti,
    )
