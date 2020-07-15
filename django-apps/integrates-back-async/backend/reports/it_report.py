# -*- coding: utf-8 -*-
""" Class for generate an xlsx file with findings information. """
import os
import re
from typing import cast, Dict, List, Optional, Union

from datetime import datetime
from django.conf import settings
from asgiref.sync import async_to_sync
import pytz
from openpyxl import load_workbook
from openpyxl.styles import Alignment, stylesheet
from backend.domain import vulnerability as vuln_domain
from backend.domain.finding import get_finding
from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType,
    Vulnerability as VulnType
)


class ITReport():
    """Class to generate IT reports."""

    workbook = None
    current_sheet: stylesheet.Stylesheet = None
    data = None
    lang = None
    row = 2
    result_filename = ''
    project_name = ''
    base = (
        '/usr/src/app/django-apps/integrates-back-async/backend/reports'
    )
    result_path = os.path.join(base, 'results/results_excel')
    templates: Dict[str, Dict[str, str]] = {
        'es': {
            'TECHNICAL': os.path.join(
                base, 'templates/excel', 'TECHNICAL_VULNS.xlsx'),
        },
        'en': {}}
    sheet_names = {
        'es': {
            'data': 'Data',
        },
        'en': {}}
    vulnerability = {
        'number': 1,
        'finding': 2,
        'finding_id': 3,
        'vuln_uuid': 4,
        'where': 5,
        'specific': 6,
        'description': 7,
        'status': 8,
        'severity': 9,
        'requirements': 10,
        'impact': 11,
        'affected_systems': 12,
        'threat': 13,
        'recommendation': 14,
        'external_bts': 15,
        'compromised_attributes': 16,
        'n_compromised_attributes': 17,
        'tags': 18,
        'business_critically': 19,
        'vuln_report_date': 20,
        'vuln_close_date': 21,
        'vuln_age': 22,
        'treatment': 23,
        'treatment_date': 24,
        'treatment_justification': 25,
        'treatment_exp_date': 26,
        'treatment_manager': 27,
        'reattack': 28,
        'n_requested_reattacks': 29,
        'remediation_effectiveness': 30,
        'last_reattack_date': 31,
        'last_reattack_requester': 32,
        'cvss_vector': 33,
    }

    def __init__(self, data: List[Dict[str, FindingType]], lang: str = 'es'):
        """Initialize variables."""
        self.lang = lang
        self.workbook = load_workbook(
            filename=self.templates[self.lang]['TECHNICAL']
        )
        self.generate(data)

    def hide_cell(self, data: List[FindingType]):
        init_row = 3 + 12 * len(data)
        end_row = 3 + 12 * 70
        self.__select_finding_sheet()
        for row in range(init_row, end_row):
            self.current_sheet.row_dimensions[row].hidden = True

    def generate(self, data: List[Dict[str, FindingType]]):
        self.project_name = str(data[0].get('projectName'))
        vulns = async_to_sync(vuln_domain.list_vulnerabilities_async)(
            [finding.get('findingId') for finding in data])

        for vuln in vulns:
            self.__write_vuln_row(vuln)
            self.row += 1
        self.__save()

    def __select_finding_sheet(self):
        """Select finding sheet."""
        self.current_sheet = self.workbook[
            self.sheet_names[self.lang]['data']
        ]

    def set_cell(
        self,
        col: int,
        value: Union[str, int, datetime],
        inc: int = 0,
        align: str = 'center'
    ):
        """Assign a value to a cell with findings index."""
        alignment = Alignment(
            horizontal=align,
            vertical='center',
            wrap_text=True
        )
        self.current_sheet.cell(
            row=self.row + inc, column=col).alignment = alignment
        self.current_sheet.cell(row=self.row + inc, column=col).value = value

    def __get_req(self, req_vect: str): # noqa
        """Get all the identifiers with the REQ.XXXX format."""
        try:
            reqs = re.findall('REQ\\.\\d{3,4}', req_vect) # noqa
            reqs = [x.replace('REQ.', '') for x in reqs]
            reqs_list = '|'.join(reqs)
            return '.*(' + reqs_list + ')'
        except ValueError:
            return ''

    @classmethod
    def __get_measure(
        cls,
        metric: str,
        metric_value: str
    ) -> Optional[str]: # noqa
        """Extract number of CSSV metrics."""
        try:
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
            metric_descriptions = metrics.get(metric)
            if metric_descriptions:
                description = metric_descriptions.get(str(metric_value))
            else:
                description = ''
            return description
        except ValueError:
            return ''

    def set_cvss_metrics_cell(self, row: VulnType):
        measures = {
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
        metric_vector = []
        for index, (indicator, measure) in enumerate(measures.items()):
            value = self.__get_measure(
                measure,
                cast(Dict[str, str], row['severity'])[measure]
            )
            if value:
                metric_vector.append(f'{indicator}:{value[0]}')
                self.set_cell(
                    self.vulnerability['cvss_vector'] + index + 1, value)

        cvss_metric_vector = '/'.join(metric_vector)
        cvss_calculator_url = (
            f'https://www.first.org/cvss/calculator/3.1#CVSS:3.1'
            f'/{cvss_metric_vector}'
        )
        cell_content = \
            f'=HYPERLINK("{cvss_calculator_url}", "{cvss_metric_vector}")'
        self.set_cell(
            self.vulnerability['cvss_vector'], cell_content)

    def __write_vuln_row(self, row: VulnType):
        finding = async_to_sync(get_finding)(row.get('finding_id'))
        specific = str(row.get('specific', ''))
        if row.get('vuln_type') == 'lines':
            specific = str(int(specific))
        tags = '-'
        if 'tag' in row:
            tags = ', '.join(str(row.get('tag')))

        self.__select_finding_sheet()

        self.set_cell(self.vulnerability['number'], self.row - 1)
        self.set_cell(
            self.vulnerability['finding'],
            finding.get('finding'),
            align='left'
        )
        self.set_cell(
            self.vulnerability['finding_id'],
            finding.get('findingId', '-')
        )
        self.set_cell(
            self.vulnerability['vuln_uuid'],
            str(row.get('UUID', '-'))
        )
        self.set_cell(self.vulnerability['where'], str(row.get("where")))
        self.set_cell(self.vulnerability['specific'], specific)
        self.set_cell(self.vulnerability['tags'], tags, align='left')
        self.set_cell(
            self.vulnerability['business_critically'],
            str(row.get('severity', '-'))
        )

        self.write_finding_data(finding, row)
        self.write_vuln_temporal_data(row)
        self.write_treatment_data(finding, row)
        self.write_reattack_data(finding, row)
        self.set_cvss_metrics_cell(finding)

    def write_finding_data(
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ):
        compromised_attributes = str(finding.get('compromisedAttrs')) or '-'
        n_compromised_attributes = None
        if compromised_attributes != '-':
            n_compromised_attributes = \
                str(len(compromised_attributes.split('\n')))
        external_bts = finding.get('externalBts', '-')

        self.set_cell(
            self.vulnerability['description'],
            str(finding.get('vulnerability', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['status'],
            cast(HistoricType, vuln.get('historic_state'))[-1]['state']
        )
        self.set_cell(
            self.vulnerability['severity'],
            str(finding.get('severityCvss', '-'))
        )
        self.set_cell(
            self.vulnerability['requirements'],
            str(finding.get('requirements', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['impact'],
            str(finding.get('attackVectorDesc', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['affected_systems'],
            str(finding.get('affectedSystems', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['threat'],
            str(finding.get('threat', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['recommendation'],
            str(finding.get('effectSolution', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['external_bts'],
            f'=HYPERLINK("{external_bts}", "{external_bts}")',
            align='left'
        )
        self.set_cell(
            self.vulnerability['compromised_attributes'],
            compromised_attributes,
            align='left'
        )
        self.set_cell(
            self.vulnerability['n_compromised_attributes'],
            n_compromised_attributes or '0'
        )

    def write_vuln_temporal_data(self, vuln: VulnType):
        vuln_historic_state = cast(HistoricType, vuln.get('historic_state'))
        vuln_date = datetime.strptime(
            vuln_historic_state[0]['date'], '%Y-%m-%d %H:%M:%S')
        vuln_closed = vuln_historic_state[-1]['state'] == 'closed'
        limit_date = datetime.today()
        if vuln_closed:
            limit_date = datetime.strptime(
                vuln_historic_state[-1]['date'], '%Y-%m-%d %H:%M:%S'
            )
        vuln_age_days = int((limit_date - vuln_date).days)
        vuln_age = f'{vuln_age_days} '

        self.set_cell(self.vulnerability['vuln_report_date'], vuln_date)
        self.set_cell(self.vulnerability['vuln_age'], vuln_age)
        self.set_cell(
            self.vulnerability['vuln_close_date'],
            datetime.strptime(
                vuln_historic_state[-1]['date'], '%Y-%m-%d %H:%M:%S')
            if vuln_closed else '-'
        )

    def write_treatment_data(
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ):
        treatment = \
            str(vuln.get('treatment', 'NEW')).capitalize().replace('_', ' ')
        if treatment == 'Accepted undefined':
            treatment = 'Eternally accepted'
        elif treatment == 'Accepted':
            treatment = 'Temporarily accepted'
        self.set_cell(
            self.vulnerability['treatment'],
            treatment
        )
        self.set_cell(
            self.vulnerability['treatment_date'],
            datetime.strptime(
                cast(HistoricType, finding.get('historicState'))[-1]['date'],
                '%Y-%m-%d %H:%M:%S'
            )
            if 'historicState' in finding and
            'date' in cast(HistoricType, finding.get('historicState'))[-1]
            else '-'
        )
        self.set_cell(
            self.vulnerability['treatment_justification'],
            str(vuln.get('treatment_justification', '-')),
            align='left'
        )
        self.set_cell(
            self.vulnerability['treatment_exp_date'],
            datetime.strptime(
                str(vuln.get('acceptance_date')), '%Y-%m-%d %H:%M:%S')
            if 'acceptance_date' in vuln else '-'
        )
        self.set_cell(
            self.vulnerability['treatment_manager'],
            str(vuln.get('treatment_manager', '-'))
        )

    def write_reattack_data(
        self,
        finding: Dict[str, FindingType],
        vuln: VulnType
    ):
        historic_verification = \
            cast(HistoricType, finding.get('historicVerification'))
        vuln_closed = cast(
            HistoricType, vuln.get('historic_state'))[-1]['state'] == 'closed'
        reattack_requested = None
        reattack_date = None
        reattack_requester = None
        n_requested_reattacks = None
        remediation_effectiveness = '-'
        if historic_verification:
            reattack_requested = \
                historic_verification[-1]['status'] == 'REQUESTED'
            n_requested_reattacks = \
                len([
                    state for state in historic_verification
                    if state['status'] == 'REQUESTED'
                ])
            if vuln_closed:
                remediation_effectiveness = f'{100 / n_requested_reattacks}%'
            if reattack_requested:
                reattack_date = datetime.strptime(
                    historic_verification[-1]['date'], '%Y-%m-%d %H:%M:%S')
                reattack_requester = historic_verification[-1]['user']

        self.set_cell(
            self.vulnerability['reattack'],
            'Yes' if reattack_requested else 'No'
        )
        self.set_cell(
            self.vulnerability['n_requested_reattacks'],
            n_requested_reattacks or '0'
        )
        self.set_cell(
            self.vulnerability['last_reattack_date'],
            reattack_date or '-'
        )
        self.set_cell(
            self.vulnerability['last_reattack_requester'],
            reattack_requester or '-'
        )
        self.set_cell(
            self.vulnerability['remediation_effectiveness'],
            remediation_effectiveness
        )

    def __save(self):
        tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
        today_date = datetime.now(tz=tzn).today().strftime('%Y-%m-%dT%H-%M-%S')
        self.result_filename = (
            f'{self.project_name}-vulnerabilities-{today_date}.xlsx'
        )
        self.workbook.save(self.result_filename)


def translate_parameter(param: str) -> str:
    translation_values = {
        'CONTINUOUS': 'Continua',
        'ANALYSIS': 'Análisis',
        'APP': 'Aplicación',
        'BINARY': 'Binario',
        'SOURCE_CODE': 'Código fuente',
        'INFRASTRUCTURE': 'Infraestructura',
        'ANONYMOUS_INTERNET': 'Anónimo desde internet',
        'ANONYMOUS_INTRANET': 'Anónimo desde intranet',
        'AUTHORIZED_USER_EXTRANET': 'Extranet usuario autorizado',
        'UNAUTHORIZED_USER_EXTRANET': 'Extranet usuario no autorizado',
        'AUTHORIZED_USER_INTERNET': 'Internet usuario autorizado',
        'UNAUTHORIZED_USER_INTERNET': 'Internet usuario no autorizado',
        'AUTHORIZED_USER_INTRANET': 'Intranet usuario autorizado',
        'UNAUTHORIZED_USER_INTRANET': 'Intranet usuario no autorizado',
        'APPLICATIONS': 'Aplicaciones',
        'DATABASES': 'Bases de Datos'
    }
    return str(translation_values.get(param))
