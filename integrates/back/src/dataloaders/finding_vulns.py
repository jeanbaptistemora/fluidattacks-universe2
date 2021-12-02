from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders.utils import (
    format_vulnerability,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from typing import (
    List,
    Tuple,
)
from vulnerabilities import (
    dal as vulns_dal,
)


async def _get_vulnerabilities_by_finding(
    finding_id: str,
) -> Tuple[Vulnerability, ...]:
    items: List[VulnerabilityType] = await vulns_dal.get_by_finding(
        finding_id=finding_id
    )
    return tuple(map(format_vulnerability, items))


class FindingVulnsTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        return await collect(
            tuple(map(_get_vulnerabilities_by_finding, finding_ids))
        )
