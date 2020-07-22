# Standard library
from typing import (
    Tuple,
)

# Local libraries
from apis.integrates.dal import (
    get_group_findings,
    ResultGetGroupFindings,
)
from utils.string import (
    are_similar,
)


async def get_closest_finding_id(*, group: str, title: str) -> str:
    findings: Tuple[ResultGetGroupFindings, ...] = \
        await get_group_findings(group=group)

    for finding in findings:
        if are_similar(title, finding.title):
            return finding.identifier

    return ''
