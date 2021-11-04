from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityStateStatus,
)
from itertools import (
    chain,
)
from typing import (
    cast,
    List,
    Tuple,
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

    # pylint: disable=method-hidden
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


def _filter_non_deleted_vulns(
    vulns: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulns
        if vuln.state.status != VulnerabilityStateStatus.DELETED
    )


class FindingVulnsNonDeletedTypedLoader(DataLoader):
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
            _filter_non_deleted_vulns(finding_vulns)
            for finding_vulns in findings_vulns
        )
