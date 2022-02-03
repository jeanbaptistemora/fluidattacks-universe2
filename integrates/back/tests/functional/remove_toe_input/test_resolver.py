from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "idTest",
        ],
    ],
)
async def test_remove_toe_input(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeToeInput"]
    assert result["data"]["removeToeInput"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1:8080",
            "btnTest",
        ],
    ],
)
async def test_remove_toe_input_fail(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The toe input is already enumerated"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point"],
    [
        [
            "customer@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
        ],
        [
            "executive@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
        ],
    ],
)
async def test_remove_toe_input_fail_2(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
