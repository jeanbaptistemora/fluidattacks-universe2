# -*- coding: utf-8 -*-
""" Class for generate an xlsx file with findings information. """
import os
import re
import uuid
from typing import cast

from datetime import datetime
from asgiref.sync import async_to_sync
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from backend.domain import vulnerability as vuln_domain
from backend.domain.finding import get_finding
from backend.typing import (
    Historic as HistoricType,
    Vulnerability as VulnType
)


class ITReport():
    """Class to generate IT reports."""

    workbook = None
    current_sheet = None
    data = None
    lang = None
    row = 2
    result_filename = ''
    base = (
        '/usr/src/app/django-apps/integrates-back-async/backend/reports'
    )
    result_path = os.path.join(base, 'results/results_excel')
    templates = {
        'es': {
            'TECHNICAL': os.path.join(
                base, 'templates/excel', 'TECHNICAL_VULNS.xlsx'),
        },
        'en': {}}
    sheet_names = {
        'es': {
            'finding': 'Findings',
        },
        'en': {}}
    finding = {
        'name': 2,
        'description': 3,
        'where': 4,
        'where_records': 5,
        'measurements': 7,
        'severityCvss': 8,
        'cardinality': 9,
        'affected_records': 10,
        'evidence': 11,
        'solution': 12,
        'requirements_id': 13
    }
    vulnerability = {
        'finding': 3,
        'specific': 2,
        'severity': 5,
        'status': 4,
        'cvss_vector': 6,
        'reattack': 7,
        'exploitable': 8,
        'report_date': 9,
        'age': 11,
        'close_date': 10,
        'treatment': 12,
        'treatment_date': 13,
        'treatment_justification': 14,
        'treatment_exp_date': 15,
        'treatment_manager': 16
    }

    def __init__(self, data, lang='es'):
        """Initialize variables."""
        self.lang = lang
        self.workbook = load_workbook(
            filename=self.templates[self.lang]['TECHNICAL']
        )
        self.generate(data)

    def hide_cell(self, data):
        init_row = 3 + 12 * len(data)
        end_row = 3 + 12 * 70
        self.__select_finding_sheet()
        for row in range(init_row, end_row):
            self.current_sheet.row_dimensions[row].hidden = True

    def generate(self, data):
        vulns = async_to_sync(vuln_domain.list_vulnerabilities_async)(
            [finding.get('findingId') for finding in data])

        for vuln in vulns:
            self.__write_vuln_row(vuln)
            self.row += 1
        self.__save()

    def __select_finding_sheet(self):
        """Select finding sheet."""
        self.current_sheet = self.workbook[
            self.sheet_names[self.lang]['finding']
        ]

    def set_cell(self, col, value, inc=0):
        """Assign a value to a cell with findings index."""
        alignment = Alignment(horizontal='center', vertical='center')
        self.current_sheet.cell(
            row=self.row + inc, column=col).alignment = alignment
        self.current_sheet.cell(row=self.row + inc, column=col).value = value

    def set_cell_number(self, col, value, inc=0):
        """Assign a numeric value to a cell with findings index."""
        self.current_sheet.cell(
            row=self.row + inc, column=col).value = float(value)

    def __get_req(self, req_vect): # noqa
        """Get all the identifiers with the REQ.XXXX format."""
        try:
            reqs = re.findall('REQ\\.\\d{3,4}', req_vect) # noqa
            reqs = [x.replace('REQ.', '') for x in reqs]
            reqs_list = '|'.join(reqs)
            return '.*(' + reqs_list + ')'
        except ValueError:
            return ''

    def __get_measure(self, metric, metric_value): # noqa
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

    def set_cvss_metrics_cell(self, row):
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
        for indicator, measure in measures.items():
            value = self.__get_measure(measure, row['severity'][measure])[0]
            metric_vector.append(f'{indicator}:{value}')

        self.set_cell(
            self.vulnerability['cvss_vector'], '/'.join(metric_vector))

    def __write_vuln_row(self, row: VulnType):
        finding = async_to_sync(get_finding)(row.get('finding_id'))
        specific = str(row.get('specific', ''))
        if row.get('vuln_type') == 'lines':
            specific = str(int(specific))
        where_specific = f'{row.get("where")}:{specific}'
        vuln_historic_state = cast(HistoricType, row.get('historic_state'))
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
        reattack_requested = \
            finding.get('historic_verification')[-1]['status'] == 'REQUESTED' \
            if 'historic_verification' in finding else False
        is_exploitable = 'Yes' if finding.get('exploitable') else 'No'

        self.__select_finding_sheet()
        self.set_cell(1, self.row - 1)
        self.set_cell(self.vulnerability['finding'], finding.get('finding'))
        self.set_cell(self.vulnerability['specific'], where_specific)
        self.set_cell(
            self.vulnerability['severity'],
            finding.get('severityCvss', '-')
        )

        self.set_cvss_metrics_cell(finding)

        self.set_cell(
            self.vulnerability['status'],
            vuln_historic_state[-1]['state']
        )
        self.set_cell(
            self.vulnerability['reattack'],
            'Yes' if reattack_requested else 'No'
        )
        self.set_cell(self.vulnerability['exploitable'], is_exploitable)

        self.set_cell(self.vulnerability['report_date'], vuln_date)
        self.set_cell(self.vulnerability['age'], vuln_age)
        self.set_cell(
            self.vulnerability['close_date'],
            datetime.strptime(
                vuln_historic_state[-1]['date'], '%Y-%m-%d %H:%M:%S')
            if vuln_closed else '-'
        )

        self.set_cell(
            self.vulnerability['treatment'],
            str(row.get('treatment', 'NEW')).capitalize()
        )
        self.set_cell(
            self.vulnerability['treatment_date'],
            datetime.strptime(
                finding.get('historicState')[-1]['date'], '%Y-%m-%d %H:%M:%S')
            if 'historicState' in finding else '-'
        )
        self.set_cell(
            self.vulnerability['treatment_justification'],
            row.get('treatment_justification', '-')
        )
        self.set_cell(
            self.vulnerability['treatment_exp_date'],
            datetime.strptime(
                str(row.get('acceptance_date')), '%Y-%m-%d %H:%M:%S')
            if 'acceptance_date' in row else '-'
        )
        self.set_cell(
            self.vulnerability['treatment_manager'],
            row.get('treatment_manager', '-')
        )

    def __write(self, row):
        """Write Formstack finding in a row on the Findings sheet."""
        self.__select_finding_sheet()
        self.set_cell(self.finding['name'], row['finding'])
        self.set_cell(self.finding['description'], row['vulnerability'])
        self.set_cell(self.finding['where'], row.get('where', ''))
        if int(row.get('recordsNumber', 0)) > 0:
            self.set_cell(self.finding['where_records'],
                          'Evidences/' + row['finding'] + '/records.csv')
        self.set_cell_number(self.finding['severityCvss'], row['severityCvss'])
        self.set_cell_number(
            self.finding['cardinality'], row['openVulnerabilities'])
        self.set_cell_number(
            self.finding['affected_records'], row.get('recordsNumber', '0'))
        self.set_cell(self.finding['evidence'], 'Evidences/' + row['finding'])
        self.set_cell(self.finding['solution'], row['effectSolution'])
        self.set_cell(self.finding['requirements_id'],
                      self.__get_req(row['requirements']))
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'attackVector', row['severity']['attackVector']))
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'attackComplexity', row['severity']['attackComplexity']), 1)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'privilegesRequired', row['severity']['privilegesRequired']),
            2)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'userInteraction', row['severity']['userInteraction']), 3)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'severityScope', row['severity']['severityScope']), 4)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'confidentialityImpact',
                row['severity']['confidentialityImpact']),
            5)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'integrityImpact', row['severity']['integrityImpact']), 6)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'availabilityImpact', row['severity']['availabilityImpact']),
            7)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'exploitability', row['severity']['exploitability']), 8)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'remediationLevel', row['severity']['remediationLevel']), 9)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure(
                'reportConfidence', row['severity']['reportConfidence']), 10)

    def __save(self):
        self.result_filename = str(uuid.uuid4()) + '.xlsx'
        self.workbook.save(self.result_filename)


def translate_parameter(param):
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
    return translation_values.get(param)
