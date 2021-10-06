# pylint: disable=method-hidden
from aiodataloader import (
    DataLoader,
)
from collections import (
    defaultdict,
)
from custom_types import (
    Finding as FindingType,
)
from findings import (
    domain as findings_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    cast,
    Dict,
    List,
)


async def _batch_load_fn(
    finding_ids: List[str],
) -> List[Dict[str, FindingType]]:
    """Batch the data load requests within the same execution fragment."""
    findings: Dict[str, Dict[str, FindingType]] = defaultdict(
        Dict[str, FindingType]
    )

    fins = await findings_domain.get_findings_async(finding_ids)
    for finding in fins:
        # Compatibility with old API
        group_name: str = get_key_or_fallback(
            finding, "groupName", "projectName", ""
        )
        finding_id: str = cast(str, finding["findingId"])
        findings[finding_id] = dict(
            affected_systems=finding.get("affectedSystems", ""),
            analyst=finding.get("analyst", ""),
            attack_vector_desc=finding.get("attackVectorDesc", ""),
            attack_vector_description=finding.get("attackVectorDesc", ""),
            compromised_attributes=finding.get("compromisedAttrs", ""),
            compromised_records=finding.get("recordsNumber", 0),
            current_state=cast(
                List[Dict[str, str]], finding.get("historicState", [{}])
            )[-1].get("state", ""),
            cvss_version=finding.get("cvssVersion", "3.1"),
            description=finding.get("vulnerability", ""),
            evidence=finding.get("evidence", ""),
            finding_id=finding.get("findingId", ""),
            historic_state=finding.get("historicState", [{}]),
            historic_verification=finding.get("historicVerification", []),
            id=finding.get("findingId", ""),
            is_exploitable=finding.get("exploitable", ""),
            recommendation=finding.get("effectSolution", ""),
            records=finding.get("records", ""),
            remediated=finding.get("remediated", False),
            repo_nickname=finding.get("repo_nickname", ""),
            requirements=finding.get("requirements", ""),
            sorts=finding.get("sorts", None),
            severity=finding.get("severity", ""),
            severity_score=finding.get("severityCvss", 0.0),
            threat=finding.get("threat", ""),
            title=finding.get("finding", ""),
            # Standardization field
            group_name=group_name,
            project_name=group_name,
        )
    return [findings.get(finding_id, {}) for finding_id in finding_ids]


class FindingLoader(DataLoader):
    # pylint: disable=no-self-use
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> List[Dict[str, FindingType]]:
        return await _batch_load_fn(finding_ids)
