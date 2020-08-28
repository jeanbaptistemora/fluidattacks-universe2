# Standard library
from textwrap import dedent

# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from integrates.graphql import (
    client as graphql_client,
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


@run_decorator
async def test_client(
    test_integrates_api_token: str,
    test_integrates_session: None,
) -> None:
    async with graphql_client() as client:
        assert client.session._default_headers == {
            'authorization': f'Bearer {test_integrates_api_token}'
        }


@run_decorator
async def test_build_vulnerabilities_stream() -> None:
    assert await build_vulnerabilities_stream(
        results=(
            Vulnerability(
                finding=FindingEnum.F034,
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


@run_decorator
async def test_get_group_level_role(
    test_group: str,
    test_integrates_session: str,
) -> None:
    assert await get_group_level_role(group=test_group) == 'admin'
