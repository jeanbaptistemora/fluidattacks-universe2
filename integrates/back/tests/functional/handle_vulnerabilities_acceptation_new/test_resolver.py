from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptation_new")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "customeradmin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "system_owner@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptation(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["handleVulnerabilitiesAcceptation"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptation_new")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptation_fail(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
