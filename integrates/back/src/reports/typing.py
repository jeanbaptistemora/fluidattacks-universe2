from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Tuple,
    Union,
)
from vulnerabilities.types import (
    GroupedVulnerabilitiesInfo,
)


# XLS reports types definitions
class ColumnConfig(NamedTuple):  # pylint: disable=too-few-public-methods
    label: str
    width: int = -1


class GenericHeader(Enum):
    @classmethod
    def labels(cls) -> List[str]:
        return [member.value.label for member in cls]

    @classmethod
    def widths(cls) -> List[int]:
        return [member.value.width for member in cls]


class GroupVulnsReportHeader(GenericHeader):
    NUMBER: ColumnConfig = ColumnConfig(label="#", width=4)
    FINDING: ColumnConfig = ColumnConfig(label="Related Finding", width=55)
    FINDING_ID: ColumnConfig = ColumnConfig(label="Finding Id", width=25)
    VULNERABILITY_ID: ColumnConfig = ColumnConfig(
        label="Vulnerability Id", width=50
    )
    WHERE: ColumnConfig = ColumnConfig(label="Where", width=45)
    STREAM: ColumnConfig = ColumnConfig(label="Stream", width=45)
    SPECIFIC: ColumnConfig = ColumnConfig(label="Specific", width=38)
    DESCRIPTION: ColumnConfig = ColumnConfig(label="Description", width=95)
    STATUS: ColumnConfig = ColumnConfig(label="Status", width=13)
    SEVERITY: ColumnConfig = ColumnConfig("Severity", width=13)
    REQUIREMENTS: ColumnConfig = ColumnConfig(label="Requirements", width=100)
    IMPACT: ColumnConfig = ColumnConfig(label="Impact", width=65)
    AFFECTED_SYSTEMS: ColumnConfig = ColumnConfig(
        label="Affected System", width=45
    )
    THREAT: ColumnConfig = ColumnConfig(label="Threat", width=55)
    RECOMMENDATION: ColumnConfig = ColumnConfig(
        label="Recommendation", width=100
    )
    EXTERNAL_BTS: ColumnConfig = ColumnConfig(label="External BTS", width=80)
    COMPROMISED_ATTRS: ColumnConfig = ColumnConfig(
        label="Compromised Attributes", width=35
    )
    N_COMPROMISED_RECORDS: ColumnConfig = ColumnConfig(
        label="# Compromised records", width=30
    )
    TAGS: ColumnConfig = ColumnConfig(label="Tags", width=60)
    BUSINESS_CRITICALLY: ColumnConfig = ColumnConfig(
        label="Business Critically", width=25
    )
    REPORT_MOMENT: ColumnConfig = ColumnConfig(label="Report Moment", width=25)
    CLOSE_MOMENT: ColumnConfig = ColumnConfig(label="Close Moment", width=25)
    AGE: ColumnConfig = ColumnConfig(label="Age in days", width=20)
    FIRST_TREATMENT: ColumnConfig = ColumnConfig(
        label="First Treatment", width=20
    )
    FIRST_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label="First Treatment Moment", width=25
    )
    FIRST_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label="First Treatment Justification", width=95
    )
    FIRST_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label="First Treatment expiration Moment", width=40
    )
    FIRST_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label="First Treatment manager", width=35
    )
    CURRENT_TREATMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment", width=20
    )
    CURRENT_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment Moment", width=25
    )
    CURRENT_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label="Current Treatment Justification", width=95
    )
    CURRENT_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment expiration Moment", width=40
    )
    CURRENT_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label="Current Treatment manager", width=35
    )
    PENDING_REATTACK: ColumnConfig = ColumnConfig(
        label="Pending Reattack", width=25
    )
    N_REQUESTED_REATTACKS: ColumnConfig = ColumnConfig(
        label="# Requested Reattacks", width=25
    )
    REMEDIATION_EFFECTIVENESS: ColumnConfig = ColumnConfig(
        label="Remediation Effectiveness", width=25
    )
    LAST_REQUESTED_REATTACK: ColumnConfig = ColumnConfig(
        label="Last requested reattack", width=25
    )
    LAST_REATTACK_REQUESTER: ColumnConfig = ColumnConfig(
        label="Last reattack Requester", width=35
    )
    CVSS_VECTOR: ColumnConfig = ColumnConfig(
        label="CVSSv3.1 string vector", width=55
    )
    ATTACK_VECTOR: ColumnConfig = ColumnConfig(label="Attack Vector", width=18)
    ATTACK_COMPLEXITY: ColumnConfig = ColumnConfig(
        label="Attack Complexity", width=20
    )
    PRIVILEGES_REQUIRED: ColumnConfig = ColumnConfig(
        label="Privileges Required", width=25
    )
    USER_INTERACTION: ColumnConfig = ColumnConfig(
        label="User Interaction", width=20
    )
    SEVERITY_SCOPE: ColumnConfig = ColumnConfig(
        label="Severity Scope", width=20
    )
    CONFIDENTIALITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Confidentiality Impact", width=23
    )
    INTEGRITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Integrity Impact", width=20
    )
    AVAILABILITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Availability Imapact", width=20
    )
    EXPLOITABILITY: ColumnConfig = ColumnConfig(
        label="Exploitability", width=18
    )
    REMEDIATION_LEVEL: ColumnConfig = ColumnConfig(
        label="Remediation Level", width=25
    )
    REPORT_CONFIDENCE: ColumnConfig = ColumnConfig(
        label="Report Confidence", width=25
    )
    COMMIT_HASH: ColumnConfig = ColumnConfig(label="Commit Hash", width=25)


