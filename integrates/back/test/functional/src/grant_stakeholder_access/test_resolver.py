# pylint: disable=import-error
from . import (
    get_group_data,
    get_result,
    get_stakeholders,
)
from asyncio import (
    sleep,
)
from back.test.functional.src.utils import (
    complete_register,
    reject_register,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email", "stakeholder_email"],
    [
        ["admin@gmail.com", "hacker1@gmail.com"],
    ],
)
async def test_grant_stakeholder_access_confirmed(
    populate: bool, email: str, stakeholder_email: str
) -> None:
    assert populate
    group_name: str = "group13"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "USER"
    await sleep(8)

    result: dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" not in result
    assert result["data"]["grantStakeholderAccess"]["success"]
    assert "success" in result["data"]["grantStakeholderAccess"]
    assert (
        result["data"]["grantStakeholderAccess"]["grantedStakeholder"]["email"]
        == stakeholder_email
    )

    stakeholders: dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )

    assert "errors" not in stakeholders
    for stakeholder in stakeholders["data"]["group"]["stakeholders"]:
        if stakeholder["email"] == stakeholder_email:
            assert stakeholder["invitationState"] == "PENDING"

    group_data: dict = await get_group_data(
        user=stakeholder_email, group=group_name
    )
    assert "errors" in group_data
    assert group_data["errors"][0]["message"] == "Access denied"

    await complete_register(stakeholder_email, group_name)

    stakeholders_after_confirm: dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )

    assert "errors" not in stakeholders_after_confirm
    for stakeholder in stakeholders_after_confirm["data"]["group"][
        "stakeholders"
    ]:
        if stakeholder["email"] == stakeholder_email:
            assert stakeholder["invitationState"] == "REGISTERED"

    group_data = await get_group_data(user=stakeholder_email, group=group_name)
    assert "errors" not in group_data
    assert len(group_data["data"]["group"]["vulnerabilities"]["edges"]) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email", "stakeholder_email"],
    [
        ["admin@gmail.com", "reattacker@gmail.com"],
    ],
)
async def test_grant_stakeholder_access_rejected(
    populate: bool, email: str, stakeholder_email: str
) -> None:
    assert populate
    group_name: str = "group13"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" not in result
    assert result["data"]["grantStakeholderAccess"]["success"]
    assert (
        result["data"]["grantStakeholderAccess"]["grantedStakeholder"]["email"]
        == stakeholder_email
    )

    stakeholders: dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )

    assert "errors" not in stakeholders
    for stakeholder in stakeholders["data"]["group"]["stakeholders"]:
        if stakeholder["email"] == stakeholder_email:
            assert stakeholder["invitationState"] == "PENDING"

    await reject_register(stakeholder_email, group_name)
    stakeholders_after_reject: dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )

    assert "errors" not in stakeholders_after_reject
    for stakeholder in stakeholders_after_reject["data"]["group"][
        "stakeholders"
    ]:
        if stakeholder["email"] == stakeholder_email:
            assert stakeholder["invitationState"] == "REJECTED"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email", "stakeholder_email"],
    [
        ["admin@gmail.com", "hacker1@gmail.com"],
        ["admin@gmail.com", "user@gmail.com"],
        ["admin@gmail.com", "vulnerability_manager@gmail.com"],
    ],
)
async def test_grant_stakeholder_access_fail_1(
    populate: bool, email: str, stakeholder_email: str
) -> None:
    assert populate
    group_name: str = "group13"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "HACKER"
    exceptions = {
        "Exception - Groups with any active Fluid Attacks service "
        "can only have Hackers provided by Fluid Attacks",
        "Exception - The stakeholder has been granted access "
        "to the group previously",
    }
    result: dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] in exceptions


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker1@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_grant_stakeholder_access_fail_2(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group13"
    stakeholder_email: str = "hacker1@gmail.com"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
