# Standard library
from textwrap import dedent

# Third party libraries
import pytest

# Local libraries
from apis.integrates.domain import (
    build_vulnerabilities_stream,
    get_closest_finding_id,
)
from apis.integrates.graphql import (
    session,
)
from model import (
    FindingEnum,
    IntegratesVulnerabilitiesLines,
    KindEnum,
    Vulnerability,
    VulnerabilityStateEnum,
)


@pytest.mark.asyncio  # type: ignore
async def test_domain(
    test_group: str,
    test_token: str,
) -> None:
    async with session(api_token=test_token):
        assert await get_closest_finding_id(
            group=test_group,
            title='Insecure random numbers generation',
        ) == '974751758'

        assert await get_closest_finding_id(
            group=test_group,
            title='XXX',
        ) == ''


@pytest.mark.asyncio  # type: ignore
async def test_build_vulnerabilities_stream() -> None:
    assert await build_vulnerabilities_stream(
        results=(
            Vulnerability(
                finding=FindingEnum.F0034,
                kind=KindEnum.LINES,
                what='what',
                where='123',
                state=VulnerabilityStateEnum.OPEN,
            ),
        )
    ) == dedent("""
        lines:
        - line: '123'
          path: what
          state: open
    """)[1:]
