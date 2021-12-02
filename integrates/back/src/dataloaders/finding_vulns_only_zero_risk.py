from aiodataloader import (
    DataLoader,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
from typing import (
    List,
    Tuple,
)


class FindingVulnsOnlyZeroRiskTypedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            vulns_utils.filter_zero_risk(finding_vulns)
            for finding_vulns in findings_vulns
        )
