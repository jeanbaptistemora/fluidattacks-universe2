from . import (
    get_query,
    put_mutation,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_url_root")
async def test_should_mutate_successfully(populate: bool) -> None:
    assert populate

    group_name: str = "group123"
    root_id: str = "88637616-41d4-4242-854a-db8ff7fe1ab6"
    root = await get_query(
        group_name=group_name,
        root_id=root_id,
        user="test@fluidattacks.com",
    )
    assert root["data"]["root"]["host"] == "app.fluidattacks.com"
    assert root["data"]["root"]["nickname"] == "test_nickname_3"
    assert root["data"]["root"]["path"] == "/"
    assert root["data"]["root"]["state"] == "ACTIVE"

    result = await put_mutation(
        group_name=group_name,
        root_id=root_id,
        nickname="newtest",
        user="test@fluidattacks.com",
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateUrlRoot"]
    assert result["data"]["updateUrlRoot"]["success"]

    root_updated = await get_query(
        group_name=group_name,
        root_id=root_id,
        user="test@fluidattacks.com",
    )
    assert root_updated["data"]["root"]["nickname"] == "newtest"
    assert root_updated["data"]["root"]["state"] == "ACTIVE"
    assert root["data"]["root"]["host"] == "app.fluidattacks.com"
    assert root["data"]["root"]["path"] == "/"