# PDF report types definitions


class PdfFindingInfo(NamedTuple):  # pylint: disable=too-few-public-methods
    affected_systems: str
    attack_vector_description: str
    closed_vulnerabilities: int
    compromised_records: int
    description: str
    evidence_set: List[Dict[str, str]]
    grouped_inputs_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_ports_vulnerablities: Tuple[GroupedVulnerabilitiesInfo, ...]
    open_vulnerabilities: int
    recommendation: str
    requirements: str
    severity_score: Decimal
    state: str
    title: str
    threat: str
    treatment: str
    where: str


class WordlistItem(NamedTuple):  # pylint: disable=too-few-public-methods
    key: str
    label: Union[str, List[str]]


class Wordlist(Enum):
    @classmethod
    def keys(cls) -> List[str]:
        return [member.value.key for member in cls]

    @classmethod
    def labels(cls) -> List[str]:
        return [member.value.label for member in cls]


class PDFWordlistEn(Wordlist):
    FINDING_TITLE: WordlistItem = WordlistItem("finding_title", "Finding")
    FINDING_SECTION_TITLE: WordlistItem = WordlistItem(
        "finding_section_title", "Summary"
    )
    COMMIT_HASH: WordlistItem = WordlistItem("commit_hash", "Commit Hash")
    CONTENT_TITLE: WordlistItem = WordlistItem("content_title", "Content")
    CONTENT_LIST: WordlistItem = WordlistItem(
        "content_list",
        [
            "1. Goals",
            "2. Finding Table",
            "3. General View",
            "4. Findings Summary",
        ],
    )
    TECH: WordlistItem = WordlistItem("tech", "Technical Report")
    EXECUTIVE: WordlistItem = WordlistItem("executive", "Executive Report")
    GOALS_TITLE: WordlistItem = WordlistItem("goals_title", "Goals")
    METHODOLOGY_TITLE: WordlistItem = WordlistItem(
        "metodology_title", "Methodology"
    )
    STATE_TITLE: WordlistItem = WordlistItem("state_title", "Status")
    RECORDS_TITLE: WordlistItem = WordlistItem("records_title", "Records")
    DESCRIPTION_TITLE: WordlistItem = WordlistItem(
        "description_title", "Vulnerability"
    )
    FIELD: WordlistItem = WordlistItem("field", "Field")
    INPUTS: WordlistItem = WordlistItem("inputs", "Inputs")
    LINE: WordlistItem = WordlistItem("line", "Line")
    LINES: WordlistItem = WordlistItem("lines", "Lines")
    PATH: WordlistItem = WordlistItem("path", "Path")
    PORT: WordlistItem = WordlistItem("port", "Port")
    PORTS: WordlistItem = WordlistItem("ports", "Ports")
    RESUME_VULN_TITLE: WordlistItem = WordlistItem(
        "resume_vuln_title", "Vulnerabilities"
    )
    WHERE_TITLE: WordlistItem = WordlistItem("where_title", "Where")
    RESUME_PERC_TITLE: WordlistItem = WordlistItem(
        "resume_perc_title", "Percent"
    )
    RESUME_REGI_TITLE: WordlistItem = WordlistItem(
        "resume_regi_title", "Total Records"
    )
    RESUME_VNUM_TITLE: WordlistItem = WordlistItem("resume_vnum_title", "#")
    RESUME_VNAME_TITLE: WordlistItem = WordlistItem(
        "resume_vname_title", "Name"
    )
    RESUME_TTAB_TITLE: WordlistItem = WordlistItem("resume_ttab_title", "Name")
    RESUME_TOP_TITLE: WordlistItem = WordlistItem(
        "resume_top_title", "Finding Top"
    )
    THREAT_TITLE: WordlistItem = WordlistItem("threat_title", "Threat")
    SOLUCION_TITLE: WordlistItem = WordlistItem("solution_title", "Solution")
    REQUISITE_TITLE: WordlistItem = WordlistItem(
        "requisite_title", "Requirement"
    )
    TREATMENT_TITLE: WordlistItem = WordlistItem(
        "treatment_title", "Treatment"
    )
    RISK_TITLE: WordlistItem = WordlistItem("risk_title", "Risk")
    EVIDENCE_TITLE: WordlistItem = WordlistItem("evidence_title", "Evidences")
    COMPROMISED_SYSTEM_TITLE: WordlistItem = WordlistItem(
        "compromised_system_title", "Compromised System"
    )
    SEVERITY_TITLE: WordlistItem = WordlistItem("severity_title", "Severity")
    CARDINALITY_TITLE: WordlistItem = WordlistItem(
        "cardinality_title", "Vulnerabilities"
    )
    ATTACK_VECTOR_TITLE: WordlistItem = WordlistItem(
        "attack_vector_title", "Attack Vector"
    )
    RESUME_PAGE_TITLE: WordlistItem = WordlistItem(
        "resume_page_title", "General View"
    )
    RESUME_TABLE_TITLE: WordlistItem = WordlistItem(
        "resume_table_title", "Finding Table"
    )
    VULN_C: WordlistItem = WordlistItem("vuln_c", "Critical")
    VULN_H: WordlistItem = WordlistItem("vuln_h", "High")
    VULN_M: WordlistItem = WordlistItem("vuln_m", "Moderate")
    VULN_L: WordlistItem = WordlistItem("vuln_l", "Low")
    CRIT_C: WordlistItem = WordlistItem("crit_c", "(Critical)")
    CRIT_H: WordlistItem = WordlistItem("crit_h", "(High)")
    CRIT_M: WordlistItem = WordlistItem("crit_m", "(Moderate)")
    CRIT_L: WordlistItem = WordlistItem("crit_l", "(Low)")
    TREAT_STATUS_WOR: WordlistItem = WordlistItem("treat_status_wor", "New")
    TREAT_STATUS_ASU: WordlistItem = WordlistItem(
        "treat_status_asu", "Temporarily Accepted"
    )
    TREAT_PERMANENTLY_ASU: WordlistItem = WordlistItem(
        "treat_per_asu", "Permanently Accepted"
    )
    TREAT_STATUS_REM: WordlistItem = WordlistItem(
        "treat_status_rem", "In Progress"
    )
    FIN_STATUS_OPEN: WordlistItem = WordlistItem("fin_status_open", "Open")
    FIN_STATUS_CLOSED: WordlistItem = WordlistItem(
        "fin_status_closed", "Closed"
    )
