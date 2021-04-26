from enum import Enum
from typing import (
    List,
    NamedTuple,
    Union,
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
    AFFECTED_SYSTEMS: ColumnConfig = ColumnConfig(
        label='Affected System',
        width=45
    )
    AGE: ColumnConfig = ColumnConfig(label='Age in days', width=20)
    ATTACK_COMPLEXITY: ColumnConfig = ColumnConfig(
        label='Attack Complexity',
        width=20
    )
    ATTACK_VECTOR: ColumnConfig = ColumnConfig(
        label='Attack Vector',
        width=18
    )
    AVAILABILITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Availability Imapact',
        width=20
    )
    BUSINESS_CRITICALLY: ColumnConfig = ColumnConfig(
        label='Business Critically',
        width=25
    )
    CLOSE_MOMENT: ColumnConfig = ColumnConfig(label='Close Moment', width=25)
    COMPROMISED_ATTRS: ColumnConfig = ColumnConfig(
        label='Compromised Attributes',
        width=35
    )
    CONFIDENTIALITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Confidentiality Impact',
        width=23
    )
    CURRENT_TREATMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment',
        width=20
    )
    CURRENT_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment expiration Moment',
        width=40
    )
    CURRENT_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label='Current Treatment Justification',
        width=95
    )
    CURRENT_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='Current Treatment manager',
        width=35
    )
    CURRENT_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment Moment',
        width=25
    )
    CVSS_VECTOR: ColumnConfig = ColumnConfig(
        label='CVSSv3.1 string vector',
        width=55
    )
    DESCRIPTION: ColumnConfig = ColumnConfig(label='Description', width=95)
    EXPLOITABILITY: ColumnConfig = ColumnConfig(
        label='Exploitability',
        width=18
    )
    EXTERNAL_BTS: ColumnConfig = ColumnConfig(
        label='External BTS',
        width=80
    )
    FINDING: ColumnConfig = ColumnConfig(label='Related Finding', width=55)
    FINDING_ID: ColumnConfig = ColumnConfig(label='Finding Id', width=25)
    FIRST_TREATMENT: ColumnConfig = ColumnConfig(
        label='First Treatment',
        width=20
    )
    FIRST_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label='First Treatment expiration Moment',
        width=40
    )
    FIRST_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label='First Treatment Justification',
        width=95
    )
    FIRST_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='First Treatment manager',
        width=35
    )
    FIRST_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label='First Treatment Moment',
        width=25
    )
    IMPACT: ColumnConfig = ColumnConfig(label='Impact', width=65)
    INTEGRITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Integrity Impact',
        width=20
    )
    LAST_REATTACK_REQUESTER: ColumnConfig = ColumnConfig(
        label='Last reattack Requester',
        width=35
    )
    LAST_REQUESTED_REATTACK: ColumnConfig = ColumnConfig(
        label='Last requested reattack',
        width=25
    )
    N_COMPROMISED_RECORDS: ColumnConfig = ColumnConfig(
        label='# Compromised records',
        width=30
    )
    N_REQUESTED_REATTACKS: ColumnConfig = ColumnConfig(
        label='# Requested Reattacks',
        width=25
    )
    NUMBER: ColumnConfig = ColumnConfig(label='#', width=4)
    PENDING_REATTACK: ColumnConfig = ColumnConfig(
        label='Pending Reattack',
        width=25
    )
    PRIVILEGES_REQUIRED: ColumnConfig = ColumnConfig(
        label='Privileges Required',
        width=25
    )
    RECOMMENDATION: ColumnConfig = ColumnConfig(
        label='Recommendation',
        width=100
    )
    REMEDIATION_LEVEL: ColumnConfig = ColumnConfig(
        label='Remediation Level',
        width=25
    )
    REMEDIATION_EFFECTIVENESS: ColumnConfig = ColumnConfig(
        label='Remediation Effectiveness',
        width=25
    )
    REPORT_CONFIDENCE: ColumnConfig = ColumnConfig(
        label='Report Confidence',
        width=25
    )
    REPORT_MOMENT: ColumnConfig = ColumnConfig(label='Report Moment', width=25)
    REQUIREMENTS: ColumnConfig = ColumnConfig(label='Requirements', width=100)
    SEVERITY: ColumnConfig = ColumnConfig('Severity', width=13)
    SEVERITY_SCOPE: ColumnConfig = ColumnConfig(
        label='Severity Scope',
        width=20
    )
    SPECIFIC: ColumnConfig = ColumnConfig(label='Specific', width=38)
    STATUS: ColumnConfig = ColumnConfig(label='Status', width=13)
    TAGS: ColumnConfig = ColumnConfig(label='Tags', width=60)
    THREAT: ColumnConfig = ColumnConfig(label='Threat', width=55)
    USER_INTERACTION: ColumnConfig = ColumnConfig(
        label='User Interaction',
        width=20
    )
    VULNERABILITY_ID: ColumnConfig = ColumnConfig(
        label='Vulnerability Id',
        width=50
    )
    WHERE: ColumnConfig = ColumnConfig(label='Where', width=45)


