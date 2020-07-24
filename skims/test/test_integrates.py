# Standard library
from textwrap import dedent

# Third party libraries
import pytest

# Local libraries
from integrates.graphql import (
    Session,
)
from integrates.dal import (
    do_create_draft,
    do_update_finding_severity,
    do_upload_vulnerabilities,
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_level_role,
    ResultGetGroupFindings,
)
from integrates.domain import (
    build_vulnerabilities_stream,
    get_closest_finding_id,
)
from utils.model import (
    FindingEnum,
    IntegratesVulnerabilitiesLines,
    IntegratesVulnerabilityMetadata,
    SeverityEnum,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)


@pytest.mark.asyncio  # type: ignore
async def test_session() -> None:
    assert Session.value is not None


@pytest.mark.asyncio  # type: ignore
async def test_build_vulnerabilities_stream() -> None:
    assert await build_vulnerabilities_stream(
        results=(
            Vulnerability(
                finding=FindingEnum.F0034,
                integrates_metadata=IntegratesVulnerabilityMetadata(
                    source=VulnerabilitySourceEnum.SKIMS,
                ),
                kind=VulnerabilityKindEnum.LINES,
                state=VulnerabilityStateEnum.OPEN,
                what='what',
                where='123',
            ),
        )
    ) == dedent("""
        lines:
        - line: '123'
          path: what
          source: skims
          state: open
    """)[1:]


@pytest.mark.asyncio  # type: ignore
async def test_get_group_level_role(
    test_group: str,
) -> None:
    assert await get_group_level_role(group=test_group) == 'admin'


@pytest.mark.asyncio  # type: ignore
async def test_statefull(
    test_finding: FindingEnum,
    test_group: str,
    test_token: str,
) -> None:
    finding_id: str = await get_closest_finding_id(
        create_if_missing=True,
        finding=test_finding,
        group=test_group,
    )

    assert finding_id
    assert finding_id == await get_closest_finding_id(
        create_if_missing=False,
        finding=test_finding,
        group=test_group,
    )

    assert await do_update_finding_severity(
        finding_id=finding_id,
        severity=SeverityEnum.F0034,
    )

    assert ResultGetGroupFindings(
        identifier=finding_id,
        title=test_finding.value,
    ) in await get_group_findings(group=test_group)

    assert await do_upload_vulnerabilities(
        finding_id=finding_id,
        stream=await build_vulnerabilities_stream(
            results=(
                Vulnerability(
                    finding=FindingEnum.F0034,
                    integrates_metadata=IntegratesVulnerabilityMetadata(
                        source=VulnerabilitySourceEnum.SKIMS,
                    ),
                    kind=VulnerabilityKindEnum.LINES,
                    state=VulnerabilityStateEnum.OPEN,
                    what='repo/file',
                    where='123',
                ),
            ),
        ),
    )

    assert any(
        (
            vulnerability.finding == FindingEnum.F0034
            and vulnerability.integrates_metadata
            and vulnerability.integrates_metadata.approval_status == (
                VulnerabilityApprovalStatusEnum.PENDING
            )
            and vulnerability.integrates_metadata.source == (
                VulnerabilitySourceEnum.SKIMS
            )
            and vulnerability.integrates_metadata.uuid
            and vulnerability.kind == VulnerabilityKindEnum.LINES
            and vulnerability.state == VulnerabilityStateEnum.OPEN
            and vulnerability.what == 'repo/file'
            and vulnerability.where == '123'
        )
        for vulnerability in await get_finding_vulnerabilities(
            finding=FindingEnum.F0034,
            finding_id=finding_id,
        )
    )
