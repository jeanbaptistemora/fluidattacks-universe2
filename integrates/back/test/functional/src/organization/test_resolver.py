# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from . import (
    get_result,
    get_vulnerabilities_url,
)
from back.test.functional.src.remove_stakeholder_access import (
    get_access_token,
)
from custom_exceptions import (
    RequiredVerificationCode,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest
from typing import (
    Any,
    Optional,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 12),),
)
async def test_get_organization_ver_1(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_stakeholders: list[str] = [
        "admin@fluidattacks.com",
        "admin@gmail.com",
        "architect@fluidattacks.com",
        "architect@gmail.com",
        "customer_manager@fluidattacks.com",
        "hacker@fluidattacks.com",
        "hacker@gmail.com",
        "reattacker@fluidattacks.com",
        "reattacker@gmail.com",
        "resourcer@fluidattacks.com",
        "resourcer@gmail.com",
        "reviewer@fluidattacks.com",
        "reviewer@gmail.com",
        "service_forces@fluidattacks.com",
        "user@fluidattacks.com",
        "user@gmail.com",
        "user_manager@fluidattacks.com",
        "user_manager@gmail.com",
        "vulnerability_manager@fluidattacks.com",
        "vulnerability_manager@gmail.com",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
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
        ("user@gmail.com", "user", 3),
        ("user_manager@gmail.com", "user_manager", 23),
        ("vulnerability_manager@gmail.com", "user", 3),
        ("hacker@gmail.com", "user", 3),
        ("reattacker@gmail.com", "user", 3),
        ("resourcer@gmail.com", "user", 3),
        ("reviewer@gmail.com", "user", 3),
        ("customer_manager@fluidattacks.com", "customer_manager", 26),
    ),
)
async def test_get_organization_ver_2(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_groups: list[str] = [
        "group1",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == org_groups
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 12),),
)
async def test_get_organization_default_values(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    org_name: str = "acme"
    org_stakeholders: list[str] = [
        "admin@gmail.com",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] is None
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 10.0
    assert result["data"]["organization"]["maxNumberAcceptances"] is None
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 0.0
    assert result["data"]["organization"]["minBreakingSeverity"] == 0.0
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 0
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == []
    assert sorted(stakeholders) == org_stakeholders
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (
        ("admin@gmail.com", None),
        ("admin@gmail.com", "123123"),
    ),
)
async def test_get_org_vulnerabilities_url(
    populate: bool, email: str, verification_code: Optional[str]
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    if verification_code:
        assert "errors" not in result
        assert (
            result["data"]["organization"]["vulnerabilitiesUrl"]
            == "https://test.com"
        )
    else:
        assert "errors" in result
        assert result["errors"][0]["message"] == str(
            RequiredVerificationCode()
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (("admin@gmail.com", None),),
)
async def test_get_org_vulnerabilities_url_api(
    populate: bool, email: str, verification_code: Optional[str]
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result_1: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    assert "errors" in result_1
    assert result_1["errors"][0]["message"] == str(RequiredVerificationCode())

    ts_expiration_time: int = int(
        (datetime.utcnow() + timedelta(weeks=8)).timestamp()
    )
    result_jwt = await get_access_token(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result_jwt
    assert result_jwt["data"]["updateAccessToken"]["success"]

    session_jwt: str = result_jwt["data"]["updateAccessToken"]["sessionJwt"]
    result_2: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=session_jwt,
    )

    assert "errors" not in result_2
    assert (
        result_2["data"]["organization"]["vulnerabilitiesUrl"]
        == "https://test.com"
    )
