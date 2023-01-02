from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
@pytest.mark.resolver_test_group("get_organization_finding_policy")
async def test_get_organization_finding_policy(
    populate: bool,
    email: str,
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    policy_id: str = "3be367f9-b06c-4f72-ab77-38268045a8ff"
    name = "009. Sensitive information in source code"
    result: dict[str, Any] = await get_result(
        email=email, organization_id=org_id
    )

    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert len(result["data"]["organization"]["findingPolicies"]) == 3
    assert (
        result["data"]["organization"]["findingPolicies"][0]["id"] == policy_id
    )
    assert result["data"]["organization"]["findingPolicies"][0]["name"] == name
    assert (
        result["data"]["organization"]["findingPolicies"][0]["status"]
        == "APPROVED"
    )
