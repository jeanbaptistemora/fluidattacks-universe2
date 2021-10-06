# pylint: disable=method-hidden

from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from itertools import (
    chain,
)
from typing import (
    cast,
    List,
)


class FindingVulnsNonDeletedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        unchained_data = await self.load_many(finding_ids)
        return list(chain.from_iterable(unchained_data))

    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)

        for index, finding_vulns in enumerate(findings_vulns):
            vulns = [
                vuln
                for vuln in finding_vulns
                if vuln.get("historic_state", [{}])[-1].get("state")
                != "DELETED"
            ]
            findings_vulns[index] = vulns
        return cast(List[List[VulnerabilityType]], findings_vulns)
