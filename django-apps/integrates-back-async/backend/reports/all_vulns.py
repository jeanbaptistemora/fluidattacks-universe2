# -*- coding: utf-8 -*-
""" Export all vulnerabilities """
import hashlib
import uuid
from typing import Dict, List, cast
from pyexcelerate import Workbook

from asgiref.sync import async_to_sync

from backend.dal import project as project_dal
from backend.domain import vulnerability as vuln_domain
from backend.reports.typing import (
    AllVulnsReportHeaderFindings,
    AllVulnsReportHeaderMasked,
    AllVulnsReportHeaderVulns
)
from backend.typing import Finding as FindingType

from __init__ import FI_TEST_PROJECTS

TEST_PROJECTS = FI_TEST_PROJECTS.split(',')


def _hash_cell(cell: str) -> str:
    return hashlib.sha256(cell.encode()).hexdigest()[-5:]


def _mask_finding(finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    for masked_cell in [label.value for label in AllVulnsReportHeaderMasked]:
        finding[masked_cell] = _hash_cell(str(finding[masked_cell]))
    return finding


def _get_reporter_analyst(
    opening_state: Dict[str, str],
    vuln: Dict[str, FindingType],
    finding: Dict[str, FindingType]
) -> str:
    analyst = opening_state.get('analyst', '')
    if not analyst:
        analyst = str(vuln.get('analyst', ''))
        if not analyst:
            finding.get('analyst', '')
    if analyst:
        analyst = _hash_cell(analyst)
    else:
        analyst = ''
    return analyst


def _format_specific(vuln: Dict[str, FindingType]) -> str:
    specific = ''
    if vuln.get('specific') != 'Masked':
        if vuln.get('vuln_type') == 'lines':
            file_ext = str(vuln.get('where')).split('/')[-1].split('.')[-1]
            if (file_ext.isalnum()
                    and not file_ext.isdigit()
                    and file_ext != 'Masked'):
                specific = file_ext.lower()
            else:
                specific = ''
        elif vuln.get('vuln_type') == 'ports':
            specific = str(vuln.get('specific'))

    return specific


def _format_vuln(
    vuln: Dict[str, FindingType],
    finding: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    if not vuln.get('treatment'):
        if finding.get('TREATMENT'):
            vuln['treatment'] = finding.get('TREATMENT')
        else:
            vuln['treatment'] = 'NEW'

    historic_state = cast(List[Dict[str, str]], vuln.get('historic_state'))
    last_state = historic_state[-1]
    opening_state = historic_state[0]

    if last_state.get('state') == 'closed':
        vuln['treatment'] = 'CLOSED'
        vuln['closing_date'] = last_state.get('date')

    vuln['specific'] = _format_specific(vuln)
    vuln['report_date'] = opening_state.get('date')
    vuln['analyst'] = _get_reporter_analyst(opening_state, vuln, finding)
    return vuln


def generate_all_vulns_xlsx(user_email: str, project_name: str = '') -> str:
    workbook = Workbook()
    header = AllVulnsReportHeaderFindings.labels() + \
        AllVulnsReportHeaderVulns.labels()
    sheet_values = [header]
    if project_name:
        projects = [{'project_name': project_name}]
    else:
        projects = cast(
            List[Dict[str, str]],
            async_to_sync(project_dal.get_all)(data_attr='project_name')
        )

    for project in projects:
        if project not in TEST_PROJECTS:
            findings = async_to_sync(project_dal.get_released_findings)(
                project.get('project_name', ''))
        else:
            findings = []
        for finding in findings:
            vulns = async_to_sync(vuln_domain.list_vulnerabilities_async)(
                [str(finding['finding_id'])]
            )
            finding_row = _mask_finding(finding)
            for vuln in vulns:
                vuln_row = cast(
                    Dict[str, FindingType],
                    _format_vuln(vuln, finding_row)
                )

                sheet_values.append([
                    [finding_row.get(label, '')
                        for label in AllVulnsReportHeaderFindings.labels()] +
                    [vuln_row.get(label, '')
                        for label in AllVulnsReportHeaderVulns.labels()]
                ])

    username = user_email.split('@')[0]
    filepath = f'/tmp/{username}-{str(uuid.uuid4())}-allvulns.xlsx'
    workbook.new_sheet('Data', data=sheet_values)
    workbook.save(filepath)

    return filepath
