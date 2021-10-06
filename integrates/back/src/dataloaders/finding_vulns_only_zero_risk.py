# pylint: disable=method-hidden

from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from typing import (
    cast,
    List,
)
from vulnerabilities import (
    domain as vulns_domain,
)


class FindingVulnsOnlyZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)

        for index, finding_vulns in enumerate(findings_vulns):
            finding_vulns = vulns_domain.filter_requested_zero_risk(
                finding_vulns
            ) + vulns_domain.filter_confirmed_zero_risk(finding_vulns)
            findings_vulns[index] = finding_vulns
        return cast(List[List[VulnerabilityType]], findings_vulns)
