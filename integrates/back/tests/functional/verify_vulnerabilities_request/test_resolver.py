from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_request_vulnerabilities_verification(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]
