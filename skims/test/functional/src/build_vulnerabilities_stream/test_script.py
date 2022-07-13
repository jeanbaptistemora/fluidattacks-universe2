from ctx import (
    CTX,
)
from integrates.domain import (
    build_vulnerabilities_stream,
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
@pytest.mark.skims_test_group("build_vulnerabilities_stream")
async def test_build_vulnerabilities_stream() -> None:
    sast_developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    sast_method = "query.query_f034"
    sast_technique = core_model.TechniqueEnum.ADVANCE_SAST

    dast_developer = core_model.DeveloperEnum.ALEJANDRO_SALGADO
    dast_method = "analyze_protocol.pfs_disabled"
    dast_technique = core_model.TechniqueEnum.DAST

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
          state: open
          stream: home,socket-send,socket-response
          url: https://example.com:443 (test)
        lines:
        - commit_hash: {commit_hash}
          developer: {sast_developer.value}
          line: '11'
          path: test/what
          repo_nickname: test
          skims_method: {sast_method}
          skims_technique: {sast_technique.value}
          state: open
    """
        )[1:]
    )
