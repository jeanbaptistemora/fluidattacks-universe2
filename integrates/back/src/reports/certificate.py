from aioextensions import (
    collect,
)
from back.src.settings.logger import (
    LOGGING,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
import logging
import matplotlib
from newutils.datetime import (
    get_from_str,
    get_now,
)
from reports.pdf import (
    CreatorPdf,
)
from reports.typing import (
    CertFindingInfo,
    CertInfoEs,
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
CertContext = TypedDict(
    "CertContext",
    {
        "business": str,
        "business_number": str,
        "customer": str,
        "solution": str,
        "remediation_table": ValuesView[List[Union[float, int, str]]],
        "fluid_tpl": Dict[str, str],
        "cert_title": str,
        "cert_body_part_1": str,
        "cert_body_part_2": str,
        "signature_footer": str,
        "start_day": str,
        "start_month": str,
        "start_year": str,
        "report_day": str,
        "report_month": str,
        "report_year": str,
        "words": Dict[str, str],
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
        return f"{closed_vulns * 100.0 / total_vulns:.1f}%"
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

    cert_context: Optional[CertContext] = None
    cert_body: Dict[str, Dict[str, str]] = {}

    def __init__(self, lang: str, doctype: str, tempdir: str) -> None:
        "Class constructor"
        super().__init__(lang, doctype, tempdir)
        self.proj_tpl = "templates/pdf/certificate.adoc"
        self.cert_support()

    def cert_support(self) -> None:
        """Define the dictionaries of accepted languages. For
        the certificate body"""
        self.cert_body = {}
        self.cert_support_es()

    def cert_support_es(self) -> None:
        """Adds the English dictionary."""
        self.wordlist["en"] = dict(zip(CertInfoEs.keys(), CertInfoEs.labels()))

    def make_content(self, words: Dict[str, str]) -> Dict[str, str]:
        """Gather Fluid-related content needed for the cert"""
        base_adoc = "include::../templates/pdf/footer_{lang}.adoc[]"
        return {
            "signature_img": "image::../templates/pdf/signature.png[]",
            "footer_adoc": base_adoc.format(lang=self.lang),
        }

    async def fill_context(  # noqa pylint: disable=too-many-arguments,too-many-locals
        self,
        findings: Tuple[Finding, ...],
        group: str,
        description: str,
        user: str,
        loaders: Any,
    ) -> None:
        """Fetch information and fill out the context"""
        words = self.wordlist[self.lang]
        cert_body_loc = self.cert_body[self.lang]
        fluid_tpl_content = self.make_content(words)
        context_findings = await collect(
            [format_finding(loaders, finding, words) for finding in findings]
        )
        remediation_table = make_remediation_table(context_findings, words)
        group_data: Dict[str, Any] = loaders.group.load((group))
        start_date: datetime = get_from_str(
            group_data["historic_configuration"][0]["date"]
        )
        current_date: datetime = get_now()
        self.cert_context = {
            "business": "",
            "business_number": "",
            "customer": user,
            "fluid_tpl": fluid_tpl_content,
            "remediation_table": remediation_table,
            "cert_title": words["cert_title"],
            "cert_body_part_1": cert_body_loc["cert_body_part_1"],
            "cert_body_part_2": cert_body_loc["cert_body_part_2"],
            "signature_footer": cert_body_loc["signature_footer"],
            "start_day": str(start_date.day),
            "start_month": start_date.strftime("%B"),
            "start_year": str(start_date.year),
            "report_day": str(current_date.day),
            "report_month": current_date.strftime("%B"),
            "report_year": str(current_date.year),
            "solution": description,
            "words": words,
        }
