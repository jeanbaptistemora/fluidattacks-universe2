# pylint: disable=method-hidden

from collections import defaultdict
from typing import cast, Dict, List

from backend.domain import finding as finding_domain

from backend.typing import Finding as FindingType

from aiodataloader import DataLoader


async def _batch_load_fn(
        finding_ids: List[str]) -> List[Dict[str, FindingType]]:
    """Batch the data load requests within the same execution fragment."""
    findings: Dict[str, Dict[str, FindingType]] = \
        defaultdict(Dict[str, FindingType])

    fins = await finding_domain.get_findings_async(finding_ids)

    for finding in fins:
        finding_id: str = cast(str, finding['findingId'])
        findings[finding_id] = dict(
            actor=finding.get('actor', ''),
            affected_systems=finding.get('affectedSystems', ''),
            age=finding.get('age', 0),
            analyst=finding.get('analyst', ''),
            attack_vector_desc=finding.get('attackVectorDesc', ''),
            bts_url=finding.get('externalBts', ''),
            compromised_attributes=finding.get('compromisedAttrs', ''),
            compromised_records=finding.get('recordsNumber', 0),
            cvss_version=finding.get('cvssVersion', '3.1'),
            cwe_url=finding.get('cwe', ''),
            description=finding.get('vulnerability', ''),
            evidence=finding.get('evidence', {}),  # type: ignore
            exploit=finding.get('exploit', {}),  # type: ignore
            id=finding.get('findingId', ''),
            is_exploitable=finding.get('exploitable', ''),
            last_vulnerability=finding.get('lastVulnerability', 0),
            project_name=finding.get('projectName', ''),
            recommendation=finding.get('effectSolution', ''),
            records=finding.get('records', {}),  # type: ignore
            release_date=finding.get('releaseDate', ''),
            remediated=finding.get('remediated', False),
            new_remediated=finding.get('newRemediated', False),
            verified=finding.get('verified', False),
            report_date=finding.get('reportDate', ''),
            requirements=finding.get('requirements', ''),
            risk=finding.get('risk', ''),
            scenario=finding.get('scenario', ''),
            severity=finding.get('severity', {}),  # type: ignore
            severity_score=finding.get('severityCvss', 0.0),
            threat=finding.get('threat', ''),
            title=finding.get('finding', ''),
            type=finding.get('findingType', ''),
            historic_state=finding.get('historicState', []),
            historic_treatment=finding.get('historicTreatment', []),
            current_state=finding.get(  # type: ignore
                'historicState', [{}])[-1].get('state', '')  # type: ignore
        )

    return [findings.get(finding_id, dict()) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingLoader(DataLoader):
    async def batch_load_fn(
            self, finding_ids: List[str]) -> List[Dict[str, FindingType]]:
        return await _batch_load_fn(finding_ids)
