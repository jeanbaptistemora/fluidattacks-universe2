from back.src.settings.logger import (
    LOGGING,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
import logging
import matplotlib
from reports.pdf import (
    CreatorPdf,
)
from reports.typing import (
    CertFindingInfo,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    TypedDict,
    Union,
    ValuesView,
)

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
Context = TypedDict(
    "Context",
    {
        "business": str,
        "business_number": str,
        "solution": str,
        "start_date": str,
        "report_date": str,
        "team": str,
        "team_mail": str,
        "customer": str,
        "version": str,
        "revdate": str,
        "remediation_table": ValuesView[List[Union[float, int, str]]],
        "findings": Tuple[CertFindingInfo, ...],
        "accessVector": Optional[str],
        "cert_title": str,
        "cert_body_part_1": str,
        "cert_body_part_2": str,
        "cert_signature": str,
        "crit_h": str,
        "crit_m": str,
        "crit_l": str,
        "field": str,
        "user": str,
        "date": str,
        "link": str,
    },
)


async def format_finding(
    loaders: Any,
    finding: Finding,
    words: Dict[str, str],
) -> CertFindingInfo:
    closed_vulnerabilities = await findings_domain.get_closed_vulnerabilities(
        loaders, finding.id
    )
    open_vulnerabilities = await findings_domain.get_open_vulnerabilities(
        loaders, finding.id
    )
    severity_score = findings_domain.get_severity_score(finding.severity)

    if open_vulnerabilities > 0:
        state = words["fin_status_open"]
    else:
        state = words["fin_status_closed"]

    return CertFindingInfo(
        closed_vulnerabilities=closed_vulnerabilities,
        open_vulnerabilities=open_vulnerabilities,
        severity_score=severity_score,
        state=state,
        title=finding.title,
    )


def _set_percentage(total_vulns: int, closed_vulns: int) -> str:
    if total_vulns == 0:
        return f"{closed_vulns * 100.0 / total_vulns:.1f}"
    return "N/A"


def make_remediation_table(
    context_findings: Tuple[CertFindingInfo, ...], words: Dict[str, str]
) -> ValuesView[List[Union[float, int, str]]]:
    critical, high, medium, low = (
        words["vuln_c"],
        words["vuln_h"],
        words["vuln_m"],
        words["vuln_l"],
    )
    remediation_dict: Dict[str, List[Union[float, int, str]]] = {
        #   Severity | Quantity | Total vulns | Closed vulns | Remediation %
        critical: [critical, 0, 0, 0, "N/A"],
        high: [high, 0, 0, 0, "N/A"],
        medium: [medium, 0, 0, 0, "N/A"],
        low: [low, 0, 0, 0, "N/A"],
    }

    for finding in context_findings:
        label: str = ""
        if 9.0 <= finding.severity_score <= 10.0:
            label = critical
        elif 7.0 <= finding.severity_score < 9.0:
            label = high
        elif 4.0 <= finding.severity_score < 7.0:
            label = medium
        else:
            label = low
        remediation_dict[label][1] = int(remediation_dict[label][1]) + 1
        remediation_dict[label][2] = int(remediation_dict[label][2]) + (
            finding.open_vulnerabilities + finding.closed_vulnerabilities
        )
        remediation_dict[label][3] = (
            int(remediation_dict[label][3]) + finding.closed_vulnerabilities
        )

    remediation_dict[critical][4] = _set_percentage(
        int(remediation_dict[critical][2]), int(remediation_dict[critical][3])
    )
    remediation_dict[high][4] = _set_percentage(
        int(remediation_dict[high][2]), int(remediation_dict[high][3])
    )
    remediation_dict[medium][4] = _set_percentage(
        int(remediation_dict[medium][2]), int(remediation_dict[medium][3])
    )
    remediation_dict[low][4] = _set_percentage(
        int(remediation_dict[low][2]), int(remediation_dict[low][3])
    )

    return remediation_dict.values()


class CertificateCreator(CreatorPdf):
    """Class to generate certificates in PDF."""

    def __init__(self, lang: str, doctype: str, tempdir: str) -> None:
        "Class constructor"
        super().__init__(lang, doctype, tempdir)
        self.proj_tpl = "templates/pdf/certificate.adoc"
