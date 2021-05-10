# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
@pytest.mark.usefixtures("populate")
async def test_admin() -> None:
    result: Dict[str, Any] = await query(
        stakeholder="admin@gmail.com",
        vuln_id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
    )
    assert "errors" not in result
    assert result["data"]["updateVulnCommit"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
@pytest.mark.usefixtures("populate")
async def test_user() -> None:
    result: Dict[str, Any] = await query(
        stakeholder="someone-without-access@gmail.com",
        vuln_id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
    )
    assert "errors" in result
    assert result["errors"] == [
        {
            "locations": [{"column": 21, "line": 3}],
            "message": "Access denied",
            "path": ["updateVulnCommit"],
        },
    ]
