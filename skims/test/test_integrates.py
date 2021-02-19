# Standard library
from textwrap import dedent

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from integrates.graphql import (
    client as graphql_client,
)
from integrates.dal import (
    get_group_level_role,
)
from integrates.domain import (
    build_vulnerabilities_stream,
)
from model import (
    core_model,
)


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_client(
    test_integrates_api_token: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    async with graphql_client() as client:
        # pylint: disable=protected-access
        assert client.session._default_headers == {
            'authorization': f'Bearer {test_integrates_api_token}',
            'x-integrates-source': 'skims'
        }


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_build_vulnerabilities_stream() -> None:
    assert await build_vulnerabilities_stream(
        results=(
            core_model.Vulnerability(
                finding=core_model.FindingEnum.F034,
                integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                    source=core_model.VulnerabilitySourceEnum.SKIMS,
                ),
                kind=core_model.VulnerabilityKindEnum.LINES,
                state=core_model.VulnerabilityStateEnum.OPEN,
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
@pytest.mark.skims_test_group('functional')
async def test_get_group_level_role(
    test_group: str,
    test_integrates_session: str,  # pylint: disable=unused-argument
) -> None:
    assert await get_group_level_role(group=test_group) == 'admin'
