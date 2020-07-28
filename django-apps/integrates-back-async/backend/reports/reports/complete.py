# Standard library
from enum import Enum
from typing import cast, List, NamedTuple
import uuid
from pyexcelerate import Workbook

from asgiref.sync import async_to_sync

# Local libraries
from backend.domain import (
    project as project_domain,
    vulnerability as vuln_domain
)
from backend.typing import Historic as HistoricType
from backend.utils import reports as reports_utils


class ColumnConfig(NamedTuple):
    label: str
    width: int


class CompleteReportHeader(Enum):
    PROJECT: ColumnConfig = ColumnConfig(label='Project', width=30)
    FINDING: ColumnConfig = ColumnConfig(label='Finding', width=30)
    WHERE: ColumnConfig = ColumnConfig(label='Vulnerability (where)', width=30)
    SPECIFIC: ColumnConfig = ColumnConfig(
        label='Vulnerability (specific)', width=30)
    TREATMENT: ColumnConfig = ColumnConfig(label='Treatment', width=30)
    TREATMENT_MANAGER: ColumnConfig = ColumnConfig(
        label='Treatment Manager', width=30)


# pylint: disable=too-many-locals
def generate(
    user_email: str,
    projects: List[str]
) -> str:
    header = [label.value.label for label in CompleteReportHeader]
    workbook = Workbook()
    sheet_values = [header]

    for project in projects:
        findings = async_to_sync(project_domain.get_released_findings)(
            project, 'finding_id, finding, historic_treatment'
        )
        for finding in findings:
            vulns = async_to_sync(vuln_domain.list_vulnerabilities_async)(
                [str(finding['finding_id'])]
            )
            for vuln in vulns:
                historic_treatment = finding.get('historic_treatment', [{}])
                sheet_values.append([
                    vuln['where'],
                    vuln['specific'],
                    (f'{str(finding["finding"]).encode("utf-8")!s} '
                     f'(#{str(finding["finding_id"])})'),
                    cast(
                        HistoricType,
                        historic_treatment
                    )[-1].get('treatment', ''),
                    vuln.get('treatment_manager', 'Unassigned')
                ])

    username = user_email.split('@')[0]
    report_filepath = f'/tmp/{username}-{uuid.uuid4()}-complete.xlsx'
    workbook.new_sheet('Data', data=sheet_values)
    workbook.save(cast(str, report_filepath))

    uploaded_file_name = reports_utils.upload_report(report_filepath)
    uploaded_file_url = reports_utils.sign_url(
        uploaded_file_name,
        minutes=1.0 / 6
    )

    return uploaded_file_url
