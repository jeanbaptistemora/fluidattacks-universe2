# Standard library
from typing import cast, List, Union
import uuid
from pyexcelerate import Workbook

# Local libraries
from backend.domain import (
    finding as finding_domain,
    vulnerability as vuln_domain
)
from backend.reports.typing import CompleteReportHeader
from backend.typing import Historic as HistoricType
from backend.utils import reports as reports_utils


# pylint: disable=too-many-locals
async def generate(
    user_email: str,
    projects: List[str]
) -> str:
    header = CompleteReportHeader.labels()
    workbook = Workbook()
    sheet_values: List[Union[List[str], List[List[str]]]] = [header]

    for project in projects:
        attrs = {'finding_id', 'finding'}
        findings = await finding_domain.get_findings_by_group(
            project,
            attrs
        )
        for finding in findings:
            vulns = await vuln_domain.list_vulnerabilities_async(
                [str(finding['finding_id'])]
            )
            for vuln in vulns:
                historic_treatment = cast(
                    HistoricType,
                    vuln.get('historic_treatment', [{}])
                )
                sheet_values.append([
                    cast(str, vuln['where']),
                    cast(str, vuln['specific']),
                    (f'{str(finding["finding"]).encode("utf-8")!s} '
                     f'(#{str(finding["finding_id"])})'),
                    historic_treatment[-1].get('treatment', 'NEW'),
                    historic_treatment[-1].get(
                        'treatment_manager', 'Unassigned'
                    ),
                ])

    username = user_email.split('@')[0]
    report_filepath = f'/tmp/{username}-{uuid.uuid4()}-complete.xlsx'
    workbook.new_sheet('Data', data=sheet_values)
    workbook.save(report_filepath)

    uploaded_file_name = await reports_utils.upload_report(report_filepath)
    uploaded_file_url = await reports_utils.sign_url(
        uploaded_file_name,
        minutes=1.0 / 6
    )

    return uploaded_file_url
