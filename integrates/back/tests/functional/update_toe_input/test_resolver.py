from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "root_id", "component", "entry_point", "be_present"],
    [
        [
            "admin@fluidattacks.com",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "https://test.com/test",
            "idTest",
            True,
        ],
        [
            "admin@fluidattacks.com",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "https://test.com/test",
            "idTest",
            False,
        ],
    ],
)
async def test_update_toe_input(
    populate: bool,
    email: str,
    root_id: str,
    component: str,
    entry_point: str,
    be_present: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateToeInput"]
    assert result["data"]["updateToeInput"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "root_id", "component", "entry_point", "be_present"],
    [
        [
            "user@gmail.com",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "https://app.fluidattacks.com:8080/test",
            "-",
            True,
        ],
        [
            "executive@gmail.com",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "https://app.fluidattacks.com:8080/test",
            "-",
            True,
        ],
    ],
)
async def test_update_toe_input_fail_3(
    populate: bool,
    email: str,
    root_id: str,
    component: str,
    entry_point: str,
    be_present: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
