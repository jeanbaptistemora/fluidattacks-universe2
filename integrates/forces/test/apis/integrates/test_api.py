from forces.apis.integrates.api import (
    get_findings,
    get_groups_access,
    get_vulnerabilities,
)
from forces.apis.integrates.client import (
    ApiError,
)
from forces.model import (
    ForcesConfig,
)
import pytest


@pytest.mark.asyncio
async def test_get_findings(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    result = await get_findings(test_group, api_token=test_token)
    assert test_finding in result[0]["id"]


@pytest.mark.asyncio
async def test_get_vulnerabilities(
    test_token: str, test_config: ForcesConfig
) -> None:
    result = await get_vulnerabilities(test_config, api_token=test_token)
    assert len(result) == 36
    assert "192.168.100.103" in result[0]["where"]


@pytest.mark.asyncio
async def test_get_group_access() -> None:
    try:
        await get_groups_access(api_token="bad_token")
    except ApiError as exc:
        assert (
            "Login required" in exc.messages
            or "Token format unrecognized" in exc.messages
        )
