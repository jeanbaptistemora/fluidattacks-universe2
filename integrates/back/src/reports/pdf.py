from .typing import (
    PDFWordlistEn,
)
from context import (
    BASE_URL,
    STARTDIR,
)
from custom_types import (
    Finding as FindingType,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from decimal import (
    Decimal,
)
import importlib
import jinja2
from jinja2 import (
    select_autoescape,
)
import logging
import logging.config
import matplotlib
from newutils.vulnerabilities import (
    get_treatments,
)
from pylab import (  # noqa
    axis,
    cla,
    clf,
    close,
    figure,
    pie,
    savefig,
)
from settings import (
    LOGGING,
)
import subprocess  # nosec
import sys
import time
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)
from typing_extensions import (
    TypedDict,
)
import uuid

# FP: local testing
logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
VulnTable = TypedDict(  # pylint: disable=invalid-name
    "VulnTable",
    {
        "resume": List[List[Union[float, int, str]]],
        "top": List[List[Union[int, str]]],
        "num_reg": int,
    },
)
Context = TypedDict(  # pylint: disable=invalid-name
    "Context",
    {
        "full_group": str,
        "team": str,
        "team_mail": str,
        "customer": str,
        "toe": str,
        "version": str,
        "revdate": str,
        "simpledate": str,
        "fluid_tpl": Dict[str, str],
        "main_pie_filename": str,
        "main_tables": VulnTable,
        "findings": List[Dict[str, FindingType]],
        "accessVector": Optional[str],
        "finding_title": str,
        "finding_section_title": str,
        "where_title": str,
        "description_title": str,
        "resume_vuln_title": str,
        "resume_perc_title": str,
        "resume_regi_title": str,
        "resume_vnum_title": str,
        "resume_vname_title": str,
        "resume_ttab_title": str,
        "resume_top_title": str,
        "risk_title": str,
        "evidence_title": str,
        "records_title": str,
        "threat_title": str,
        "solution_title": str,
        "requisite_title": str,
        "treatment_title": str,
        "severity_title": str,
        "cardinality_title": str,
        "attack_vector_title": str,
        "compromised_system_title": str,
        "resume_page_title": str,
        "resume_table_title": str,
        "state_title": str,
        "commit_hash": str,
        "crit_h": str,
        "crit_m": str,
        "crit_l": str,
        "field": str,
        "inputs": str,
        "line": str,
        "lines": str,
        "path": str,
        "port": str,
        "ports": str,
        "user": str,
        "date": str,
        "link": str,
    },
)


def get_access_vector(finding: Dict[str, FindingType]) -> Optional[str]:
    """Get metrics based on cvss version."""
    if finding.get("cvssVersion") == "3.1":
        severity = get_severity("attackVector", finding["attackVector"])
    else:
        severity = get_severity("accessVector", finding["accessVector"])
    return severity


def get_access_vector_new(finding: Finding) -> Optional[str]:
    """Get metrics based on cvss version."""
    if isinstance(finding.severity, Finding31Severity):
        severity = get_severity_new(
            "attack_vector", finding.severity.attack_vector
        )
    else:
        severity = get_severity_new(
            "access_vector", finding.severity.access_vector
        )
    return severity


def get_severity(metric: str, metric_value: str) -> Optional[str]:
    """Extract number of CSSV2 metrics."""
    description: Optional[str] = ""
    try:
        metrics = {
            "accessVector": {
                "0.395": "Local",
                "0.646": "Red adyacente",
                "1.0": "Red",
            },
            "attackVector": {
                "0.85": "Red",
                "0.62": "Red adyacente",
                "0.55": "Local",
                "0.20": "Físico",
            },
            "confidentialityImpact": {
                "0.0": "Ninguno",
                "0.275": "Parcial",
                "0.66": "Completo",
            },
            "integrityImpact": {
                "0.0": "Ninguno",
                "0.275": "Parcial",
                "0.66": "Completo",
            },
            "availabilityImpact": {
                "0.0": "Ninguno",
                "0.275": "Parcial",
                "0.66": "Completo",
            },
            "authentication": {
                "0.45": "Múltiple",
                "0.56": "Única",
                "0.704": "Ninguna",
            },
            "exploitability": {
                "0.85": "Improbable",
                "0.9": "Conceptual",
                "0.95": "Funcional",
                "1.0": "Alta",
            },
            "confidenceLevel": {
                "0.9": "No confirmado",
                "0.95": "No corroborado",
                "1.0": "Confirmado",
            },
            "resolutionLevel": {
                "0.87": "Oficial",
                "0.9": "Temporal",
                "0.95": "Paliativa",
                "1.0": "Inexistente",
            },
            "accessComplexity": {
                "0.35": "Alto",
                "0.61": "Medio",
                "0.71": "Bajo",
            },
        }
        metric_descriptions = metrics.get(metric)
        if metric_descriptions:
            description = metric_descriptions.get(str(metric_value))
    except ValueError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return description


