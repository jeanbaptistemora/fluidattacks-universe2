# Standard library
from typing import (
    Dict,
    Tuple,
    Union,
)

# Local libraries
from apis.integrates.dal import (
    get_group_findings,
    ResultGetGroupFindings,
)
from model import (
    IntegratesVulnerabilitiesLines,
    KindEnum,
    SkimResult,
    VulnerabilityStateEnum,
)
from utils.aio import (
    unblock,
)
from utils.encodings import (
    yaml_dumps,
)
from utils.string import (
    are_similar,
)


async def build_vulnerabilities_stream(
    *,
    results: Tuple[SkimResult, ...],
) -> str:

    data_type = Dict[
        KindEnum,
        Tuple[Union[IntegratesVulnerabilitiesLines], ...]
    ]

    def _get_data() -> data_type:
        data: data_type = {
            KindEnum.LINES: tuple(
                IntegratesVulnerabilitiesLines(
                    line=result.where,
                    path=result.what,
                    state=VulnerabilityStateEnum.OPEN,
                )
                for result in results
                if result.kind == KindEnum.LINES
            ),
            # More bindings for PORTS and INPUTS go here ...
        }

        return data

    return await yaml_dumps(await unblock(_get_data))


async def get_closest_finding_id(*, group: str, title: str) -> str:
    findings: Tuple[ResultGetGroupFindings, ...] = \
        await get_group_findings(group=group)

    for finding in findings:
        if are_similar(title, finding.title):
            return finding.identifier

    return ''
