from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from dataloaders.utils import (
    format_vulnerability,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
from vulnerabilities import (
    dal as vulns_dal,
)


async def _get_vulnerabilities_by_finding(
    finding_id: str,
) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = await vulns_dal.get_by_finding(
        finding_id=finding_id
    )
    return items


class FindingVulnsTypedLoader(DataLoader):
    def __init__(self, vuln_loader: DataLoader) -> None:
        super().__init__()
        self.vuln_loader = vuln_loader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        vulns = await collect(
            tuple(map(_get_vulnerabilities_by_finding, finding_ids))
        )
        result = []
        for finding_vulns in vulns:
            formatted = []
            for vuln in finding_vulns:
                self.vuln_loader.prime(vuln["UUID"], vuln)
                formatted.append(format_vulnerability(vuln))
            result.append(tuple(formatted))

        return tuple(result)
