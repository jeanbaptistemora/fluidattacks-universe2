from . import (
    get_result_mutation,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["system_owner@gmail.com"],
    ],
)
async def test_remove_stakeholder(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result_mutation(
        user=email,
    )

    assert "errors" not in result
    assert result["data"]["removeStakeholder"]["success"]
