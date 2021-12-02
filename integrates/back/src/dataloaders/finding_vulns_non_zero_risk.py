from aiodataloader import (
    DataLoader,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from itertools import (
    chain,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
from typing import (
    List,
    Tuple,
)


class FindingVulnsNonZeroRiskTypedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, finding_ids: List[str]
    ) -> Tuple[Vulnerability, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            vulns_utils.filter_non_zero_risk(finding_vulns)
            for finding_vulns in findings_vulns
        )
