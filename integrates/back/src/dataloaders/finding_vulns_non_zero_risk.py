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
from newutils import (
    vulnerabilities as vulns_utils,
)
from typing import (
    cast,
    List,
)


class FindingVulnsNonZeroRiskLoader(DataLoader):
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
            finding_vulns = vulns_utils.filter_non_requested_zero_risk(
                finding_vulns
            )
            finding_vulns = vulns_utils.filter_non_confirmed_zero_risk(
                finding_vulns
            )
            findings_vulns[index] = finding_vulns
        return cast(List[List[VulnerabilityType]], findings_vulns)
