from . import (
    get_result,
    get_vulnerability,
)
from dataloaders import (
    vulnerability,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_request_vuln")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("analyst@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("closer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_verify_vulnerabilities_open(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        open_vulnerabilities=[vuln_id],
        closed_vulnerabilities=[],
    )
    assert "errors" not in result
    assert result["data"]["verifyRequestVulnerabilities"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_request_vuln")
@pytest.mark.parametrize(
    ("email", "closed_vulnerability"),
    (("analyst@gmail.com", "fa4f847d-f76e-4a70-8942-0ddd183bf1b9"),),
)
async def test_verify_vulnerabilities_closed(
    populate: bool,
    email: str,
    closed_vulnerability: str,
) -> None:
    assert populate
    finding_id: str = "475041513"
    vulnerability_result: Dict[str, Any] = await get_vulnerability(
        user=email, vulnerability_id=closed_vulnerability
    )
    assert "errors" not in vulnerability_result
    assert (
        vulnerability_result["data"]["vulnerability"]["currentState"] == "open"
    )
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        open_vulnerabilities=[],
        closed_vulnerabilities=[closed_vulnerability],
    )
    assert "errors" not in result
    assert result["data"]["verifyRequestVulnerabilities"]["success"]

    vulnerability_result: Dict[str, Any] = await get_vulnerability(
        user=email, vulnerability_id=closed_vulnerability
    )
    assert "errors" not in vulnerability_result
    assert (
        vulnerability_result["data"]["vulnerability"]["currentState"]
        == "closed"
    )
