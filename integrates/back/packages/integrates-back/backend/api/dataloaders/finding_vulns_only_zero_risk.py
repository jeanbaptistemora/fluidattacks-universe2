# pylint: disable=method-hidden

# Standard libraries
from typing import (
    cast,
    List
)

# Third party libraries
from aiodataloader import DataLoader

# Local libraries
from backend.domain import vulnerability as vuln_domain
from backend.typing import Vulnerability as VulnerabilityType


# pylint: disable=too-few-public-methods
class FindingVulnsOnlyZeroRiskLoader(DataLoader):  # type: ignore

    def __init__(self, dataloader: DataLoader) -> None:
        super(FindingVulnsOnlyZeroRiskLoader, self).__init__()
        self.dataloader = dataloader

    async def batch_load_fn(
        self,
        finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)

        for index, finding_vulns in enumerate(findings_vulns):
            finding_vulns = (
                vuln_domain.filter_requested_zero_risk(finding_vulns) +
                vuln_domain.filter_confirmed_zero_risk(finding_vulns)
            )
            findings_vulns[index] = finding_vulns

        return cast(List[List[VulnerabilityType]], findings_vulns)
