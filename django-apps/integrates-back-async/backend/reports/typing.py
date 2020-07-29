from enum import Enum
from typing import NamedTuple


class ColumnConfig(NamedTuple):
    label: str
    width: int = -1


class AllVulnsHeader(Enum):

    @classmethod
    def labels(cls):
        return [member.value.label for member in cls]

    @classmethod
    def widths(cls):
        return [member.value.width for member in cls]


class AllUsersReportHeader(AllVulnsHeader):
    NAME: ColumnConfig = ColumnConfig(label='full_name')
    EMAIL: ColumnConfig = ColumnConfig(label='user_email')


class CompleteReportHeader(AllVulnsHeader):
    PROJECT: ColumnConfig = ColumnConfig(label='Project')
    FINDING: ColumnConfig = ColumnConfig(label='Finding')
    WHERE: ColumnConfig = ColumnConfig(label='Vulnerability (where)')
    SPECIFIC: ColumnConfig = ColumnConfig(
        label='Vulnerability (specific)')
    TREATMENT: ColumnConfig = ColumnConfig(label='Treatment')
    TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='Treatment Manager')


class AllVulnsReportHeaderFindings(AllVulnsHeader):
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


class AllVulnsReportHeaderVulns(AllVulnsHeader):
    VULN_TYPE: ColumnConfig = ColumnConfig(label='vuln_type', width=30)
    REPORT_DATE: ColumnConfig = ColumnConfig(label='report_date', width=30)
    ANALYST: ColumnConfig = ColumnConfig(label='analyst', width=30)
    TREATMENT: ColumnConfig = ColumnConfig(label='treatment', width=30)
    SPECIFIC: ColumnConfig = ColumnConfig(label='specific', width=30)
    CLOSE_DATE: ColumnConfig = ColumnConfig(label='closing_date', width=30)


class AllVulnsReportHeaderMasked(Enum):
    FINDING_ID: str = 'finding_id'
    PROJECT_NAME: str = 'project_name'
