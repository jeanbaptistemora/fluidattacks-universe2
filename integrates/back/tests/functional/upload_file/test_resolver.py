from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)


async def _get_vulns(finding_id: str) -> List[Dict[str, Any]]:
    return sorted(
        (
            dict(
                commit_hash=vuln.get("commit_hash", None),
                repo_nickname=vuln.get("repo_nickname", ""),
                specific=vuln.get("specific", ""),
                stream=vuln.get("stream", None),
                type=vuln.get("vuln_type", ""),
                where=vuln.get("where", ""),
            )
            for vuln in await vulns_dal.get_by_finding(finding_id)
        ),
        key=str,
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_upload_file(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(user=email, finding=finding_id)
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]
    assert await _get_vulns(finding_id) == [
        {
            "commit_hash": "111111111111111111111111111111111111111f",
            "repo_nickname": "product",
            "specific": "1",
            "stream": None,
            "type": "lines",
            "where": "product/test/1",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "product",
            "specific": "123",
            "stream": None,
            "type": "lines",
            "where": "product/path/to/file1.ext",
        },
        {
            "commit_hash": "e17059d1e17059d1e17059d1e17059d1e17059d1",
            "repo_nickname": "product",
            "specific": "345",
            "stream": None,
            "type": "lines",
            "where": "product/path/to/file3.ext",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "phone",
            "stream": "home,blog,articulo",
            "type": "inputs",
            "where": "https://example.com",
        },
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_upload_file_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(user=email, finding=finding_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
