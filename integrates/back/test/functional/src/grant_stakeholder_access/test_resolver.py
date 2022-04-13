# pylint: disable=import-error
from . import (
    get_result,
    get_stakeholders,
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
    ["email", "stakeholder_email", "confirm"],
    [
        ["admin@gmail.com", "hacker@gmail.com", True],
        ["admin@gmail.com", "reattacker@gmail.com", False],
    ],
)
async def test_grant_stakeholder_access(
    populate: bool, email: str, stakeholder_email: str, confirm: bool
) -> None:
    assert populate
    group_name: str = "group2"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "EXECUTIVE"
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

    if confirm:
        await complete_register(stakeholder_email, group_name)
        stakeholders_after_confirm: dict[str, Any] = await get_stakeholders(
            user=email, group=group_name
        )

        assert "errors" not in stakeholders_after_confirm
        for stakeholder in stakeholders_after_confirm["data"]["group"][
            "stakeholders"
        ]:
            if stakeholder["email"] == stakeholder_email:
                assert stakeholder["invitationState"] == "CONFIRMED"
    else:
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
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_grant_stakeholder_access_fail(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group2"
    stakeholder_email: str = "hacker@gmail.com"
    stakeholder_responsibility: str = "test"
    stakeholder_role: str = "EXECUTIVE"
    result: dict[str, Any] = await get_result(
        user=email,
        stakeholder=stakeholder_email,
        group=group_name,
        responsibility=stakeholder_responsibility,
        role=stakeholder_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
