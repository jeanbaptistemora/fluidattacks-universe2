from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_vuln_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_download_vuln_file(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    finding_id: str = "475041513"
    result: Dict[str, Any] = await query(user=email, finding=finding_id)
    assert "errors" not in result
    assert result["data"]["downloadVulnFile"]["success"]
    assert "url" in result["data"]["downloadVulnFile"]
    assert (
        f"localhost:9000/fluidintegrates.reports/{group}-{finding_id}"
        in result["data"]["downloadVulnFile"]["url"]
    )
