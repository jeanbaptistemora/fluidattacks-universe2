from . import (
    get_result,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
async def test_should_mutate_successfully(populate: bool) -> None:
    assert populate
    result = await get_result(
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        source_group_name="kibi",
        target_group_name="kuri",
        user="test@fluidattacks.com",
    )
    assert "errors" not in result
    assert "success" in result["data"]["moveRoot"]
    assert result["data"]["moveRoot"]["success"]
