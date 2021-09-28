from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 10),),
)
async def test_get_organization_ver_1(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_stakeholders: List[str] = [
        "admin@gmail.com",
        "customer@gmail.com",
        "customeradmin@gmail.com",
        "executive@gmail.com",
        "hacker@gmail.com",
        "reattacker@gmail.com",
        "resourcer@gmail.com",
        "reviewer@gmail.com",
        "system_owner@gmail.com",
    ]
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, group=group_name
    )
    groups: List[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: List[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptations"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == []
    assert sorted(stakeholders) == org_stakeholders
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (
        ("customer@gmail.com", "customer", 0),
        ("customeradmin@gmail.com", "customeradmin", 0),
        ("executive@gmail.com", "executive", 0),
        ("hacker@gmail.com", "hacker", 0),
        ("reattacker@gmail.com", "reattacker", 0),
        ("resourcer@gmail.com", "resourcer", 0),
        ("reviewer@gmail.com", "reviewer", 0),
        ("system_owner@gmail.com", "system_owner", 0),
    ),
)
async def test_get_organization_ver_2(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_groups: List[str] = [
        "group1",
    ]
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, org=org_id, group=group_name
    )
    groups: List[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptations"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == org_groups
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role
