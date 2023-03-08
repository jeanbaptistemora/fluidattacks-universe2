from aioextensions import (
    collect,
)
from collections.abc import (
    ValuesView,
)
from dataloaders import (
    Dataloaders,
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
from groups import (
    domain as groups_domain,
)
import jinja2
from jinja2.utils import (
    select_autoescape,
)
import logging
import matplotlib
from newutils import (
    datetime as datetime_utils,
)
from newutils.reports import (
    get_ordinal_ending,
)
from reports.pdf import (
    CreatorPdf,
)
from reports.typing import (
    CertFindingInfo,
)
from s3 import (
    operations as s3_ops,
)
from settings.logger import (
    LOGGING,
)
import subprocess  # nosec
import tempfile
from typing import (
    TypedDict,
)
import uuid

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
CertContext = TypedDict(
    "CertContext",
    {
        "business": str,
        "business_number": str,
        "solution": str,
        "remediation_table": ValuesView[list[float | int | str]],
        "start_day": str,
        "start_month": str,
        "start_year": str,
        "start_ordinal_ending": str,
        "report_day": str,
        "report_month": str,
        "report_year": str,
        "report_ordinal_ending": str,
        "signature_img": str,
        "words": dict[str, str],
    },
)


async def format_finding(
    loaders: Dataloaders,
    finding: Finding,
    words: dict[str, str],
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
    if total_vulns != 0:
        percentage = closed_vulns * 100.0 / total_vulns
        if percentage == int(percentage):
            return f"{percentage:.0f}%"
        return f"{percentage:.1f}%"
    return "N/A"


def make_remediation_table(
    context_findings: tuple[CertFindingInfo, ...], words: dict[str, str]
) -> ValuesView[list[float | int | str]]:
    critical, high, medium, low = (
        words["vuln_c"],
        words["vuln_h"],
        words["vuln_m"],
        words["vuln_l"],
    )
    remediation_dict: dict[str, list[float | int | str]] = {
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


def resolve_month_name(
    lang: str, date: datetime, words: dict[str, str]
) -> str:
    if lang.lower() == "en":
        return date.strftime("%B")
    return words[date.strftime("%B").lower()]


class CertificateCreator(CreatorPdf):
    """Class to generate certificates in PDF."""

    cert_context: CertContext

    def __init__(  # pylint: disable=too-many-arguments
        self, lang: str, doctype: str, tempdir: str, group: str, user: str
    ) -> None:
        "Class constructor"
        super().__init__(lang, doctype, tempdir, group, user)
        self.proj_tpl = f"templates/pdf/certificate_{lang}.adoc"

    async def fill_context(  # noqa
        self,
        findings: tuple[Finding, ...],
        group_name: str,
        description: str,
        loaders: Dataloaders,
    ) -> None:
        """Fetch information and fill out the context."""
        words = self.wordlist[self.lang]
        context_findings = await collect(
            [format_finding(loaders, finding, words) for finding in findings]
        )
        remediation_table = make_remediation_table(context_findings, words)
        group = await groups_domain.get_group(loaders, group_name)
        oldest_vuln_date: (
            datetime | None
        ) = await groups_domain.get_oldest_finding_date(loaders, group_name)
        start_date: datetime = (
            min(group.created_date, oldest_vuln_date)
            if oldest_vuln_date
            else group.created_date
        )
        current_date = datetime_utils.get_utc_now()

        self.cert_context = {
            "business": group.business_name or "",
            "business_number": group.business_id or "",
            "remediation_table": remediation_table,
            "start_day": str(start_date.day),
            "start_month": resolve_month_name(self.lang, start_date, words),
            "start_year": str(start_date.year),
            "start_ordinal_ending": get_ordinal_ending(start_date.day),
            "report_day": str(current_date.day),
            "report_month": resolve_month_name(self.lang, current_date, words),
            "report_year": str(current_date.year),
            "report_ordinal_ending": get_ordinal_ending(current_date.day),
            "solution": description,
            "signature_img": "placeholder value",
            "words": words,
        }

    async def cert(  # noqa
        self,
        findings: tuple[Finding, ...],
        group_name: str,
        description: str,
        loaders: Dataloaders,
    ) -> None:
        """Create the template to render and apply the context."""
        await self.fill_context(findings, group_name, description, loaders)
        self.out_name = f"{str(uuid.uuid4())}.pdf"
        searchpath = self.path
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(
            loader=template_loader,
            autoescape=select_autoescape(["html", "xml"], default=True),
        )
        template = template_env.get_template(self.proj_tpl)
        tpl_name = f"{self.tpl_dir}{group_name}_CERT.tpl"
        # Fetch signature resource
        with tempfile.NamedTemporaryFile(mode="w+") as file:
            await s3_ops.download_file(
                "resources/certificate/signature.png",
                file.name,
            )
            self.cert_context[
                "signature_img"
            ] = f"image::{file.name}[Signature,180,45]"
            render_text = template.render(self.cert_context)
            with open(tpl_name, "wb") as tplfile:
                tplfile.write(render_text.encode("utf-8"))
            self.create_command(tpl_name, self.out_name)
            subprocess.call(self.command, shell=True)  # nosec
