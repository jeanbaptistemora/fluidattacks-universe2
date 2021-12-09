from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


async def _get_vulns(
    loaders: Dataloaders, finding_id: str
) -> List[Dict[str, Any]]:
    finding_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_typed.load(finding_id)
    return sorted(
        (
            dict(
                commit_hash=vuln.commit,
                repo_nickname=vuln.repo,
                specific=vuln.specific,
                state_status=vuln.state.status.value,
                stream=vuln.stream,
                treatment_status=vuln.treatment.status.value
                if vuln.treatment
                else None,
                type=vuln.type.value,
                verification_status=vuln.verification.status.value
                if vuln.verification
                else None,
                where=vuln.where,
            )
            for vuln in finding_vulns
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
    loaders: Dataloaders = get_new_context()
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(user=email, finding=finding_id)
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]
    assert await _get_vulns(loaders, finding_id) == [
        {
            "commit_hash": "111111111111111111111111111111111111111f",
            "repo_nickname": "product",
            "specific": "1",
            "state_status": "OPEN",
            "stream": None,
            "treatment_status": "NEW",
            "type": "LINES",
            "verification_status": None,
            "where": "product/test/1",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "product",
            "specific": "123",
            "state_status": "OPEN",
            "stream": None,
            "treatment_status": "NEW",
            "type": "LINES",
            "verification_status": None,
            "where": "product/path/to/file1.ext",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "4444",
            "state_status": "OPEN",
            "stream": None,
            "treatment_status": "NEW",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.44",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "4545",
            "state_status": "CLOSED",
            "stream": None,
            "treatment_status": "NEW",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.45",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "4646",
            "state_status": "CLOSED",
            "stream": None,
            "treatment_status": "NEW",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.46",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "4646",
            "state_status": "OPEN",
            "stream": None,
            "treatment_status": "NEW",
            "type": "PORTS",
            "verification_status": None,
            "where": "192.168.1.46",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "8080",
            "state_status": "OPEN",
            "stream": None,
            "treatment_status": "NEW",
            "type": "PORTS",
            "verification_status": None,
            "where": "https://example.com",
        },
        {
            "commit_hash": None,
            "repo_nickname": "product",
            "specific": "phone",
            "state_status": "OPEN",
            "stream": ["home", "blog", "articulo"],
            "treatment_status": "NEW",
            "type": "INPUTS",
            "verification_status": None,
            "where": "https://example.com",
        },
    ]

    escaper_vuln: Vulnerability = next(
        vuln
        for vuln in await loaders.finding_vulns_typed.load(finding_id)
        if vuln.specific == "4646"
        and vuln.where == "192.168.1.46"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    assert escaper_vuln.state.source == Source.ESCAPE
    assert escaper_vuln.state.modified_by == "escaper@gmail.com"


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
