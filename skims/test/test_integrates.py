# Standard library
from textwrap import dedent

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
    delete_closest_findings,
    get_closest_finding_id,
)
from utils.aio import (
    block_decorator,
)
from utils.model import (
    FindingEnum,
    IntegratesVulnerabilitiesLines,
    IntegratesVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)
from zone import (
    t,
)


def test_session(
    test_integrates_api_token: str,
    test_integrates_session: None,
) -> None:
    assert Session.value is not None
    assert Session.value.headers == {
        'authorization': f'Bearer {test_integrates_api_token}'
    }


@block_decorator
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


@block_decorator
async def test_get_group_level_role(
    test_group: str,
    test_integrates_session: str,
) -> None:
    assert await get_group_level_role(group=test_group) == 'admin'


@block_decorator
async def test_statefull(
    test_group: str,
    test_integrates_session: None,
) -> None:
    finding: FindingEnum = FindingEnum.F0034

    assert await delete_closest_findings(
        finding=finding,
        group=test_group,
    )

    finding_id: str = await get_closest_finding_id(
        create_if_missing=True,
        finding=finding,
        group=test_group,
    )

    assert finding_id
    assert finding_id == await get_closest_finding_id(
        create_if_missing=False,
        finding=finding,
        group=test_group,
    )

    assert await do_update_finding_severity(
        finding_id=finding_id,
        severity=finding.value.severity,
    )

    assert ResultGetGroupFindings(
        identifier=finding_id,
        title=t(finding.value.title),
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
