from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import pytest
from vulnerabilities.domain import (
    get_reattack_requester,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_reattack_requester() -> None:
    loaders = get_new_context()
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        "3bcdb384-5547-4170-a0b6-3b397a245465"
    )
    requester = await get_reattack_requester(
        loaders,
        vuln=vulnerability,
    )
    assert requester == "integratesuser@gmail.com"
