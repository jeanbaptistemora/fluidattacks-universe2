from .typing import (
    GroupVulnsReportHeader,
)
from aioextensions import (
    collect,
)
from datetime import (
    datetime,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingVerification,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
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
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

EMPTY = "-"
HEADER_HEIGHT = 20
ROW_HEIGHT = 57
RED = Color(255, 52, 53, 1)  # FF3435
WHITE = Color(255, 255, 255, 1)


# pylint: disable=too-many-instance-attributes
class ITReport:
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
    filters = None
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
        treatments: Set[VulnerabilityTreatmentStatus],
        loaders: Any,
    ) -> None:
        """Initialize variables."""
        self.data = data
        self.loaders = loaders
        self.group_name = group_name
        self.treatments = treatments

        self.workbook = Workbook()
        self.current_sheet = self.workbook.new_sheet("Data")
        self.parse_template()

    async def create(self) -> None:
        await self.generate(self.data)
        self.style_sheet()
        self.save()

    async def _get_findings_vulnerabilities(
        self, findings_ids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return (
            await self.loaders.finding_vulnerabilities_nzr.load_many_chained(
                findings_ids
            )
        )

    async def _get_findings_historics_verifications(
        self, findings_ids: Tuple[str, ...]
    ) -> Tuple[FindingVerification, ...]:
        return await self.loaders.finding_historic_verification.load_many(
            findings_ids
        )

    async def generate(self, data: Tuple[Finding, ...]) -> None:
        findings_ids = tuple(finding.id for finding in data)
        findings_vulnerabilities, findings_verifications = await collect(
            (
                self._get_findings_vulnerabilities(findings_ids),
                self._get_findings_historics_verifications(findings_ids),
            )
        )
        finding_data: Dict[str, Tuple[Finding]] = {
            finding.id: finding for finding in data
        }
        finding_verification: Dict[str, Tuple[FindingVerification]] = {
            finding.id: verification
            for finding, verification in zip(data, findings_verifications)
        }

        vulnerabilities_filtered: Tuple[Vulnerability, ...] = tuple(
            vulnerability
            for vulnerability in findings_vulnerabilities
            if vulnerability.treatment.status in self.treatments
        )
        vulnerabilities_historics: Tuple[
            Tuple[
                Tuple[VulnerabilityTreatment, ...],
                Tuple[VulnerabilityVerification, ...],
            ],
            ...,
        ] = await collect(
            tuple(
                self._get_vulnerability_data(vulnerability)
                for vulnerability in vulnerabilities_filtered
            ),
            workers=32,
        )

        for vulnerability, historics in zip(
            vulnerabilities_filtered, vulnerabilities_historics
        ):
            await self.set_vuln_row(
                vulnerability,
                finding_data[vulnerability.finding_id],
                historics[1],
                historics[0],
                finding_verification[vulnerability.finding_id],
            )
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
        if description == EMPTY:
            description = metric_descriptions.get(
                f"{Decimal(str(metric_value)):.1f}", EMPTY
            )

        return description

    @classmethod
    def get_row_range(cls, row: int) -> List[str]:
        # AX is the 50th column
        return [f"A{row}", f"AX{row}"]

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

    def set_finding_data(self, finding: Finding, vuln: Vulnerability) -> None:
        severity = float(findings_domain.get_severity_score(finding.severity))
        finding_data = {
            "Description": finding.description,
            "Status": vuln.state.status.value,
            "Severity": severity or EMPTY,
            "Requirements": finding.requirements,
            "Impact": finding.attack_vector_description,
            "Threat": finding.threat,
            "Recommendation": finding.recommendation,
        }
        for key, value in finding_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_reattack_data(
        self,
        vuln: Vulnerability,
        historic_verification: Tuple[VulnerabilityVerification, ...],
        finding_verification: Tuple[FindingVerification, ...],
    ) -> None:
        reattack_requested = None
        reattack_date = None
        reattack_requester = None
        n_requested_reattacks = None
        remediation_effectiveness: str = EMPTY
        if historic_verification:
            vuln_verification: VulnerabilityVerification = (
                historic_verification[-1]
            )
            reattack_requested = (
                vuln_verification.status
                == VulnerabilityVerificationStatus.REQUESTED
            )
            n_requested_reattacks = len(
                [
                    verification
                    for verification in historic_verification
                    if verification.status
                    == VulnerabilityVerificationStatus.REQUESTED
                ]
            )
            if vuln.state.status == VulnerabilityStateStatus.CLOSED:
                effectiveness: float = 100 / n_requested_reattacks
                remediation_effectiveness = (
                    f"{f'{effectiveness:.2f}'.rstrip('0').rstrip('.')}%"
                )
            if reattack_requested and vuln_verification.modified_date:
                reattack_date = datetime_utils.as_zone(
                    datetime.fromisoformat(vuln_verification.modified_date)
                )
                reattack_requester = self._get_reattack_requester(
                    vuln, finding_verification
                )
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

    def set_treatment_data(
        self,
        vuln: Vulnerability,
        historic_treatment: Tuple[VulnerabilityTreatment, ...],
    ) -> None:
        def get_first_treatment(
            treatments: Tuple[VulnerabilityTreatment, ...]
        ) -> Optional[VulnerabilityTreatment]:

            return next(
                (
                    treatment
                    for treatment in treatments
                    if treatment.status != VulnerabilityTreatmentStatus.NEW
                ),
                None,
            )

        def format_treatment(treatment: VulnerabilityTreatmentStatus) -> str:
            if treatment == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED:
                return "Permanently accepted"
            if treatment == VulnerabilityTreatmentStatus.ACCEPTED:
                return "Temporarily accepted"
            return treatment.value.capitalize().replace("_", " ")

        first_treatment = get_first_treatment(historic_treatment)
        current_treatment_exp_date: Union[str, datetime] = EMPTY
        if vuln.treatment.accepted_until:
            current_treatment_exp_date = datetime_utils.convert_from_iso_str(
                vuln.treatment.accepted_until
            )
        current_treatment_data = {
            "Current Treatment": format_treatment(vuln.treatment.status),
            "Current Treatment Moment": datetime_utils.convert_from_iso_str(
                vuln.treatment.modified_date
            ),
            "Current Treatment Justification": (
                vuln.treatment.justification or EMPTY
            ),
            "Current Treatment expiration Moment": current_treatment_exp_date,
            "Current Assigned": vuln.treatment.assigned or EMPTY,
        }
        first_treatment_data = {
            "First Treatment": EMPTY,
            "First Treatment Moment": EMPTY,
            "First Treatment Justification": EMPTY,
            "First Treatment expiration Moment": EMPTY,
            "First Assigned": EMPTY,
        }
        if first_treatment:
            first_expiration = EMPTY
            if (
                first_treatment.status == VulnerabilityTreatmentStatus.ACCEPTED
                and first_treatment.accepted_until
            ):
                first_expiration = datetime_utils.convert_from_iso_str(
                    first_treatment.accepted_until
                )
            first_treatment_data = {
                "First Treatment": format_treatment(first_treatment.status),
                "First Treatment Moment": datetime_utils.convert_from_iso_str(
                    first_treatment.modified_date
                ),
                "First Treatment Justification": first_treatment.justification
                or EMPTY,
                "First Treatment expiration Moment": first_expiration,
                "First Assigned": first_treatment.assigned or EMPTY,
            }

        for key, value in current_treatment_data.items():
            self.row_values[self.vulnerability[key]] = (
                value
                if vuln.state.status == VulnerabilityStateStatus.OPEN
                else EMPTY
            )
            first_treatment_key = key.replace("Current", "First")
            kword = self.vulnerability[first_treatment_key]
            self.row_values[kword] = first_treatment_data[first_treatment_key]

    async def _get_historic_treatment(
        self, vulnerability_id: str
    ) -> Tuple[VulnerabilityTreatment, ...]:
        return await self.loaders.vulnerability_historic_treatment.load(
            vulnerability_id
        )

    async def _get_historic_verification(
        self, vulnerability_id: str
    ) -> Tuple[VulnerabilityVerification, ...]:
        return await self.loaders.vulnerability_historic_verification.load(
            vulnerability_id
        )

    async def _get_vulnerability_data(
        self, vuln: Vulnerability
    ) -> Tuple[
        Tuple[VulnerabilityTreatment, ...],
        Tuple[VulnerabilityVerification, ...],
    ]:
        return await collect(
            (
                self._get_historic_treatment(vuln.id),
                self._get_historic_verification(vuln.id),
            )
        )

    @staticmethod
    def _get_reattack_requester(
        vuln: Vulnerability,
        historic_verification: Tuple[FindingVerification, ...],
    ) -> Optional[str]:
        reversed_historic_verification = tuple(reversed(historic_verification))
        for verification in reversed_historic_verification:
            if (
                verification.status == FindingVerificationStatus.REQUESTED
                and verification.vulnerability_ids is not None
                and vuln.id in verification.vulnerability_ids
            ):
                return verification.modified_by
        return None

    async def set_vuln_row(  # pylint: disable=too-many-arguments
        self,
        row: Vulnerability,
        finding: Finding,
        historic_verification: Tuple[VulnerabilityVerification, ...],
        historic_treatment: Tuple[VulnerabilityTreatment, ...],
        finding_verification: Tuple[FindingVerification, ...],
    ) -> None:
        vuln = self.vulnerability
        specific = row.specific
        if row.type == VulnerabilityType.LINES:
            specific = str(int(specific))

        commit = EMPTY
        if row.commit:
            commit = row.commit[0:7]

        tags = EMPTY
        if row.tags:
            tags = ", ".join(sorted(row.tags))

        stream = EMPTY
        if row.stream:
            stream = " > ".join(row.stream)

        nickname = EMPTY
        if row.root_id:
            root: RootItem = await self.loaders.root.load(
                (finding.group_name, row.root_id)
            )
            nickname = root.state.nickname

        self.row_values[vuln["#"]] = self.row - 1
        self.row_values[vuln["Related Finding"]] = finding.title
        self.row_values[vuln["Finding Id"]] = finding.id
        self.row_values[vuln["Vulnerability Id"]] = row.id
        self.row_values[vuln["Where"]] = row.where
        self.row_values[vuln["Specific"]] = specific
        self.row_values[vuln["Commit Hash"]] = commit
        self.row_values[vuln["Tags"]] = tags
        self.row_values[vuln["Stream"]] = stream
        self.row_values[vuln["Root Nickname"]] = nickname

        self.set_finding_data(finding, row)
        self.set_vuln_temporal_data(row)
        self.set_treatment_data(row, historic_treatment)
        self.set_reattack_data(
            row, historic_verification, finding_verification
        )
        self.set_cvss_metrics_cell(finding)

        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            self.row_values[1:]
        ]
        self.set_row_height()

    def set_vuln_temporal_data(self, vuln: Vulnerability) -> None:
        indicators = vuln.unreliable_indicators
        vuln_date = datetime.fromisoformat(indicators.unreliable_report_date)
        limit_date = datetime_utils.get_now()
        vuln_close_date: Union[str, datetime] = EMPTY
        if vuln.state.status == VulnerabilityStateStatus.CLOSED:
            limit_date = datetime.fromisoformat(vuln.state.modified_date)
            vuln_close_date = datetime.fromisoformat(vuln.state.modified_date)
        vuln_age_days = int((limit_date - vuln_date).days)
        external_bts = vuln.bug_tracking_system_url or EMPTY

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
