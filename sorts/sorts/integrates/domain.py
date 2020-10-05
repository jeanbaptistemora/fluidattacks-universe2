# Standard libraries
from typing import List

# Local libraries
from integrates.dal import (
    get_vulnerabilities,
    Vulnerability,
    VulnerabilityKindEnum,
)


async def get_vulnerable_lines(group: str) -> List[Vulnerability]:
    vulnerabilities: List[Vulnerability] = await get_vulnerabilities(group)
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.kind == VulnerabilityKindEnum.LINES
    ]
