# FP: local testing
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
)

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
RemediationTable = TypedDict(
    "RemediationTable",
    {
        "table": List[List[Union[float, int, str]]],
    },
)
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
        "simpledate": str,
        "remediation_table": RemediationTable,
        "findings": Tuple[CertFindingInfo, ...],
        "accessVector": Optional[str],
        "cert_title": str,
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


class CertificateCreator(CreatorPdf):
    """Class to generate certificates in PDF."""

    def __init__(self, lang: str, doctype: str, tempdir: str) -> None:
        "Class constructor"
        super().__init__(lang, doctype, tempdir)
        self.proj_tpl = "templates/pdf/certificate.adoc"
