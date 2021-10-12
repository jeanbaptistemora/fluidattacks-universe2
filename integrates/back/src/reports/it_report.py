from .typing import (
    GroupVulnsReportHeader,
)
from custom_types import (
    Historic as HistoricType,
    Vulnerability as VulnType,
)
from datetime import (
    datetime,
)
from dateutil.parser import (  # type: ignore
    parse,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingVerification,
)
from findings import (
    domain as findings_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from pyexcelerate import (
    Alignment,
    Color,
    Format,
    Style,
    Workbook,
    Worksheet as WorksheetType,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Tuple,
    Union,
)

EMPTY = "-"
HEADER_HEIGHT = 20
ROW_HEIGHT = 57
RED = Color(255, 52, 53, 1)  # FF3435
WHITE = Color(255, 255, 255, 1)


def get_formatted_last_date(
    historic_state: HistoricType,
) -> Union[str, datetime]:
    curr_trtmnt_date: Union[str, datetime] = EMPTY
    if historic_state and "date" in cast(HistoricType, historic_state)[-1]:
        last_date = str(cast(HistoricType, historic_state)[-1]["date"])
        curr_trtmnt_date = datetime_utils.get_from_str(
            datetime_utils.get_as_str(parse(last_date))
        )
    return curr_trtmnt_date


# pylint: disable=too-many-instance-attributes
class ITReportNew:
    """Class to generate IT reports."""

    current_sheet: WorksheetType = None
    cvss_measures = {
        "AV": "attack_vector",
        "AC": "attack_complexity",
        "PR": "privileges_required",
        "UI": "user_interaction",
        "S": "severity_scope",
        "C": "confidentiality_impact",
        "I": "integrity_impact",
        "A": "availability_impact",
        "E": "exploitability",
        "RL": "remediation_level",
        "RC": "report_confidence",
    }
    data: Tuple[Finding, ...] = tuple()
    lang = None
    result_filename = ""
    row = 1
    vulnerability = {
        col_name: index + 1
        for index, col_name in enumerate(GroupVulnsReportHeader.labels())
    }
    workbook: Workbook

    row_values: List[Union[str, int, float, datetime]] = [
        EMPTY for _ in range(len(vulnerability) + 1)
    ]

    def __init__(
        self,
        data: Tuple[Finding, ...],
        group_name: str,
        loaders: Any,
        lang: str = "es",
    ) -> None:
        """Initialize variables."""
        self.data = data
        self.finding_historic_verification_loader = (
            loaders.finding_historic_verification_new
        )
        self.finding_vulns_loader = loaders.finding_vulns_nzr
        self.group_name = group_name
        self.lang = lang

        self.workbook = Workbook()
        self.current_sheet = self.workbook.new_sheet("Data")
        self.parse_template()

    async def create(self) -> None:
        await self.generate(self.data)
        self.style_sheet()
        self.save()

    async def generate(self, data: Tuple[Finding, ...]) -> None:
        for finding in data:
            finding_vulns = await self.finding_vulns_loader.load(finding.id)
            for vuln in finding_vulns:
                await self.set_vuln_row(cast(VulnType, vuln), finding)
                self.row += 1

    @staticmethod
    def get_measure(metric: str, metric_value: str) -> str:
        """Extract number of CSSV metrics."""
        metrics = {
            "attack_vector": {
                "0.85": "Network",
                "0.62": "Adjacent",
                "0.55": "Local",
                "0.20": "Physical",
            },
            "attack_complexity": {
                "0.77": "Low",
                "0.44": "High",
            },
            "privileges_required": {
                "0.85": "None",
                "0.62": "Low",
                "0.68": "Low",
                "0.27": "High",
                "0.50": "High",
            },
            "user_interaction": {
                "0.85": "None",
                "0.62": "Required",
            },
            "severity_scope": {
                "0.0": "Unchanged",
                "1.0": "Changed",
            },
            "confidentiality_impact": {
                "0.56": "High",
                "0.22": "Low",
                "0.0": "None",
            },
            "integrity_impact": {
                "0.56": "High",
                "0.22": "Low",
                "0.0": "None",
            },
            "availability_impact": {
                "0.56": "High",
                "0.22": "Low",
                "0.0": "None",
            },
            "exploitability": {
                "0.91": "Unproven",
                "0.94": "Proof of concept",
                "0.97": "Functional",
                "1.0": "High",
            },
            "remediation_level": {
                "0.95": "Official Fix",
                "0.96": "Temporary Fix",
                "0.97": "Workaround",
                "1.0": "Unavailable",
            },
            "report_confidence": {
                "0.92": "Unknown",
                "0.96": "Reasonable",
                "1.0": "Confirmed",
            },
        }
        metric_descriptions = metrics.get(metric, {})
        description = metric_descriptions.get(str(metric_value), EMPTY)
        return description

    @classmethod
    def get_row_range(cls, row: int) -> List[str]:
        return [f"A{row}", f"AY{row}"]

    def parse_template(self) -> None:
        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            list(self.vulnerability.keys())
        ]
        self.row += 1

    def save(self) -> None:
        today_date = datetime_utils.get_as_str(
            datetime_utils.get_now(), date_format="%Y-%m-%dT%H-%M-%S"
        )
        self.result_filename = (
            f"{self.group_name}-vulnerabilities-{today_date}.xlsx"
        )
        self.workbook.save(self.result_filename)

    def set_cvss_metrics_cell(self, row: Finding) -> None:
        metric_vector = []
        vuln = self.vulnerability
        cvss_key = "CVSSv3.1 string vector"
        is_31_severity = isinstance(row.severity, Finding31Severity)
        for ind, (indicator, measure) in enumerate(self.cvss_measures.items()):
            value = EMPTY
            if is_31_severity:
                value = self.get_measure(
                    measure, getattr(row.severity, measure)
                )

            self.row_values[vuln[cvss_key] + ind + 1] = value
            if value != EMPTY:
                metric_vector.append(f"{indicator}:{value[0]}")

        cvss_metric_vector = "/".join(metric_vector)
        cvss_calculator_url = (
            "https://www.first.org/cvss/calculator/3.1#CVSS:3.1"
            f"/{cvss_metric_vector}"
        )
        cell_content = (
            f'=HYPERLINK("{cvss_calculator_url}", "{cvss_metric_vector}")'
        )
        self.row_values[vuln[cvss_key]] = cell_content

    def set_finding_data(self, finding: Finding, vuln: VulnType) -> None:
        severity = float(
            findings_domain.get_severity_score_new(finding.severity)
        )
        finding_data = {
            "Description": finding.description,
            "Status": cast(HistoricType, vuln.get("historic_state"))[-1][
                "state"
            ],
            "Severity": severity or EMPTY,
            "Requirements": finding.requirements,
            "Impact": finding.attack_vector_description,
            "Affected System": finding.affected_systems,
            "Threat": finding.threat,
            "Recommendation": finding.recommendation,
            "Compromised Attributes": finding.compromised_attributes,
            "# Compromised records": str(finding.compromised_records),
        }
        for key, value in finding_data.items():
            self.row_values[self.vulnerability[key]] = value

    async def set_reattack_data(
        self, finding: Finding, vuln: VulnType
    ) -> None:
        historic_verification: Tuple[
            FindingVerification, ...
        ] = await self.finding_historic_verification_loader.load(finding.id)
        vuln_closed = (
            cast(HistoricType, vuln.get("historic_state"))[-1]["state"]
            == "closed"
        )
        reattack_requested = None
        reattack_date = None
        reattack_requester = None
        n_requested_reattacks = None
        remediation_effectiveness = EMPTY
        if historic_verification:
            reattack_requested = (
                finding.verification.status
                == FindingVerificationStatus.REQUESTED
            )
            n_requested_reattacks = len(
                [
                    verification
                    for verification in historic_verification
                    if verification.status
                    == FindingVerificationStatus.REQUESTED
                ]
            )
            if vuln_closed:
                remediation_effectiveness = f"{100 / n_requested_reattacks}%"
            if reattack_requested:
                reattack_date = datetime_utils.as_zone(
                    datetime.fromisoformat(finding.verification.modified_date)
                )
                reattack_requester = finding.verification.modified_by
        reattack_data = {
            "Pending Reattack": "Yes" if reattack_requested else "No",
            "# Requested Reattacks": n_requested_reattacks or "0",
            "Last requested reattack": reattack_date or EMPTY,
            "Last reattack Requester": reattack_requester or EMPTY,
            "Remediation Effectiveness": remediation_effectiveness,
        }
        for key, value in reattack_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_row_height(self) -> None:
        self.current_sheet.set_row_style(
            self.row,
            Style(size=ROW_HEIGHT, alignment=Alignment(wrap_text=True)),
        )

        # this makes that the cells for severity get the rigth format
        self.current_sheet.set_cell_style(
            self.row,
            9,
            Style(
                size=ROW_HEIGHT,
                alignment=Alignment(wrap_text=True),
                format=Format(0.0),
            ),
        )

    def set_treatment_data(  # pylint: disable=too-many-locals
        self, vuln: VulnType
    ) -> None:
        def format_treatment(treatment: str) -> str:
            treatment = treatment.capitalize().replace("_", " ")
            if treatment == "Accepted undefined":
                treatment = "Permanently accepted"
            elif treatment == "Accepted":
                treatment = "Temporarily accepted"
            return treatment

        is_vuln_open: bool = vuln["current_state"] == "open"
        historic_treatment = cast(
            HistoricType, vuln.get("historic_treatment", [{}])
        )
        curr_trtmnt_date: Union[str, datetime] = get_formatted_last_date(
            historic_treatment
        )
        current_treatment_exp_date: Union[str, datetime] = EMPTY
        first_treatment_exp_date: Union[str, datetime] = EMPTY
        current_treatment = historic_treatment[-1]
        first_treatment_state = historic_treatment[0]
        if current_treatment.get("acceptance_date"):
            current_treatment_exp_date = datetime_utils.get_from_str(
                str(current_treatment["acceptance_date"])
            )
        if first_treatment_state.get("acceptance_date"):
            first_treatment_exp_date = datetime_utils.get_from_str(
                str(first_treatment_state["acceptance_date"])
            )

        current_treatment_data: Dict[str, Union[str, int, float, datetime]] = {
            "Current Treatment": format_treatment(
                str(current_treatment.get("treatment", "NEW"))
            ),
            "Current Treatment Moment": curr_trtmnt_date,
            "Current Treatment Justification": str(
                current_treatment.get("justification", EMPTY)
            ),
            "Current Treatment expiration Moment": current_treatment_exp_date,
            "Current Treatment manager": str(
                current_treatment.get("treatment_manager", EMPTY)
            ),
        }
        first_treatment_data: Dict[str, Union[str, int, float, datetime]] = {
            "First Treatment": str(
                format_treatment(first_treatment_state.get("treatment", "NEW"))
            ),
            "First Treatment Moment": get_formatted_last_date(
                [first_treatment_state]
            ),
            "First Treatment Justification": str(
                first_treatment_state.get("justification", EMPTY)
            ),
            "First Treatment expiration Moment": first_treatment_exp_date,
            "First Treatment manager": str(
                first_treatment_state.get("treatment_manager", EMPTY)
            ),
        }
        for key, value in current_treatment_data.items():
            self.row_values[self.vulnerability[key]] = (
                value if is_vuln_open else EMPTY
            )
            first_treatment_key = key.replace("Current", "First")
            kword = self.vulnerability[first_treatment_key]
            self.row_values[kword] = first_treatment_data[first_treatment_key]

    async def set_vuln_row(self, row: VulnType, finding: Finding) -> None:
        vuln = self.vulnerability
        specific = str(row.get("specific", ""))
        if row.get("vuln_type") == "lines":
            specific = str(int(specific))

        commit = EMPTY
        if "commit_hash" in row:
            commit = row["commit_hash"][0:7]

        tags = EMPTY
        if "tag" in row:
            tags = row.get("tag", "")

        stream = EMPTY
        if "stream" in row:
            stream = row.get("stream", "")

        self.row_values[vuln["#"]] = self.row - 1
        self.row_values[vuln["Related Finding"]] = finding.title
        self.row_values[vuln["Finding Id"]] = finding.id
        self.row_values[vuln["Vulnerability Id"]] = str(row.get("UUID", EMPTY))
        self.row_values[vuln["Where"]] = str(row.get("where"))
        self.row_values[vuln["Specific"]] = specific
        self.row_values[vuln["Commit Hash"]] = commit
        self.row_values[vuln["Tags"]] = tags
        self.row_values[vuln["Stream"]] = stream

        self.set_finding_data(finding, row)
        self.set_vuln_temporal_data(row)
        self.set_treatment_data(row)
        await self.set_reattack_data(finding, row)
        self.set_cvss_metrics_cell(finding)

        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            self.row_values[1:]
        ]
        self.set_row_height()

    def set_vuln_temporal_data(self, vuln: VulnType) -> None:
        vuln_historic_state = cast(HistoricType, vuln.get("historic_state"))
        vuln_date = datetime_utils.get_from_str(vuln_historic_state[0]["date"])
        vuln_closed = vuln_historic_state[-1]["state"] == "closed"
        limit_date = datetime_utils.get_now()
        vuln_close_date: Union[str, datetime] = EMPTY
        if vuln_closed:
            limit_date = datetime_utils.get_from_str(
                vuln_historic_state[-1]["date"]
            )
            vuln_close_date = datetime_utils.get_from_str(
                vuln_historic_state[-1]["date"]
            )
        vuln_age_days = int((limit_date - vuln_date).days)
        external_bts = vuln.get("external_bts", EMPTY)

        vuln_temporal_data: Dict[str, Union[str, int, float, datetime]] = {
            "Report Moment": vuln_date,
            "Age in days": vuln_age_days,
            "Close Moment": vuln_close_date,
            "External BTS": f'=HYPERLINK("{external_bts}", "{external_bts}")',
        }
        for key, value in vuln_temporal_data.items():
            self.row_values[self.vulnerability[key]] = value

    def style_sheet(self) -> None:
        header = self.current_sheet.range(*self.get_row_range(1))
        header.style.fill.background = RED
        header.style.font.color = WHITE
        header.style.alignment.horizontal = "center"
        header.style.alignment.vertical = "center"
        header.style.alignment.wrap_text = True

        for column, col_width in enumerate(
            GroupVulnsReportHeader.widths(), start=1
        ):
            self.current_sheet.set_col_style(
                column,
                Style(size=col_width, alignment=Alignment(wrap_text=True)),
            )
