from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce11",
        ),
    ),
)
async def test_confirm_vulnerabilities(
    populate: bool,
    email: str,
    vuln_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SUBMITTED

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" not in result
    assert result["data"]["confirmVulnerabilities"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
    ),
)
async def test_confirm_vulnerabilities_fail(
    populate: bool,
    email: str,
    vuln_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