def get_severity_new(metric: str, metric_value: Decimal) -> Optional[str]:
    """Extract number of CSSV metrics."""
    description: Optional[str] = ""
    metrics = {
        "access_vector": {
            Decimal("0.395"): "Local",
            Decimal("0.646"): "Red adyacente",
            Decimal("1.0"): "Red",
        },
        "attack_vector": {
            Decimal("0.85"): "Red",
            Decimal("0.62"): "Red adyacente",
            Decimal("0.55"): "Local",
            Decimal("0.20"): "Físico",
        },
        "confidentiality_impact": {
            Decimal("0.0"): "Ninguno",
            Decimal("0.275"): "Parcial",
            Decimal("0.66"): "Completo",
        },
        "integrity_impact": {
            Decimal("0.0"): "Ninguno",
            Decimal("0.275"): "Parcial",
            Decimal("0.66"): "Completo",
        },
        "availability_impact": {
            Decimal("0.0"): "Ninguno",
            Decimal("0.275"): "Parcial",
            Decimal("0.66"): "Completo",
        },
        "authentication": {
            Decimal("0.45"): "Múltiple",
            Decimal("0.56"): "Única",
            Decimal("0.704"): "Ninguna",
        },
        "exploitability": {
            Decimal("0.85"): "Improbable",
            Decimal("0.9"): "Conceptual",
            Decimal("0.95"): "Funcional",
            Decimal("1.0"): "Alta",
        },
        "confidence_level": {
            Decimal("0.9"): "No confirmado",
            Decimal("0.95"): "No corroborado",
            Decimal("1.0"): "Confirmado",
        },
        "resolution_level": {
            Decimal("0.87"): "Oficial",
            Decimal("0.9"): "Temporal",
            Decimal("0.95"): "Paliativa",
            Decimal("1.0"): "Inexistente",
        },
        "access_complexity": {
            Decimal("0.35"): "Alto",
            Decimal("0.61"): "Medio",
            Decimal("0.71"): "Bajo",
        },
    }
    metric_descriptions = metrics.get(metric)
    if metric_descriptions:
        description = metric_descriptions.get(metric_value)

    return description


def make_vuln_table(
    findings: List[Dict[str, FindingType]], words: Dict[str, str]
) -> VulnTable:
    """Label findings percent quantity."""
    vuln_table: List[List[Union[float, int, str]]] = [
        [words["vuln_c"], 0, 0, 0],
        [words["vuln_h"], 0, 0, 0],
        [words["vuln_m"], 0, 0, 0],
        [words["vuln_l"], 0, 0, 0],
        ["Total", len(findings), "100.00%", 0],
    ]
    top_table = []
    ttl_vulns, ttl_num_reg, top = 0, 0, 1
    for finding in findings:
        severity = finding["severityCvss"]
        crit_as_text = words["crit_l"]
        vuln_amount = 0
        if finding["openVulnerabilities"] != "-":
            vuln_amount = int(finding["openVulnerabilities"])
        ttl_vulns += vuln_amount
        if 9.0 <= severity <= 10.0:
            vuln_table[0][1] = int(vuln_table[0][1]) + 1
            vuln_table[0][3] = int(vuln_table[0][3]) + vuln_amount
            crit_as_text = words["crit_c"]
        elif 7.0 <= severity <= 8.9:
            vuln_table[1][1] = int(vuln_table[1][1]) + 1
            vuln_table[1][3] = int(vuln_table[1][3]) + vuln_amount
            crit_as_text = words["crit_h"]
        elif 4.0 <= severity <= 6.9:
            vuln_table[2][1] = int(vuln_table[2][1]) + 1
            vuln_table[2][3] = int(vuln_table[2][3]) + vuln_amount
            crit_as_text = words["crit_m"]
        else:
            vuln_table[3][1] = int(vuln_table[3][1]) + 1
            vuln_table[3][3] = int(vuln_table[3][3]) + vuln_amount
        ttl_num_reg += int(finding.get("recordsNumber", 0))
        finding["severityCvss"] = str(finding["severityCvss"])
        if top <= 5:
            top_table.append(
                [
                    top,
                    f'{finding["severityCvss"]} {crit_as_text}',
                    finding["finding"],
                ]
            )
            top += 1
    number_of_findings: float = float(len(findings))
    vuln_table[0][2] = float(
        int(vuln_table[0][1]) * 100 / number_of_findings
        if number_of_findings != 0
        else 0.0
    )
    vuln_table[1][2] = float(
        int(vuln_table[1][1]) * 100 / number_of_findings
        if number_of_findings != 0
        else 0.0
    )
    vuln_table[2][2] = float(
        int(vuln_table[2][1]) * 100 / number_of_findings
        if number_of_findings != 0
        else 0.0
    )
    vuln_table[3][2] = float(
        int(vuln_table[3][1]) * 100 / number_of_findings
        if number_of_findings != 0
        else 0.0
    )
    vuln_table[0][2] = "{0:.2f}%".format(float(vuln_table[0][2]))
    vuln_table[1][2] = "{0:.2f}%".format(float(vuln_table[1][2]))
    vuln_table[2][2] = "{0:.2f}%".format(float(vuln_table[2][2]))
    vuln_table[3][2] = "{0:.2f}%".format(float(vuln_table[3][2]))
    vuln_table[4][3] = ttl_vulns
    return {"resume": vuln_table, "top": top_table, "num_reg": ttl_num_reg}


