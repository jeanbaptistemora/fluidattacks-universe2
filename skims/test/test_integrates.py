from aioextensions import (
    run_decorator,
)
from ctx import (
    CTX,
)
from integrates.dal import (
    get_group_level_role,
)
from integrates.domain import (
    build_vulnerabilities_stream,
)
from integrates.graphql import (
    client as graphql_client,
)
from model import (
    core_model,
)
import pytest
from textwrap import (
    dedent,
)
from utils.repositories import (
    get_repo_head_hash,
)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_client(
    test_integrates_api_token: str,
) -> None:
    async with graphql_client() as client:
        # pylint: disable=protected-access
        assert client.session._default_headers == {
            "authorization": f"Bearer {test_integrates_api_token}",
            "x-integrates-source": "skims",
        }


@run_decorator
@pytest.mark.skims_test_group("functional")
async def test_build_vulnerabilities_stream() -> None:
    developer = "drestrepo@fluidattacks.com"
    skims_method = "query.query_f034"
    skims_technique = "ASAST"
    commit_hash = get_repo_head_hash(CTX.config.working_dir)

    assert (
        await build_vulnerabilities_stream(
            results=(
                core_model.Vulnerability(
                    finding=core_model.FindingEnum.F034,
                    integrates_metadata=(
                        core_model.IntegratesVulnerabilityMetadata(
                            source=core_model.VulnerabilitySourceEnum.SKIMS,
                        )
                    ),
                    kind=core_model.VulnerabilityKindEnum.LINES,
                    namespace="test",
                    state=core_model.VulnerabilityStateEnum.OPEN,
                    what="what",
                    where="11",
                    skims_metadata=core_model.SkimsVulnerabilityMetadata(
                        cwe=(330,),
                        description="Vulnerability description",
                        snippet="Vulnerability snippet",
                        source_method=skims_method,
                        developer=developer,
                        technique=skims_technique,
                    ),
                ),
                core_model.Vulnerability(
                    finding=core_model.FindingEnum.F034,
                    integrates_metadata=(
                        core_model.IntegratesVulnerabilityMetadata(
                            source=core_model.VulnerabilitySourceEnum.SKIMS,
                        )
                    ),
                    kind=core_model.VulnerabilityKindEnum.INPUTS,
                    namespace="test",
                    state=core_model.VulnerabilityStateEnum.OPEN,
                    stream="a,b,c",
                    what="https://example.com",
                    where="test",
                ),
            )
        )
        == dedent(
            f"""
        inputs:
        - field: test
          repo_nickname: test
          state: open
          stream: a,b,c
          url: https://example.com (test)
        lines:
        - commit_hash: {commit_hash}
          developer: {developer}
          line: '11'
          path: test/what
          repo_nickname: test
          skims_method: {skims_method}
          skims_technique: {skims_technique}
          state: open
    """
        )[1:]
    )


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_get_group_level_role(
    test_group: str,
) -> None:
    assert await get_group_level_role(group=test_group) == "admin"
