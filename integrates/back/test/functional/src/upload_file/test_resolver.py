from . import (
    get_group_vulnerabilities,
    get_result,
    update_services,
)
import asyncio
from custom_exceptions import (
    InvalidCannotModifyNicknameWhenClosing,
    InvalidNewVulnState,
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerificationSummary,
)
from db_model.groups.enums import (
    GroupSubscriptionType,
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
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
)


def _get_key(item: dict) -> str:
    return item["node"]["where"]


async def _get_vulns(
    loaders: Dataloaders,
    finding_id: str,
    group_name: str,
) -> list[dict[str, Any]]:
    finding_vulns = await loaders.finding_vulnerabilities.load(finding_id)
    roots = await loaders.group_roots.load(group_name)
    roots_nickname: dict[str, str] = {
        root.id: root.state.nickname for root in roots
    }
    return sorted(
        (
            dict(
                commit_hash=vuln.state.commit,
                repo_nickname=roots_nickname[vuln.root_id or ""],
                specific=vuln.state.specific,
                state_status=vuln.state.status.value,
                stream=vuln.stream,
                treatment_status=vuln.treatment.status.value
                if vuln.treatment
                else None,
                type=vuln.type.value,
                verification_status=vuln.verification.status.value
                if vuln.verification
                else None,
                where=vuln.state.where,
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
async def test_upload_file(
    # pylint: disable=too-many-locals
    populate: bool,
    email: str,
) -> None:
    assert populate
    loaders = get_new_context()
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    with freeze_time("2022-02-09"):
        result: dict[str, Any] = await get_result(
            user=email,
            finding=finding_id,
            yaml_file_name=file_name,
        )
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]
    assert await _get_vulns(loaders, finding_id, "group1") == [
        {
            "commit_hash": "111111111111111111111111111111111111111f",
            "repo_nickname": "universe",
            "specific": "1",
            "state_status": "VULNERABLE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "test/1",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "universe",
            "specific": "123",
            "state_status": "VULNERABLE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "path/to/file1.ext",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe",
            "specific": "phone",
            "state_status": "VULNERABLE",
            "stream": ["home", "blog", "articulo"],
            "treatment_status": "UNTREATED",
            "type": "INPUTS",
            "verification_status": None,
            "where": "https://example.com",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe44",
            "specific": "4444",
            "state_status": "VULNERABLE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.44",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe45",
            "specific": "4545",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.45",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe46",
            "specific": "4646",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.46",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe46",
            "specific": "4646",
            "state_status": "VULNERABLE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": None,
            "where": "192.168.1.46",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe47",
            "specific": "4747",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": None,
            "where": "192.168.1.47",
        },
    ]
    expected_group_vulns = sorted(
        [
            {
                "node": {
                    "currentState": "open",
                    "state": "VULNERABLE",
                    "treatment": "NEW",
                    "treatmentStatus": "UNTREATED",
                    "where": "universe/path/to/file1.ext",
                }
            },
            {
                "node": {
                    "currentState": "open",
                    "state": "VULNERABLE",
                    "treatment": "NEW",
                    "treatmentStatus": "UNTREATED",
                    "where": "universe/test/1",
                }
            },
            {
                "node": {
                    "currentState": "open",
                    "state": "VULNERABLE",
                    "treatment": "NEW",
                    "treatmentStatus": "UNTREATED",
                    "where": "192.168.1.44",
                }
            },
            {
                "node": {
                    "currentState": "open",
                    "state": "VULNERABLE",
                    "treatment": "NEW",
                    "treatmentStatus": "UNTREATED",
                    "where": "https://example.com",
                }
            },
            {
                "node": {
                    "currentState": "open",
                    "state": "VULNERABLE",
                    "treatment": "NEW",
                    "treatmentStatus": "UNTREATED",
                    "where": "192.168.1.46",
                }
            },
        ],
        key=_get_key,
    )
    await asyncio.sleep(8)
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1",
        state_status="VULNERABLE",
    )
    assert "errors" not in group_vulns
    assert (
        sorted(
            group_vulns["data"]["group"]["vulnerabilities"]["edges"],
            key=_get_key,
        )
        == expected_group_vulns
    )

    escaper_vuln: Vulnerability = next(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "4646"
        and vuln.state.where == "192.168.1.46"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    assert escaper_vuln.state.source == Source.ESCAPE

    vuln_loader = loaders.vulnerability
    open_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    vuln_open_verified = await vuln_loader.load(open_verified_id)
    assert vuln_open_verified
    assert (
        vuln_open_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_efficacy=Decimal("0"),
            unreliable_last_reattack_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date=(
                datetime.fromisoformat("2018-04-08T01:45:11+00:00")
            ),
            unreliable_reattack_cycles=None,
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )
    closed_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce9"
    vuln_closed_verified = await vuln_loader.load(closed_verified_id)
    assert vuln_closed_verified
    assert (
        vuln_closed_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_closing_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_efficacy=Decimal("100"),
            unreliable_last_reattack_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date=(
                datetime.fromisoformat("2018-04-08T01:45:11+00:00")
            ),
            unreliable_reattack_cycles=None,
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )
    changed_source_id = "be09edb7-cd5c-47ed-bee4-97c645acdceb"
    vuln_changed_source = await vuln_loader.load(changed_source_id)
    assert vuln_changed_source
    assert vuln_changed_source.state.source == Source.ANALYST

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.unreliable_indicators == FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=3,
        unreliable_newest_vulnerability_report_date=(
            datetime.fromisoformat("2022-02-09T00:00:00+00:00")
        ),
        unreliable_oldest_open_vulnerability_report_date=(
            datetime.fromisoformat("2018-04-08T00:43:11+00:00")
        ),
        unreliable_oldest_vulnerability_report_date=(
            datetime.fromisoformat("2018-04-08T00:43:11+00:00")
        ),
        unreliable_open_vulnerabilities=5,
        unreliable_status=FindingStatus.VULNERABLE,
        unreliable_treatment_summary=FindingTreatmentSummary(
            accepted=0, accepted_undefined=0, in_progress=0, untreated=5
        ),
        unreliable_verification_summary=FindingVerificationSummary(
            requested=0, on_hold=0, verified=1
        ),
        unreliable_where=(
            "192.168.1.44, 192.168.1.46, https://example.com, "
            "path/to/file1.ext, test/1"
        ),
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_upload_file_access_denied_error(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.skip(reason="Return error on localhost, no errors in result")
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
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidNewVulnState.msg


@pytest.mark.skip(reason="Return error on localhost, no errors in result")
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
async def test_upload_error(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns-error.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == InvalidCannotModifyNicknameWhenClosing.msg
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
async def test_upload_error_root(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vuln-error-root.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(RootNotFound())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_continuous_not_able(
    populate: bool, email: str
) -> None:
    """if type is continuous should have either squad or machine active"""
    assert populate
    finding_id: str = "918fbc15-2121-4c2a-83a8-dfa8748bcb2e"
    file_name: str = "test-vulns.yaml"
    result: dict[str, Any] = await get_result(
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
    ],
)
async def test_upload_file_oneshot_able(populate: bool, email: str) -> None:
    """if type is oneshot is not necessary to have squad or machine active"""
    assert populate
    mutation_1 = await update_services(
        user=email,
        group="group1",
        has_squad="false",
        has_machine="false",
        subscription=GroupSubscriptionType.ONESHOT.value,
    )
    assert "errors" not in mutation_1
    assert mutation_1["data"]["updateGroup"]["success"]

    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name: str = "test-vulnerability.yaml"
    result_1: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    mutation_2 = await update_services(
        user=email,
        group="group1",
        has_squad="false",
        has_machine="false",
        subscription=GroupSubscriptionType.CONTINUOUS.value,
    )
    assert "errors" not in mutation_2
    assert mutation_2["data"]["updateGroup"]["success"]

    result_2: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result_2
    assert result_2["errors"][0]["message"] == "Access denied"
