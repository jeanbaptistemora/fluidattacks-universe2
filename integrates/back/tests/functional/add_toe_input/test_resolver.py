from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "https://test.com/test",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1:8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "https://app.fluidattacks.com:8080/test",
            "eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
        ],
    ],
)
async def test_add_toe_input(
    populate: bool,
    email: str,
    component: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    entry_point: str = "-"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addToeInput"]
    assert result["data"]["addToeInput"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "https://fail.com/test",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "https://app.fluidattacks.com:80/test",
            "eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
        ],
    ],
)
async def test_add_toe_input_fail(
    populate: bool,
    email: str,
    component: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    entry_point: str = "-"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The root does not have the component"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_input")
@pytest.mark.parametrize(
    ["email", "component", "root_id"],
    [
        [
            "customer@gmail.com",
            "https://test.com/test",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
        [
            "executive@gmail.com",
            "192.168.1.1:8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
    ],
)
async def test_add_toe_input_fail_2(
    populate: bool,
    email: str,
    component: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    entry_point: str = "-"
    result: Dict[str, Any] = await get_result(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
