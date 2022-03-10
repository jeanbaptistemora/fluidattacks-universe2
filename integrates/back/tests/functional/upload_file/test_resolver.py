from . import (
    get_result,
)
from custom_exceptions import (
    InvalidNewVulnState,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    Finding,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from freezegun import (  # type: ignore
    freeze_time,
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
    ] = await loaders.finding_vulnerabilities.load(finding_id)
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
@freeze_time("2022-02-09")
async def test_upload_file(populate: bool, email: str) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
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
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.specific == "4646"
        and vuln.where == "192.168.1.46"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    assert escaper_vuln.state.source == Source.ESCAPE
    assert escaper_vuln.state.modified_by == "escaper@gmail.com"

    vuln_loader = loaders.vulnerability
    open_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    vuln_open_verified: Vulnerability = await vuln_loader.load(
        open_verified_id
    )
    assert (
        vuln_open_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_efficacy=Decimal("0"),
            unreliable_last_reattack_date="2022-02-09T00:00:00+00:00",
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date="2018-04-08T01:45:11"
            "+00:00",
            unreliable_reattack_cycles=None,
            unreliable_report_date="2018-04-08T00:43:11+00:00",
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )
    closed_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce9"
    vuln_closed_verified: Vulnerability = await vuln_loader.load(
        closed_verified_id
    )
    assert (
        vuln_closed_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_efficacy=Decimal("100"),
            unreliable_last_reattack_date="2022-02-09T00:00:00+00:00",
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date="2018-04-08T01:45:11"
            "+00:00",
            unreliable_reattack_cycles=None,
            unreliable_report_date="2018-04-08T00:44:11+00:00",
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )

    finding: Finding = await loaders.finding.load(finding_id)
    assert finding.unreliable_indicators == FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=2,
        unreliable_is_verified=True,
        unreliable_newest_vulnerability_report_date="2022-02-09T00:00:00"
        "+00:00",
        unreliable_oldest_open_vulnerability_report_date="2018-04-08T"
        "00:45:11+00:00",
        unreliable_oldest_vulnerability_report_date="2018-04-08T00:45:11"
        "+00:00",
        unreliable_open_vulnerabilities=6,
        unreliable_status=FindingStatus.OPEN,
        unreliable_treatment_summary=FindingTreatmentSummary(
            accepted=0, accepted_undefined=0, in_progress=0, new=6
        ),
        unreliable_where="192.168.1.44, 192.168.1.46, https://example.com, "
        "product/path/to/file1.ext, product/test/1",
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_upload_file_access_denied_error(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


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
async def test_upload_new_closed_error(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns-new-closed-error.yaml"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidNewVulnState.msg