# pylint: disable=too-many-instance-attributes
class CreatorPDF:
    """Class to generate reports in PDF."""

    command: str = ""
    context: Optional[Context] = None
    doctype: str = "executive"
    font_dir: str = "/resources/fonts"
    lang: str = "en"
    out_name: str = ""
    proj_tpl: str = "templates/pdf/executive.adoc"
    result_dir: str = "/results/results_pdf/"
    style: str = "fluid"
    style_dir: str = "/resources/themes"
    tpl_dir: str = "/tpls/"
    wordlist: Dict[str, Dict[str, str]] = {}

    def __init__(self, lang: str, doctype: str, tempdir: str) -> None:
        """Class constructor."""
        self.path = f"{STARTDIR}/integrates/back/src/reports"
        self.tpl_img_path = tempdir

        self.doctype = doctype
        self.font_dir = self.path + self.font_dir
        self.lang = lang
        self.result_dir = self.path + self.result_dir
        self.tpl_dir = self.path + self.tpl_dir
        self.style_dir = self.path + self.style_dir
        if self.doctype == "tech":
            self.proj_tpl = "templates/pdf/tech.adoc"

        importlib.reload(sys)
        self.lang_support()

    def create_command(self, tpl_name: str) -> None:
        """Create the SO command to create the PDF with asciidoctor."""
        self.command = (
            "asciidoctor-pdf "
            f"-a pdf-stylesdir={self.style_dir} "
            f"-a pdf-style={self.style} "
            f"-a pdf-fontsdir={self.font_dir} "
            f"-D {self.result_dir} "
            f"-o {self.out_name} "
            f"{tpl_name} && chmod 777 {tpl_name}"
        )

    async def fill_group(  # noqa pylint: disable=too-many-arguments,too-many-locals
        self,
        findings: List[Dict[str, FindingType]],
        group: str,
        description: str,
        user: str,
        context: Any,
    ) -> None:
        """Add group information."""
        words = self.wordlist[self.lang]
        doctype = words[self.doctype]
        full_group = f"{description} [{group}]"
        team = "Engineering Team"
        version = "v1.0"
        team_mail = "engineering@fluidattacks.com"
        main_pie_filename = self.make_pie_finding(findings, group, words)
        finding_vulns_loader = context.finding_vulns_nzr
        vulnerabilities = await finding_vulns_loader.load_many(
            [finding["findingId"] for finding in findings]
        )
        for finding, vulns in zip(findings, vulnerabilities):
            treatment = get_treatments(vulns)
            treatments: List[str] = []
            if treatment.ACCEPTED > 0:
                treatments.append(
                    f'{words["treat_status_asu"]}: {treatment.ACCEPTED}'
                )
            if treatment.ACCEPTED_UNDEFINED > 0:
                treatments.append(
                    f'{words["treat_ete_asu"]}: {treatment.ACCEPTED_UNDEFINED}'
                )
            if treatment.IN_PROGRESS > 0:
                treatments.append(
                    f'{words["treat_status_rem"]}: {treatment.IN_PROGRESS}'
                )
            if treatment.NEW > 0:
                treatments.append(
                    f'{words["treat_status_wor"]}: {treatment.NEW}'
                )

            if int(finding["openVulnerabilities"]) > 0:
                finding["state"] = words["fin_status_open"]
                finding["treatment"] = "\n".join(sorted(treatments))
            else:
                finding["state"] = words["fin_status_closed"]
                finding["treatment"] = "-"

        main_pie_filename = (
            f"image::{main_pie_filename}[width=300, align=center]"
        )
        main_tables = make_vuln_table(findings, words)
        fluid_tpl_content = self.make_content(words)
        access_vector = get_access_vector(findings[0]) if findings else ""
        self.context = {
            "full_group": full_group.upper(),
            "team": team,
            "team_mail": team_mail,
            "customer": "",
            "toe": description,
            "version": version,
            "revdate": f'{doctype} {time.strftime("%d/%m/%Y")}',
            "simpledate": time.strftime("%Y.%m.%d"),
            "fluid_tpl": fluid_tpl_content,
            "main_pie_filename": main_pie_filename,
            "main_tables": main_tables,
            "findings": findings,
            "accessVector": access_vector,
            # Titulos segun lenguaje
            "finding_title": words["finding_title"],
            "finding_section_title": words["finding_section_title"],
            "where_title": words["where_title"],
            "description_title": words["description_title"],
            "resume_vuln_title": words["resume_vuln_title"],
            "resume_perc_title": words["resume_perc_title"],
            "resume_regi_title": words["resume_regi_title"],
            "resume_vnum_title": words["resume_vnum_title"],
            "resume_vname_title": words["resume_vname_title"],
            "resume_ttab_title": words["resume_ttab_title"],
            "resume_top_title": words["resume_top_title"],
            "risk_title": words["risk_title"],
            "evidence_title": words["evidence_title"],
            "records_title": words["records_title"],
            "threat_title": words["threat_title"],
            "solution_title": words["solution_title"],
            "requisite_title": words["requisite_title"],
            "treatment_title": words["treatment_title"],
            "severity_title": words["severity_title"],
            "cardinality_title": words["cardinality_title"],
            "attack_vector_title": words["attack_vector_title"],
            "compromised_system_title": words["compromised_system_title"],
            "resume_page_title": words["resume_page_title"],
            "resume_table_title": words["resume_table_title"],
            "state_title": words["state_title"],
            "commit_hash": words["commit_hash"],
            "crit_h": words["crit_h"],
            "crit_m": words["crit_m"],
            "crit_l": words["crit_l"],
            "field": words["field"],
            "inputs": words["inputs"],
            "line": words["line"],
            "lines": words["lines"],
            "path": words["path"],
            "port": words["port"],
            "ports": words["ports"],
            "user": user,
            "date": time.strftime("%Y-%m-%d at %H:%M"),
            "link": f"{BASE_URL}/groups/{group}/vulns",
        }

    def lang_support(self) -> None:
        """Define the dictionaries of accepted languages."""
        self.wordlist = dict()
        self.lang_support_en()

    def lang_support_en(self) -> None:
        """Add the English dictionary."""
        self.wordlist["en"] = dict(
            zip(PDFWordlistEn.keys(), PDFWordlistEn.labels())
        )

    def make_content(self, words: Dict[str, str]) -> Dict[str, str]:
        """Create context with the titles of the document."""
        base_img = "image::../templates/pdf/{name}_{lang}.png[]"
        base_adoc = "include::../templates/pdf/{name}_{lang}.adoc[]"
        return {
            "content_title": words["content_title"],
            "content_list": words["content_list"],
            "goals_title": words["goals_title"],
            "goals_img": base_img.format(name="goals", lang=self.lang),
            "severity_img": base_img.format(name="severity", lang=self.lang),
            "metodology_title": words["metodology_title"],
            "metodology_img": base_img.format(
                name="metodology", lang=self.lang
            ),
            "footer_adoc": base_adoc.format(name="footer", lang=self.lang),
        }

    def make_pie_finding(
        self,
        findings: List[Dict[str, FindingType]],
        group: str,
        words: Dict[str, str],
    ) -> str:
        """Create the findings graph."""
        figure(1, figsize=(6, 6))
        finding_state_pie = [0, 0, 0, 0]  # A, PC, C
        finding_state_pielabels = [
            words["vuln_c"],
            words["vuln_h"],
            words["vuln_m"],
            words["vuln_l"],
        ]
        colors = ["#980000", "red", "orange", "yellow"]
        explode = (0.1, 0, 0, 0)
        for finding in findings:
            severity = finding["severityCvss"]
            if 9.0 <= severity <= 10.0:
                finding_state_pie[0] += 1
            elif 7.0 <= severity <= 8.9:
                finding_state_pie[1] += 1
            elif 4.0 <= severity <= 6.9:
                finding_state_pie[2] += 1
            elif 0.0 <= severity <= 3.9:  # Abierto por defecto
                finding_state_pie[3] += 1
            else:
                finding_state_pie[3] += 1
        pie(
            finding_state_pie,
            explode=explode,
            labels=finding_state_pielabels,
            autopct="%1.0f%%",
            startangle=90,
            colors=colors,
        )
        axis("equal")
        pie_filename = f"{self.tpl_img_path}/finding_graph_{group}.png"
        savefig(pie_filename, bbox_inches="tight", transparent=True, dpi=100)
        cla()
        clf()
        close("all")
        return pie_filename

    async def tech(  # noqa pylint: disable=too-many-arguments
        self,
        data: List[Dict[str, FindingType]],
        group: str,
        description: str,
        user: str,
        context: Any,
    ) -> None:
        """Create the template to render and apply the context."""
        await self.fill_group(data, group, description, user, context)
        self.out_name = f"{str(uuid.uuid4())}.pdf"
        searchpath = self.path
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(
            loader=template_loader,
            autoescape=select_autoescape(["html", "xml"], default=True),
        )
        template = template_env.get_template(self.proj_tpl)
        tpl_name = f"{self.tpl_dir}{group}_IT.tpl"
        render_text = template.render(self.context)
        with open(tpl_name, "wb") as tplfile:
            tplfile.write(render_text.encode("utf-8"))
        self.create_command(tpl_name)
        subprocess.call(self.command, shell=True)


