# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_verification_vuln")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("analyst@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("closer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("customer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
    ),
)
async def test_request_verification_vuln(
    populate: bool, email: str, vuln_id: str
):
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await query(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert result["data"]["requestVerificationVuln"]["success"]
