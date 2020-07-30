from enum import Enum
from typing import NamedTuple


class ColumnConfig(NamedTuple):
    label: str
    width: int = -1


class GenericHeader(Enum):

    @classmethod
    def labels(cls):
        return [member.value.label for member in cls]

    @classmethod
    def widths(cls):
        return [member.value.width for member in cls]


class AllUsersReportHeader(GenericHeader):
    NAME: ColumnConfig = ColumnConfig(label='full_name')
    EMAIL: ColumnConfig = ColumnConfig(label='user_email')


class CompleteReportHeader(GenericHeader):
    PROJECT: ColumnConfig = ColumnConfig(label='Project')
    FINDING: ColumnConfig = ColumnConfig(label='Finding')
    WHERE: ColumnConfig = ColumnConfig(label='Vulnerability (where)')
    SPECIFIC: ColumnConfig = ColumnConfig(
        label='Vulnerability (specific)')
    TREATMENT: ColumnConfig = ColumnConfig(label='Treatment')
    TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='Treatment Manager')


class AllVulnsReportHeaderFindings(GenericHeader):
    PROJECT: ColumnConfig = ColumnConfig(label='project_name')
    FINDING_ID: ColumnConfig = ColumnConfig(label='finding_id')
    FINDING: ColumnConfig = ColumnConfig(label='finding')
    FINDING_TYPE: ColumnConfig = ColumnConfig(label='finding_type')
    ATTACK_VECTOR: ColumnConfig = ColumnConfig(label='attack_vector')
    ATTACK_COMPLEXITY: ColumnConfig = ColumnConfig(
        label='attack_complexity')
    USER_INTERACTION: ColumnConfig = ColumnConfig(
        label='user_interaction')
    SEVERITY_SCOPE: ColumnConfig = ColumnConfig(
        label='severity_scope')
    CONFIDENTIALITY_IMPACT: ColumnConfig = ColumnConfig(
        label='confidentiality_impact')
    INTEGRITY_IMPACT: ColumnConfig = ColumnConfig(
        label='integrity_impact')
    AVAILABILITY_IMPACT: ColumnConfig = ColumnConfig(
        label='availability_impact')
    EXPLOITABILITY: ColumnConfig = ColumnConfig(
        label='exploitability')
    REMEDIATION_LEVEL: ColumnConfig = ColumnConfig(
        label='remediation_level')
    REPORT_CONFIDENCE: ColumnConfig = ColumnConfig(
        label='report_confidence')
    CVSS_BASESCORE: ColumnConfig = ColumnConfig(
        label='cvss_basescore')
    CVSS_TEMPORAL: ColumnConfig = ColumnConfig(label='cvss_temporal')
    ACTOR: ColumnConfig = ColumnConfig(label='actor')
    CWE: ColumnConfig = ColumnConfig(label='cwe')
    SCENARIO: ColumnConfig = ColumnConfig(label='scenario')


class AllVulnsReportHeaderVulns(GenericHeader):
    VULN_TYPE: ColumnConfig = ColumnConfig(label='vuln_type', width=30)
    REPORT_DATE: ColumnConfig = ColumnConfig(label='report_date', width=30)
    ANALYST: ColumnConfig = ColumnConfig(label='analyst', width=30)
    TREATMENT: ColumnConfig = ColumnConfig(label='treatment', width=30)
    SPECIFIC: ColumnConfig = ColumnConfig(label='specific', width=30)
    CLOSE_DATE: ColumnConfig = ColumnConfig(label='closing_date', width=30)


class AllVulnsReportHeaderMasked(Enum):
    FINDING_ID: str = 'finding_id'
    PROJECT_NAME: str = 'project_name'


