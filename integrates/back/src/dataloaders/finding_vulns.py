# pylint: disable=method-hidden

from aiodataloader import (
    DataLoader,
)
from collections import (
    defaultdict,
)
from custom_types import (
    Historic as HistoricType,
    Vulnerability as VulnerabilityType,
)
from newutils.requests import (
    map_source,
)
from typing import (
    cast,
    Dict,
    List,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def batch_load_fn_vulns(
    finding_ids: List[str],
) -> List[List[VulnerabilityType]]:
    """Batch the data load requests within the same execution fragment."""
    vulnerabilities: Dict[str, List[VulnerabilityType]] = defaultdict(list)

    vulns = await vulns_domain.list_vulnerabilities_async(
        finding_ids,
        should_list_deleted=True,
        include_requested_zero_risk=True,
        include_confirmed_zero_risk=True,
    )
    for vuln in vulns:
        # Compatibility with old API
        history: HistoricType = cast(HistoricType, vuln["historic_state"])
        source: str = map_source(history[0]["source"])
        vulnerabilities[cast(str, vuln["finding_id"])].append(
            dict(
                UUID=cast(str, vuln.get("UUID", "")),
                analyst=cast(
                    str,
                    cast(HistoricType, vuln.get("historic_state", [{}]))[
                        -1
                    ].get("analyst", ""),
                ),
                commit_hash=str(vuln.get("commit_hash", "")),
                current_approval_status=cast(
                    str,
                    cast(HistoricType, vuln.get("historic_state", [{}]))[
                        -1
                    ].get("approval_status", ""),
                ),
                current_state=cast(
                    str,
                    cast(HistoricType, vuln.get("historic_state", [{}]))[
                        -1
                    ].get("state", ""),
                ),
                cycles=str(vulns_domain.get_reattack_cycles(vuln)),
                efficacy=str(vulns_domain.get_efficacy(vuln)),
                external_bts=cast(str, vuln.get("external_bts", "")),
                finding_id=cast(str, vuln.get("finding_id", "")),
                historic_state=cast(
                    HistoricType, vuln.get("historic_state", [{}])
                ),
                historic_treatment=cast(
                    HistoricType, vuln.get("historic_treatment", [])
                ),
                historic_verification=cast(
                    HistoricType, vuln.get("historic_verification", [{}])
                ),
                historic_zero_risk=cast(
                    HistoricType, vuln.get("historic_zero_risk", [{}])
                ),
                id=cast(str, vuln.get("UUID", "")),
                last_reattack_date=vulns_domain.get_last_reattack_date(vuln),
                last_requested_reattack_date=(
                    vulns_domain.get_last_requested_reattack_date(vuln)
                ),
                remediated=cast(
                    HistoricType, vuln.get("historic_verification", [{}])
                )[-1].get("status")
                == "REQUESTED",
                repo_nickname=vuln.get("repo_nickname"),
                report_date=cast(HistoricType, vuln["historic_state"])[0][
                    "date"
                ],
                severity=cast(str, vuln.get("severity", "")),
                source=source,
                specific=cast(str, vuln.get("specific", "")),
                stream=str(vuln.get("stream", "")).replace(",", " > "),
                tag=", ".join(sorted(cast(List[str], vuln.get("tag", [])))),
                verification=cast(
                    HistoricType, vuln.get("historic_verification", [{}])
                )[-1]
                .get("status", "")
                .capitalize(),
                vuln_type=cast(str, vuln.get("vuln_type", "")),
                vulnerability_type=cast(str, vuln.get("vuln_type", "")),
                where=cast(str, vuln.get("where", "")),
                zero_risk=cast(
                    HistoricType, vuln.get("historic_zero_risk", [{}])
                )[-1]
                .get("status", "")
                .capitalize(),
            )
        )
    return [vulnerabilities.get(finding_id, []) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingVulnsLoader(DataLoader):
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> List[List[VulnerabilityType]]:
        return await batch_load_fn_vulns(finding_ids)