class CreatorPdfNew:
    """Class to generate reports in PDF."""

    command: str = ""
    context: Optional[Context] = None
    doctype: str = "executive"
    font_dir: str = "/resources/fonts"
    lang: str = "en"
    out_name: str = ""
    proj_tpl: str = "templates/pdf/executive_new.adoc"
    result_dir: str = "/results/results_pdf/"
    style: str = "fluid"
    style_dir: str = "/resources/themes"
    tpl_dir: str = "/tpls/"
    wordlist: Dict[str, Dict[str, str]] = {}

    def __init__(self, lang: str, doctype: str, tempdir: str) -> None:
        """Class constructor."""
        self.path = f"{STARTDIR}/integrates/back/src/reports"
        self.tpl_img_path = tempdir

        self.doctype = doctype
        self.font_dir = self.path + self.font_dir
        self.lang = lang
        self.result_dir = self.path + self.result_dir
        self.tpl_dir = self.path + self.tpl_dir
        self.style_dir = self.path + self.style_dir
        if self.doctype == "tech":
            self.proj_tpl = "templates/pdf/tech.adoc"

        importlib.reload(sys)
        self.lang_support()

    def create_command(self, tpl_name: str) -> None:
        """Create the SO command to create the PDF with asciidoctor."""
        self.command = (
            "asciidoctor-pdf "
            f"-a pdf-stylesdir={self.style_dir} "
            f"-a pdf-style={self.style} "
            f"-a pdf-fontsdir={self.font_dir} "
            f"-D {self.result_dir} "
            f"-o {self.out_name} "
            f"{tpl_name} && chmod 777 {tpl_name}"
        )

    def lang_support(self) -> None:
        """Define the dictionaries of accepted languages."""
        self.wordlist = dict()
        self.lang_support_en()

    def lang_support_en(self) -> None:
        """Add the English dictionary."""
        self.wordlist["en"] = dict(
            zip(PDFWordlistEn.keys(), PDFWordlistEn.labels())
        )

    def make_content(self, words: Dict[str, str]) -> Dict[str, str]:
        """Create context with the titles of the document."""
        base_img = "image::../templates/pdf/{name}_{lang}.png[]"
        base_adoc = "include::../templates/pdf/{name}_{lang}.adoc[]"
        return {
            "content_title": words["content_title"],
            "content_list": words["content_list"],
            "goals_title": words["goals_title"],
            "goals_img": base_img.format(name="goals", lang=self.lang),
            "severity_img": base_img.format(name="severity", lang=self.lang),
            "metodology_title": words["metodology_title"],
            "metodology_img": base_img.format(
                name="metodology", lang=self.lang
            ),
            "footer_adoc": base_adoc.format(name="footer", lang=self.lang),
        }
