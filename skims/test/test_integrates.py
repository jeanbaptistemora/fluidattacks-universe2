# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
async def test_build_vulnerabilities_stream() -> None:
    sast_developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    sast_method = "query.query_f034"
    sast_technique = core_model.TechniqueEnum.ADVANCE_SAST

    dast_developer = core_model.DeveloperEnum.ALEJANDRO_SALGADO
    dast_method = "analyze_protocol.pfs_disabled"
    dast_technique = core_model.TechniqueEnum.DAST

    commit_hash = CTX.config.commit or get_repo_head_hash(
        CTX.config.working_dir
    )

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
                        source_method=sast_method,
                        developer=sast_developer,
                        technique=sast_technique,
                    ),
                ),
                core_model.Vulnerability(
                    finding=core_model.FindingEnum.F133,
                    integrates_metadata=(
                        core_model.IntegratesVulnerabilityMetadata(
                            source=core_model.VulnerabilitySourceEnum.SKIMS,
                        )
                    ),
                    skims_metadata=core_model.SkimsVulnerabilityMetadata(
                        cwe=(310,),
                        description="Vulnerability description",
                        snippet="Vulnerability snippet",
                        source_method=dast_method,
                        developer=dast_developer,
                        technique=dast_technique,
                    ),
                    kind=core_model.VulnerabilityKindEnum.INPUTS,
                    namespace="test",
                    state=core_model.VulnerabilityStateEnum.OPEN,
                    stream="home,socket-send,socket-response",
                    what="https://example.com:443",
                    where="server refuses connections with PFS support",
                ),
            )
        )
        == dedent(
            f"""
        inputs:
        - developer: {dast_developer.value}
          field: server refuses connections with PFS support
          repo_nickname: test
          skims_method: {dast_method}
          skims_technique: {dast_technique.value}
          source: machine
          state: open
          stream: home,socket-send,socket-response
          tool:
            impact: direct
            name: machine
          url: https://example.com:443 (test)
        lines:
        - commit_hash: {commit_hash}
          developer: {sast_developer.value}
          line: '11'
          path: test/what
          repo_nickname: test
          skims_method: {sast_method}
          skims_technique: {sast_technique.value}
          source: machine
          state: open
          tool:
            impact: direct
            name: machine
    """
        )[1:]
    )


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_get_group_level_role(
    test_group: str,
) -> None:
    assert await get_group_level_role(group=test_group) == "admin"
