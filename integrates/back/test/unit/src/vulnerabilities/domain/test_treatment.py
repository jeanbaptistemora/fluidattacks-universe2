from dataloaders import (
    get_new_context,
)
import pytest
from vulnerabilities.domain import (
    get_managers_by_size,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.asyncio
async def test_get_managers_by_size() -> None:
    group_name = "unittesting"
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, 3
    )
    expected_len = 3
    assert expected_len == len(email_managers)
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, 2
    )
    expected_len = 2
    assert expected_len == len(email_managers)
