# pylint: disable=method-hidden

from collections import defaultdict
from typing import Dict, List, cast

from aiodataloader import DataLoader

from backend.domain import vulnerability as vuln_domain
from backend.typing import (
    Vulnerability as VulnerabilityType,
    Historic as HistoricType
)


async def _batch_load_fn(
        finding_ids: List[str]) -> List[List[VulnerabilityType]]:
    """Batch the data load requests within the same execution fragment."""
    vulnerabilities: Dict[str, List[VulnerabilityType]] = defaultdict(list)

    vulns = await vuln_domain.list_vulnerabilities_async(finding_ids)
    for vuln in vulns:
        vulnerabilities[cast(str, vuln['finding_id'])].append(
            dict(
                UUID=cast(str, vuln.get('UUID', '')),
                id=cast(str, vuln.get('UUID', '')),
                external_bts=cast(str, vuln.get('external_bts', '')),
                finding_id=cast(str, vuln.get('finding_id', '')),
                vuln_type=cast(str, vuln.get('vuln_type', '')),
                where=cast(str, vuln.get('where', '')),
                source=cast(str, vuln.get('source', 'integrates')),
                specific=cast(str, vuln.get('specific', '')),
                historic_state=cast(
                    HistoricType,
                    vuln.get('historic_state', [{}])
                ),
                current_state=cast(
                    str,
                    cast(
                        HistoricType,
                        vuln.get('historic_state', [{}])
                    )[-1].get('state', '')
                ),
                current_approval_status=cast(
                    str,
                    cast(
                        HistoricType,
                        vuln.get('historic_state', [{}])
                    )[-1].get('approval_status', '')
                ),
                analyst=cast(
                    str,
                    cast(
                        HistoricType,
                        vuln.get('historic_state', [{}])
                    )[-1].get('analyst', '')
                ),
                remediated=cast(
                    HistoricType,
                    vuln.get('historic_verification', [{}])
                )[-1].get('status') == 'REQUESTED',
                severity=cast(str, vuln.get('severity', '')),
                tag=', '.join(cast(List[str], vuln.get('tag', []))),
                treatment_manager=cast(str, vuln.get('treatment_manager', '')),
                verification=cast(
                    HistoricType,
                    vuln.get(
                        'historic_verification',
                        [{}]
                    )
                )[-1].get('status', '').capitalize(),
                historic_verification=cast(
                    HistoricType,
                    vuln.get('historic_verification', [])
                ),
                historic_zero_risk=cast(
                    HistoricType,
                    vuln.get('historic_zero_risk', [])
                ),
                zero_risk=cast(
                    HistoricType,
                    vuln.get(
                        'historic_zero_risk',
                        [{}]
                    )
                )[-1].get('status', '').capitalize()
            )
        )

    return [vulnerabilities.get(finding_id, []) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingVulnsLoader(DataLoader):  # type: ignore
    async def batch_load_fn(
            self, finding_ids: List[str]) -> List[List[VulnerabilityType]]:
        return await _batch_load_fn(finding_ids)
