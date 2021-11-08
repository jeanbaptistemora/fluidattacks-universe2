from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityZeroRiskStatus,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
from typing import (
    cast,
    List,
    Tuple,
)


class FindingVulnsOnlyZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)

        for index, finding_vulns in enumerate(findings_vulns):
            finding_vulns = vulns_utils.filter_requested_zero_risk(
                finding_vulns
            ) + vulns_utils.filter_confirmed_zero_risk(finding_vulns)
            findings_vulns[index] = finding_vulns
        return cast(List[List[VulnerabilityType]], findings_vulns)


def _filter_zero_risk_vulns(
    vulns: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulns
        if vuln.zero_risk
        and vuln.zero_risk.status
        in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
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
            _filter_zero_risk_vulns(finding_vulns)
            for finding_vulns in findings_vulns
        )