# PDF report types definitions
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
    ATTACK_VECTOR_TITLE: WordlistItem = WordlistItem(
        'attack_vector_title',
        'Attack Vector'
    )
    CARDINALITY_TITLE: WordlistItem = WordlistItem(
        'cardinality_title',
        'Vulnerabilities'
    )
    COMPROMISED_SYSTEM_TITLE: WordlistItem = WordlistItem(
        'compromised_system_title',
        'Compromised System'
    )
    CONTENT_LIST: WordlistItem = WordlistItem(
        'content_list',
        [
            '1. Goals',
            '2. Finding Table',
            '3. General View',
            '4. Findings Summary'
        ]
    )
    CONTENT_TITLE: WordlistItem = WordlistItem('content_title', 'Content')
    CRIT_C: WordlistItem = WordlistItem('crit_c', '(Critical)')
    CRIT_H: WordlistItem = WordlistItem('crit_h', '(High)')
    CRIT_L: WordlistItem = WordlistItem('crit_l', '(Low)')
    CRIT_M: WordlistItem = WordlistItem('crit_m', '(Moderate)')
    DESCRIPTION_TITLE: WordlistItem = WordlistItem(
        'description_title',
        'Vulnerability'
    )
    EVIDENCE_TITLE: WordlistItem = WordlistItem('evidence_title', 'Evidences')
    EXECUTIVE: WordlistItem = WordlistItem('executive', 'Executive Report')
    FIELD: WordlistItem = WordlistItem('field', 'Field')
    FIN_STATUS_CLOSED: WordlistItem = WordlistItem(
        'fin_status_closed',
        'Closed'
    )
    FIN_STATUS_OPEN: WordlistItem = WordlistItem('fin_status_open', 'Open')
    FINDING_SECTION_TITLE: WordlistItem = WordlistItem(
        'finding_section_title',
        'Resume'
    )
    FINDING_TITLE: WordlistItem = WordlistItem('finding_title', 'Finding')
    GOALS_TITLE: WordlistItem = WordlistItem('goals_title', 'Goals')
    INPUTS: WordlistItem = WordlistItem('inputs', 'Inputs')
    LINE: WordlistItem = WordlistItem('line', 'Line')
    LINES: WordlistItem = WordlistItem('lines', 'Lines')
    METHODOLOGY_TITLE: WordlistItem = WordlistItem(
        'metodology_title',
        'Methodology'
    )
    PATH: WordlistItem = WordlistItem('path', 'Path')
    PORT: WordlistItem = WordlistItem('port', 'Port')
    PORTS: WordlistItem = WordlistItem('ports', 'Ports')
    RECORDS_TITLE: WordlistItem = WordlistItem('records_title', 'Records')
    REQUISITE_TITLE: WordlistItem = WordlistItem(
        'requisite_title',
        'Requirement'
    )
    RESUME_PAGE_TITLE: WordlistItem = WordlistItem(
        'resume_page_title',
        'General View'
    )
    RESUME_PERC_TITLE: WordlistItem = WordlistItem(
        'resume_perc_title',
        'Percent'
    )
    RESUME_REGI_TITLE: WordlistItem = WordlistItem(
        'resume_regi_title',
        'Total Records'
    )
    RESUME_TABLE_TITLE: WordlistItem = WordlistItem(
        'resume_table_title',
        'Finding Table'
    )
    RESUME_TOP_TITLE: WordlistItem = WordlistItem(
        'resume_top_title',
        'Finding Top'
    )
    RESUME_TTAB_TITLE: WordlistItem = WordlistItem('resume_ttab_title', 'Name')
    RESUME_VNUM_TITLE: WordlistItem = WordlistItem('resume_vnum_title', '#')
    RESUME_VNAME_TITLE: WordlistItem = WordlistItem(
        'resume_vname_title',
        'Name'
    )
    RESUME_VULN_TITLE: WordlistItem = WordlistItem(
        'resume_vuln_title',
        'Vulnerabilities'
    )
    RISK_TITLE: WordlistItem = WordlistItem('risk_title', 'Risk')
    SEVERITY_TITLE: WordlistItem = WordlistItem('severity_title', 'Severity')
    SOLUCION_TITLE: WordlistItem = WordlistItem('solution_title', 'Solution')
    STATE_TITLE: WordlistItem = WordlistItem('state_title', 'Status')
    TECH: WordlistItem = WordlistItem('tech', 'Technical Report')
    THREAT_TITLE: WordlistItem = WordlistItem('threat_title', 'Threat')
    TREAT_ETERNALLY_ASU: WordlistItem = WordlistItem(
        'treat_ete_asu',
        'Eternally Accepted'
    )
    TREAT_STATUS_ASU: WordlistItem = WordlistItem(
        'treat_status_asu',
        'Temporarily Accepted'
    )
    TREAT_STATUS_REM: WordlistItem = WordlistItem(
        'treat_status_rem',
        'In Progress'
    )
    TREAT_STATUS_WOR: WordlistItem = WordlistItem('treat_status_wor', 'New')
    TREATMENT_TITLE: WordlistItem = WordlistItem(
        'treatment_title',
        'Treatment'
    )
    VULN_C: WordlistItem = WordlistItem('vuln_c', 'Critical')
    VULN_H: WordlistItem = WordlistItem('vuln_h', 'High')
    VULN_L: WordlistItem = WordlistItem('vuln_l', 'Low')
    VULN_M: WordlistItem = WordlistItem('vuln_m', 'Moderate')
    WHERE_TITLE: WordlistItem = WordlistItem('where_title', 'Where')
