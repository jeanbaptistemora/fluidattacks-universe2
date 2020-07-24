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
    SeverityEnum,
    Vulnerability,
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
                kind=VulnerabilityKindEnum.LINES,
                source=VulnerabilitySourceEnum.SKIMS,
                state=VulnerabilityStateEnum.OPEN,
                what='what',
                where='123',
            ),
        )
    ) == dedent("""
        lines:
        - line: '123'
          path: what
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
        stream="""
            inputs: []
            lines: []
            ports:
                -   host: 127.0.0.1
                    port: '80'
                    source: skims
                    state: open
        """,
    )

    assert Vulnerability(
        finding=FindingEnum.F0034,
        kind=VulnerabilityKindEnum.PORTS,
        source=VulnerabilitySourceEnum.SKIMS,
        state=VulnerabilityStateEnum.OPEN,
        what='127.0.0.1',
        where='80',
    ) in await get_finding_vulnerabilities(
        finding=FindingEnum.F0034,
        finding_id=finding_id,
    )