class GroupVulnsReportHeader(GenericHeader):
    NUMBER: ColumnConfig = ColumnConfig(label='#', width=4)
    FINDING: ColumnConfig = ColumnConfig(label='Related Finding', width=55)
    FINDING_ID: ColumnConfig = ColumnConfig(label='Finding Id', width=25)
    VULNERABILITY_ID: ColumnConfig = ColumnConfig(
        label='Vulnerability Id', width=50)
    WHERE: ColumnConfig = ColumnConfig(label='Where', width=45)
    SPECIFIC: ColumnConfig = ColumnConfig(label='Specific', width=38)
    DESCRIPTION: ColumnConfig = ColumnConfig(label='Description', width=95)
    STATUS: ColumnConfig = ColumnConfig(label='Status', width=13)
    SEVERITY: ColumnConfig = ColumnConfig('Severity', width=13)
    REQUIREMENTS: ColumnConfig = ColumnConfig(label='Requirements', width=100)
    IMPACT: ColumnConfig = ColumnConfig(label='Impact', width=65)
    AFFECTED_SYSTEMS: ColumnConfig = ColumnConfig(
        label='Affected System', width=45)
    THREAT: ColumnConfig = ColumnConfig(label='Threat', width=55)
    RECOMMENDATION: ColumnConfig = ColumnConfig(
        label='Recommendation', width=100)
    EXTERNAL_BTS: ColumnConfig = ColumnConfig(
        label='External BTS', width=80)
    COMPROMISED_ATTRS: ColumnConfig = ColumnConfig(
        label='Compromised Attributes', width=35)
    N_COMPROMISED_RECORDS: ColumnConfig = ColumnConfig(
        label='# Compromised records', width=30)
    TAGS: ColumnConfig = ColumnConfig(label='Tags', width=60)
    BUSINESS_CRITICALLY: ColumnConfig = ColumnConfig(
        label='Business Critically', width=25)
    REPORT_MOMENT: ColumnConfig = ColumnConfig(label='Report Moment', width=25)
    CLOSE_MOMENT: ColumnConfig = ColumnConfig(label='Close Moment', width=25)
    AGE: ColumnConfig = ColumnConfig(label='Age in days', width=20)
    FIRST_TREATMENT: ColumnConfig = ColumnConfig(
        label='First Treatment', width=20)
    FIRST_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label='First Treatment Moment', width=25)
    FIRST_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label='First Treatment Justification', width=95)
    FIRST_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label='First Treatment expiration Moment', width=40)
    FIRST_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='First Treatment manager', width=35)
    CURRENT_TREATMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment', width=20)
    CURRENT_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment Moment', width=25)
    CURRENT_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label='Current Treatment Justification', width=95)
    CURRENT_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label='Current Treatment expiration Moment', width=40)
    CURRENT_TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='Current Treatment manager', width=35)
    PENDING_REATTACK: ColumnConfig = ColumnConfig(
        label='Pending Reattack', width=25)
    N_REQUESTED_REATTACKS: ColumnConfig = ColumnConfig(
        label='# Requested Reattacks', width=25)
    REMEDIATION_EFFECTIVENESS: ColumnConfig = ColumnConfig(
        label='Remediation Effectiveness', width=25)
    LAST_REQUESTED_REATTACK: ColumnConfig = ColumnConfig(
        label='Last requested reattack', width=25)
    LAST_REATTACK_REQUESTER: ColumnConfig = ColumnConfig(
        label='Last reattack Requester', width=35)
    CVSS_VECTOR: ColumnConfig = ColumnConfig(
        label='CVSSv3.1 string vector', width=55)
    ATTACK_VECTOR: ColumnConfig = ColumnConfig(
        label='Attack Vector', width=18)
    ATTACK_COMPLEXITY: ColumnConfig = ColumnConfig(
        label='Attack Complexity', width=20)
    PRIVILEGES_REQUIRED: ColumnConfig = ColumnConfig(
        label='Privileges Required', width=25)
    USER_INTERACTION: ColumnConfig = ColumnConfig(
        label='User Interaction', width=20)
    SEVERITY_SCOPE: ColumnConfig = ColumnConfig(
        label='Severity Scope', width=20)
    CONFIDENTIALITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Confidentiality Impact', width=23)
    INTEGRITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Integrity Impact', width=20)
    AVAILABILITY_IMPACT: ColumnConfig = ColumnConfig(
        label='Availability Imapact', width=20)
    EXPLOITABILITY: ColumnConfig = ColumnConfig(
        label='Exploitability', width=18)
    REMEDIATION_LEVEL: ColumnConfig = ColumnConfig(
        label='Remediation Level', width=25)
    REPORT_CONFIDENCE: ColumnConfig = ColumnConfig(
        label='Report Confidence', width=25)
