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
    ["email", "component", "entry_point", "be_present", "attacked_at"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "idTest",
            True,
            "2020-02-02T05:00:00+00:00",
        ],
    ],
)
async def test_update_toe_input(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    be_present: bool,
    attacked_at: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        attacked_at=attacked_at,
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateToeInput"]
    assert result["data"]["updateToeInput"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "be_present", "attacked_at"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "idTest",
            False,
            "2020-02-02T05:00:00+00:00",
        ],
    ],
)
async def test_update_toe_input_fail(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    be_present: bool,
    attacked_at: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        attacked_at=attacked_at,
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The toe input is not present"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "be_present", "attacked_at"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "idTest",
            True,
            "2018-02-02T05:00:00+00:00",
        ],
    ],
)
async def test_update_toe_input_fail_2(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    be_present: bool,
    attacked_at: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        attacked_at=attacked_at,
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The attack time must be between the previous attack "
        "and the current time"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "entry_point", "be_present", "attacked_at"],
    [
        [
            "user@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
            True,
            "2020-02-02T05:00:00+00:00",
        ],
        [
            "executive@gmail.com",
            "https://app.fluidattacks.com:8080/test",
            "-",
            True,
            "2020-02-02T05:00:00+00:00",
        ],
    ],
)
async def test_update_toe_input_fail_3(
    populate: bool,
    email: str,
    component: str,
    entry_point: str,
    be_present: bool,
    attacked_at: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        attacked_at=attacked_at,
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
