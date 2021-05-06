# pylint: disable=method-hidden
from collections import defaultdict
from typing import (
    Dict,
    List,
    cast,
)

from aiodataloader import DataLoader

from backend.typing import Finding as FindingType
from findings import domain as findings_domain


async def _batch_load_fn(
    finding_ids: List[str]
) -> List[Dict[str, FindingType]]:
    """Batch the data load requests within the same execution fragment."""
    findings: Dict[str, Dict[str, FindingType]] = defaultdict(
        Dict[str, FindingType]
    )

    fins = await findings_domain.get_findings_async(finding_ids)
    for finding in fins:
        finding_id: str = cast(str, finding['findingId'])
        findings[finding_id] = dict(
            actor=finding.get('actor', ''),
            affected_systems=finding.get('affectedSystems', ''),
            analyst=finding.get('analyst', ''),
            attack_vector_desc=finding.get('attackVectorDesc', ''),
            bts_url=finding.get('externalBts', ''),
            compromised_attributes=finding.get('compromisedAttrs', ''),
            compromised_records=finding.get('recordsNumber', 0),
            current_state=cast(
                List[Dict[str, str]],
                finding.get('historicState', [{}])
            )[-1].get('state', ''),
            cvss_version=finding.get('cvssVersion', '3.1'),
            cwe_url=finding.get('cwe', ''),
            description=finding.get('vulnerability', ''),
            evidence=finding.get('evidence', ''),
            finding_id=finding.get('findingId', ''),
            historic_state=finding.get('historicState', [{}]),
            historic_verification=finding.get('historicVerification', []),
            id=finding.get('findingId', ''),
            is_exploitable=finding.get('exploitable', ''),
            project_name=finding.get('projectName', ''),
            recommendation=finding.get('effectSolution', ''),
            records=finding.get('records', ''),
            remediated=finding.get('remediated', False),
            requirements=finding.get('requirements', ''),
            risk=finding.get('risk', ''),
            scenario=finding.get('scenario', ''),
            sorts=finding.get('sorts', None),
            severity=finding.get('severity', ''),
            severity_score=finding.get('severityCvss', 0.0),
            threat=finding.get('threat', ''),
            title=finding.get('finding', ''),
            type=finding.get('findingType', ''),
        )
    return [findings.get(finding_id, dict()) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingLoader(DataLoader):
    async def batch_load_fn(
        self,
        finding_ids: List[str]
    ) -> List[Dict[str, FindingType]]:
        return await _batch_load_fn(finding_ids)
