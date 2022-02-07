from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("enumerate_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "seen_first_time_by"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "idTest",
            "hacker@fluidattacks.com",
        ],
    ],
)
async def test_enumerate_toe_input(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    seen_first_time_by: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        seen_first_time_by=seen_first_time_by,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["enumerateToeInput"]
    assert result["data"]["enumerateToeInput"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("enumerate_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "seen_first_time_by"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1:8080",
            "btnTest",
            "architect@fluidattacks.com",
        ],
    ],
)
async def test_enumerate_toe_input_fail(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    seen_first_time_by: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        seen_first_time_by=seen_first_time_by,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The role is not valid for the user in seen first time "
        "by"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("enumerate_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "seen_first_time_by"],
    [
        [
            "admin@fluidattacks.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
            "hacker@fluidattacks.com",
        ],
    ],
)
async def test_enumerate_toe_input_fail_2(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    seen_first_time_by: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        seen_first_time_by=seen_first_time_by,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The toe input is already enumerated"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("enumerate_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "seen_first_time_by"],
    [
        [
            "customer@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
            "hacker@fluidattacks.com",
        ],
        [
            "executive@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
            "hacker@fluidattacks.com",
        ],
    ],
)
async def test_enumerate_toe_input_fail_3(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    seen_first_time_by: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        seen_first_time_by=seen_first_time_by,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
