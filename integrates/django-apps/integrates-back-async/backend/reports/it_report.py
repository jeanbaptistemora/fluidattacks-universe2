# -*- coding: utf-8 -*-
""" Class for generate an xlsx file with vulnerabilities information. """
from typing import cast, Dict, List, Union

from datetime import datetime
from dateutil.parser import parse
from django.conf import settings
import pytz
from pyexcelerate import (
    Alignment,
    Color,
    Style,
    Workbook,
    Worksheet as WorksheetType
)
from backend.domain import vulnerability as vuln_domain
from backend.reports.typing import GroupVulnsReportHeader
from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType,
    Vulnerability as VulnType
)


EMPTY = '-'
HEADER_HEIGHT = 20
ROW_HEIGHT = 57
RED = Color(255, 52, 53, 1)  # FF3435
WHITE = Color(255, 255, 255, 1)


def get_formatted_last_date(
    historic_state: HistoricType
) -> Union[str, datetime]:
    curr_trtmnt_date: Union[str, datetime] = EMPTY

    if historic_state and 'date' in cast(HistoricType, historic_state)[-1]:
        last_date = str(cast(HistoricType, historic_state)[-1]['date'])
        curr_trtmnt_date = parse(last_date)
    return curr_trtmnt_date


class ITReport():
    """Class to generate IT reports."""

    workbook: Workbook
    current_sheet: WorksheetType = None
    data: List[Dict[str, FindingType]] = []
    lang = None
    row = 1
    result_filename = ''
    project_name = ''
    vulnerability = {
        col_name: index + 1
        for index, col_name in enumerate(GroupVulnsReportHeader.labels())
    }
    cvss_measures = {
        'AV': 'attackVector',
        'AC': 'attackComplexity',
        'PR': 'privilegesRequired',
        'UI': 'userInteraction',
        'S': 'severityScope',
        'C': 'confidentialityImpact',
        'I': 'integrityImpact',
        'A': 'availabilityImpact',
        'E': 'exploitability',
        'RL': 'remediationLevel',
        'RC': 'reportConfidence',
    }
    row_values: List[Union[str, int, datetime]] = [
        EMPTY
        for _ in range(len(vulnerability) + 1)
    ]

    def __init__(
            self,
            data: List[Dict[str, FindingType]],
            lang: str = 'es') -> None:
        """Initialize variables."""
        self.data = data
        self.project_name = str(data[0].get('projectName'))
        self.lang = lang

        self.workbook = Workbook()
        self.current_sheet = self.workbook.new_sheet('Data')

        self.parse_template()

    async def create(self) -> None:
        await self.generate(self.data)
        self.style_sheet()
        self.save()

    def save(self) -> None:
        tzn = pytz.timezone(settings.TIME_ZONE)
        today_date = datetime.now(tz=tzn).strftime('%Y-%m-%dT%H-%M-%S')
        self.result_filename = (
            f'{self.project_name}-vulnerabilities-{today_date}.xlsx'
        )
        self.workbook.save(self.result_filename)

    def style_sheet(self) -> None:
        header = self.current_sheet.range(*self.get_row_range(1))
        header.style.fill.background = RED
        header.style.font.color = WHITE
        header.style.alignment.horizontal = 'center'
        header.style.alignment.vertical = 'center'
        header.style.alignment.wrap_text = True

        for column, col_width in enumerate(GroupVulnsReportHeader.widths()):
            self.current_sheet.set_col_style(
                column + 1,
                Style(size=col_width, alignment=Alignment(wrap_text=True)),
            )

    def parse_template(self) -> None:
        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            list(self.vulnerability.keys())
        ]
        self.row += 1

    async def generate(self, data: List[Dict[str, FindingType]]) -> None:
        self.project_name = str(data[0].get('projectName'))

        for finding in data:
            finding_vulns = await vuln_domain.list_vulnerabilities_async(
                [str(finding.get('findingId'))]
            )
            for vuln in finding_vulns:
                await self.set_vuln_row(
                    cast(VulnType, vuln),
                    cast(Dict[str, FindingType], finding)
                )
                self.row += 1

    def set_row_height(self) -> None:
        self.current_sheet.set_row_style(
            self.row, Style(
                size=ROW_HEIGHT,
                alignment=Alignment(wrap_text=True)
            )
        )

    @classmethod
    def get_row_range(cls, row: int) -> List[str]:
        return [f'A{row}', f'AW{row}']

    @staticmethod
    def get_measure(
        metric: str,
        metric_value: str
    ) -> str:
        """Extract number of CSSV metrics."""
        metrics = {
            'attackVector': {
                '0.85': 'Network',
                '0.62': 'Adjacent',
                '0.55': 'Local',
                '0.20': 'Physical',
            },
            'attackComplexity': {
                '0.77': 'Low',
                '0.44': 'High',
            },
            'privilegesRequired': {
                '0.85': 'None',
                '0.62': 'Low',
                '0.68': 'Low',
                '0.27': 'High',
                '0.50': 'High',
            },
            'userInteraction': {
                '0.85': 'None',
                '0.62': 'Required',
            },
            'severityScope': {
                '0.0': 'Unchanged',
                '1.0': 'Changed',
            },
            'confidentialityImpact': {
                '0.56': 'High',
                '0.22': 'Low',
                '0.0': 'None',
            },
            'integrityImpact': {
                '0.56': 'High',
                '0.22': 'Low',
                '0.0': 'None',
            },
            'availabilityImpact': {
                '0.56': 'High',
                '0.22': 'Low',
                '0.0': 'None',
            },
            'exploitability': {
                '0.91': 'Unproven',
                '0.94': 'Proof of concept',
                '0.97': 'Functional',
                '1.0': 'High',
            },
            'remediationLevel': {
                '0.95': 'Official Fix',
                '0.96': 'Temporary Fix',
                '0.97': 'Workaround',
                '1.0': 'Unavailable',
            },
            'reportConfidence': {
                '0.92': 'Unknown',
                '0.96': 'Reasonable',
                '1.0': 'Confirmed',
            }
        }
        metric_descriptions = metrics.get(metric, dict())
        description = metric_descriptions.get(str(metric_value), EMPTY)

        return description

    def set_cvss_metrics_cell(self, row: Dict[str, FindingType]) -> None:
        metric_vector = []
        vuln = self.vulnerability
        cvss_key = 'CVSSv3.1 string vector'
        for ind, (indicator, measure) in enumerate(self.cvss_measures.items()):
            value = self.get_measure(
                measure,
                cast(Dict[str, str], row['severity'])[measure]
            )
            if value:
                metric_vector.append(f'{indicator}:{value[0]}')
                self.row_values[vuln[cvss_key] + ind + 1] = value

        cvss_metric_vector = '/'.join(metric_vector)
        cvss_calculator_url = (
            f'https://www.first.org/cvss/calculator/3.1#CVSS:3.1'
            f'/{cvss_metric_vector}'
        )
        cell_content = (
            f'=HYPERLINK("{cvss_calculator_url}", "{cvss_metric_vector}")'
        )
        self.row_values[vuln[cvss_key]] = cell_content

    async def set_vuln_row(
        self,
        row: VulnType,
        finding: Dict[str, FindingType]
    ) -> None:
        vuln = self.vulnerability
        specific = str(row.get('specific', ''))
        if row.get('vuln_type') == 'lines':
            specific = str(int(specific))
        tags = EMPTY
        if 'tag' in row:
            tags = str(', '.join(cast(List[str], row.get('tag'))))

        self.row_values[vuln['#']] = self.row - 1
        self.row_values[vuln['Related Finding']] = str(finding.get('finding'))
        self.row_values[vuln['Finding Id']] = str(
            finding.get('findingId', EMPTY))
        self.row_values[vuln['Vulnerability Id']] = str(row.get('UUID', EMPTY))
        self.row_values[vuln['Where']] = str(row.get('where'))
        self.row_values[vuln['Specific']] = specific
        self.row_values[vuln['Tags']] = tags

        self.set_finding_data(finding, row)
        self.set_vuln_temporal_data(row)
        self.set_treatment_data(finding, row)
        self.set_reattack_data(finding, row)
        self.set_cvss_metrics_cell(finding)

        self.current_sheet.range(*self.get_row_range(self.row)).value = \
            [self.row_values[1:]]
        self.set_row_height()

    def set_finding_data(
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ) -> None:
        compromised_attributes = str(finding.get('compromisedAttrs')) or EMPTY
        n_compromised_attributes = None
        if compromised_attributes != EMPTY:
            n_compromised_attributes = str(
                len(compromised_attributes.split('\n'))
            )
        external_bts = finding.get('externalBts', EMPTY)
        severity = cast(int, finding.get('severityCvss', 0))

        finding_data = {
            'Description': str(finding.get('vulnerability', EMPTY)),
            'Status': cast(
                HistoricType, vuln.get('historic_state'))[-1]['state'],
            'Severity': severity or EMPTY,
            'Requirements': str(finding.get('requirements', EMPTY)),
            'Impact': str(finding.get('attackVectorDesc', EMPTY)),
            'Affected System': str(finding.get('affectedSystems', EMPTY)),
            'Threat': str(finding.get('threat', EMPTY)),
            'Recommendation': str(finding.get('effectSolution', EMPTY)),
            'External BTS': f'=HYPERLINK("{external_bts}", "{external_bts}")',
            'Compromised Attributes': compromised_attributes,
            '# Compromised records': n_compromised_attributes or '0',
        }
        for key, value in finding_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_vuln_temporal_data(self, vuln: VulnType) -> None:
        vuln_historic_state = cast(HistoricType, vuln.get('historic_state'))
        vuln_date = datetime.strptime(
            vuln_historic_state[0]['date'], '%Y-%m-%d %H:%M:%S'
        )
        vuln_closed = vuln_historic_state[-1]['state'] == 'closed'
        tzn = pytz.timezone(settings.TIME_ZONE)
        limit_date = datetime.now(tz=tzn)
        vuln_close_date: Union[str, datetime] = EMPTY
        if vuln_closed:
            limit_date = datetime.strptime(
                vuln_historic_state[-1]['date'], '%Y-%m-%d %H:%M:%S'
            )
            vuln_close_date = datetime.strptime(
                vuln_historic_state[-1]['date'], '%Y-%m-%d %H:%M:%S'
            )
        vuln_age_days = int((limit_date - vuln_date).days)

        vuln_temporal_data: Dict[str, Union[str, int, datetime]] = {
            'Report Moment': vuln_date,
            'Age in days': vuln_age_days,
            'Close Moment': vuln_close_date
        }
        for key, value in vuln_temporal_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_treatment_data(  # pylint: disable=too-many-locals
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ) -> None:
        def format_treatment(treatment: str) -> str:
            treatment = treatment.capitalize().replace('_', ' ')
            if treatment == 'Accepted undefined':
                treatment = 'Eternally accepted'
            elif treatment == 'Accepted':
                treatment = 'Temporarily accepted'
            return treatment

        historic_state = cast(
            HistoricType,
            finding.get('historicState')
        )
        finding_historic_treatment = cast(
            HistoricType,
            finding.get('historicTreatment')
        )
        curr_trtmnt_date: Union[str, datetime] = get_formatted_last_date(
            historic_state
        )
        current_treatment_exp_date: Union[str, datetime] = EMPTY
        first_treatment_exp_date: Union[str, datetime] = EMPTY

        if 'acceptance_date' in vuln:
            current_treatment_exp_date = datetime.strptime(
                str(vuln.get('acceptance_date')),
                '%Y-%m-%d %H:%M:%S'
            )
        first_treatment_state = finding_historic_treatment[0]
        if len(str(finding.get('releaseDate')).split(' ')) == 2:
            first_treatment_date_format = '%Y-%m-%d %H:%M:%S'
        else:
            first_treatment_date_format = '%Y-%m-%d'
        if len(finding_historic_treatment) > 1:
            first_treatment_exp_date = finding_historic_treatment[1].get(
                'date', EMPTY
            )
            if first_treatment_exp_date != EMPTY:
                first_treatment_exp_date = datetime.strptime(
                    str(first_treatment_exp_date),
                    '%Y-%m-%d %H:%M:%S'
                )

        current_treatment_data: Dict[str, Union[str, int, datetime]] = {
            'Current Treatment': format_treatment(
                str(vuln.get('treatment', 'NEW'))
            ),
            'Current Treatment Moment': curr_trtmnt_date,
            'Current Treatment Justification': str(
                vuln.get('treatment_justification', EMPTY)),
            'Current Treatment expiration Moment': current_treatment_exp_date,
            'Current Treatment manager': str(
                vuln.get('treatment_manager', EMPTY)
            ),
        }
        first_treatment_data: Dict[str, Union[str, int, datetime]] = {
            'First Treatment': str(
                format_treatment(first_treatment_state.get('treatment', 'NEW'))
            ),
            'First Treatment Moment': datetime.strptime(
                str(finding.get('releaseDate')),
                first_treatment_date_format
            ),
            'First Treatment Justification': str(
                first_treatment_state.get('justification', EMPTY)
            ),
            'First Treatment expiration Moment': first_treatment_exp_date,
            'First Treatment manager': str(
                first_treatment_state.get('user', EMPTY)
            ),
        }

        for key, value in current_treatment_data.items():
            self.row_values[self.vulnerability[key]] = value
            first_treatment_key = key.replace('Current', 'First')
            kword = self.vulnerability[first_treatment_key]
            self.row_values[kword] = first_treatment_data[first_treatment_key]

    def set_reattack_data(
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ) -> None:
        historic_verification = cast(
            HistoricType,
            finding.get('historicVerification')
        )
        vuln_closed = cast(
            HistoricType, vuln.get('historic_state'))[-1]['state'] == 'closed'
        reattack_requested = None
        reattack_date = None
        reattack_requester = None
        n_requested_reattacks = None
        remediation_effectiveness = EMPTY
        if historic_verification:
            reattack_requested = (
                historic_verification[-1]['status'] == 'REQUESTED'
            )
            n_requested_reattacks = len([
                state
                for state in historic_verification
                if state['status'] == 'REQUESTED'
            ])
            if vuln_closed:
                remediation_effectiveness = f'{100 / n_requested_reattacks}%'
            if reattack_requested:
                reattack_date = datetime.strptime(
                    historic_verification[-1]['date'], '%Y-%m-%d %H:%M:%S'
                )
                reattack_requester = historic_verification[-1]['user']
        reattack_data = {
            'Pending Reattack': 'Yes' if reattack_requested else 'No',
            '# Requested Reattacks': n_requested_reattacks or '0',
            'Last requested reattack': reattack_date or EMPTY,
            'Last reattack Requester': reattack_requester or EMPTY,
            'Remediation Effectiveness': remediation_effectiveness
        }
        for key, value in reattack_data.items():
            self.row_values[self.vulnerability[key]] = value
