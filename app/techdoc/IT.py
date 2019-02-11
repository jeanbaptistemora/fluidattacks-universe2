# -*- coding: utf-8 -*-
""" Class for generate an xlsx file with findings information. """
import re
from openpyxl import load_workbook


class ITReport(object):
    """Class to generate IT reports."""

    workbook = None
    current_sheet = None
    data = None
    lang = None
    row = 3
    qc_row = 3
    result_filename = ''
    result_path = '/usr/src/app/app/techdoc/results/'
    templates = {
        'es': {
            'NOQC': '/usr/src/app/app/techdoc/templates/NOQC.xlsx',
            'QC': '/usr/src/app/app/techdoc/templates/QC.xlsx'
        },
        'en': {}}
    sheet_names = {
        'es': {
            'finding': 'Hallazgos',
            'qc_matriz': 'MatrizQC'
        },
        'en': {}}
    finding = {
        'name': 2,
        'description': 3,
        'where': 4,
        'where_records': 5,
        'requirements': 6,
        'measurements': 8,
        'criticity': 9,
        'cardinality': 10,
        'affected_records': 11,
        'evidence': 12,
        'solution': 13,
        'requirements_id': 15}
    matriz = {
        'type': 5,
        'component': 6,
        'requirements_id': 8,
        'requirements': 9,
        'scenario': 13,
        'ambit': 17,
        'category': 18,
        'threat': 19,
        'cssv2_value': 24,
        'probability': 26,
        'severity': 27,
        'risk': 30}

    def __init__(self, project, data, username, lang='es'):
        """Initialize variables."""
        self.lang = lang
        report_format = self.detect_format(data)
        self.generate(data, project, username, report_format)

    def detect_format(self, data):
        detailed = 0
        for finding in data:
            if finding['reportLevel'] == 'DETAILED':
                detailed += 1
        detailed = detailed * 100 / len(data)
        if detailed >= 50:
            self.workbook = load_workbook(
                filename=self.templates[self.lang]['QC']
            )
            return 'QC'
        self.workbook = load_workbook(
            filename=self.templates[self.lang]['NOQC']
        )
        return 'NOQC'

    def hide_cell(self, data, report_format):
        init_row = 3 + 10 * len(data)
        end_row = 3 + 10 * 50
        self.__select_finding_sheet()
        for row in range(init_row, end_row):
            self.current_sheet.row_dimensions[row].hidden = True
        if report_format == 'QC':
            init_row_qc = 3 + 1 * len(data)
            end_row_qc = 53
            self.__select_qc_sheet()
            for row in range(init_row_qc, end_row_qc):
                self.current_sheet.row_dimensions[row].hidden = True

    def generate(self, data, project, username, report_format):
        for finding in data:
            self.__write(finding)
            self.row += 10
            if report_format == 'QC':
                self.__write_qc(finding)
                self.qc_row += 1
        self.hide_cell(data, report_format)
        self.__save(project, username)

    def __select_finding_sheet(self):
        """Select finding sheet."""
        self.current_sheet = self.workbook[
            self.sheet_names[self.lang]['finding']
        ]

    def __select_qc_sheet(self):
        """Select QC matrix sheet."""
        self.current_sheet = self.workbook[
            self.sheet_names[self.lang]['qc_matriz']
        ]

    def set_cell(self, col, value, inc=0):
        """Assign a value to a cell with findings index."""
        self.current_sheet.cell(row=self.row + inc, column=col).value = value

    def set_cell_number(self, col, value, inc=0):
        """Assign a numeric value to a cell with findings index."""
        self.current_sheet.cell(row=self.row + inc, column=col).value = float(value)

    def set_cell_qc(self, col, value, inc=0):
        """Assign a value to a cell with QC index."""
        self.current_sheet.cell(row=self.qc_row + inc, column=col).value = value

    def set_cell_number_qc(self, col, value, inc=0):
        """Assign a numeric value to a cell with QC index."""
        self.current_sheet.cell(row=self.qc_row + inc, column=col).value = float(value)

    def __get_measure(self, metric, metric_value): # noqa
        """Extract number of CSSV2 metrics."""
        try:
            metrics = {
                'accessVector': {
                    '0.395': 'Local',
                    '0.646': 'Red adyacente',
                    '1.0': 'Red',
                },
                'confidentialityImpact': {
                    '0.0': 'Ninguno',
                    '0.275': 'Parcial',
                    '0.66': 'Completo',
                },
                'integrityImpact': {
                    '0.0': 'Ninguno',
                    '0.275': 'Parcial',
                    '0.66': 'Completo',
                },
                'availabilityImpact': {
                    '0.0': 'Ninguno',
                    '0.275': 'Parcial',
                    '0.66': 'Completo',
                },
                'authentication': {
                    '0.45': 'Múltiple',
                    '0.56': 'Única',
                    '0.704': 'Ninguna',
                },
                'exploitability': {
                    '0.85': 'Improbable',
                    '0.9': 'Conceptual',
                    '0.95': 'Funcional',
                    '1.0': 'Alta',
                },
                'confidenceLevel': {
                    '0.9': 'No confirmado',
                    '0.95': 'No corroborado',
                    '1.0': 'Confirmado',
                },
                'resolutionLevel': {
                    '0.87': 'Oficial',
                    '0.9': 'Temporal',
                    '0.95': 'Paliativa',
                    '1.0': 'Inexistente',
                },
                'accessComplexity': {
                    '0.35': 'Alto',
                    '0.61': 'Medio',
                    '0.71': 'Bajo',
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

    def __get_req(self, req_vect): # noqa
        """Get all the identifiers with the REQ.XXXX format."""
        try:
            reqs = re.findall('REQ\\.\\d{3,4}', req_vect) # noqa
            reqs = [x.replace('REQ.', '') for x in reqs]
            reqs_list = '|'.join(reqs)
            return '.*(' + reqs_list + ')'
        except ValueError:
            return ''

    def __write(self, row):
        """Write Formstack finding in a row on the Findings sheet."""
        self.__select_finding_sheet()
        self.set_cell(self.finding['name'], row['finding'])
        self.set_cell(self.finding['description'], row['vulnerability'])
        self.set_cell(self.finding['where'], row['where'])
        if int(row['recordsNumber']) != 0:
            self.set_cell(self.finding['where_records'],
                          'Evidencias/' + row['finding'] + '/records.csv')
        self.set_cell(self.finding['requirements'], row['requirements'])
        self.set_cell_number(self.finding['criticity'], row['criticity'])
        self.set_cell_number(self.finding['cardinality'], row['openVulnerabilities'])
        self.set_cell_number(self.finding['affected_records'], row['recordsNumber'])
        self.set_cell(self.finding['evidence'], 'Evidencias/' + row['finding'])
        self.set_cell(self.finding['solution'], row['effectSolution'])
        self.set_cell(self.finding['requirements_id'],
                      self.__get_req(row['requirements']))
        self.set_cell(self.finding['measurements'],
                      self.__get_measure('accessVector', row['accessVector']))
        self.set_cell(
            self.finding['measurements'],
            get_complexity(self.__get_measure(
                'accessComplexity', row['accessComplexity'])),
            1)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('authentication', row['authentication']),
            2)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('confidentialityImpact', row['confidentialityImpact']),
            3)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('integrityImpact', row['integrityImpact']),
            4)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('availabilityImpact', row['availabilityImpact']),
            5)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('exploitability', row['exploitability']),
            6)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('resolutionLevel', row['resolutionLevel']),
            7)
        self.set_cell(
            self.finding['measurements'],
            self.__get_measure('confidenceLevel', row['confidenceLevel']),
            8)

    def __write_qc(self, row):
        """Write Formstack finding in a row on the QC matrix sheet."""
        self.__select_qc_sheet()
        self.set_cell_qc(self.matriz['type'],
                         translate_parameter(row['testType']))
        self.set_cell_qc(self.matriz['component'], row['clientProject'])
        self.set_cell_qc(self.matriz['requirements_id'],
                         self.__get_req(row['requirements']))
        self.set_cell_qc(self.matriz['requirements'], row['requirements'])
        if 'scenario' in row:
            self.set_cell_qc(self.matriz['scenario'],
                             translate_parameter(row['scenario']))
        if 'ambit' in row:
            self.set_cell_qc(self.matriz['ambit'], row['ambit'])
        if 'category' in row:
            self.set_cell_qc(self.matriz['category'], row['category'])
        if 'threat' in row:
            self.set_cell_qc(self.matriz['threat'], row['threat'])
        criticity = row['criticity']
        if criticity > 6.9:
            self.set_cell_qc(self.matriz['cssv2_value'], 'Alta')
        elif criticity >= 4.0:
            self.set_cell_qc(self.matriz['cssv2_value'], 'Media')
        else:
            self.set_cell_qc(self.matriz['cssv2_value'], 'Baja')
        if 'probability' in row:
            self.set_cell_qc(self.matriz['probability'], row['probability'])
        if 'severity' in row:
            self.set_cell_number_qc(self.matriz['severity'], row['severity'])
        if 'risk' in row:
            self.set_cell_qc(self.matriz['risk'], row['risk'])

    def __save(self, project, username):
        self.result_filename = self.result_path
        self.result_filename += project + '_' + username + '.xlsx'
        self.workbook.save(self.result_filename)


def get_complexity(complexity_access):
    if complexity_access == 'Bajo':
        return 'Baja'
    elif complexity_access == 'Alto':
        return 'Alta'
    elif complexity_access == 'Medio':
        return 'Media'
    return complexity_access


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
        'UNAUTHORIZED_USER_INTRANET': 'Intranet usuario no autorizado'
    }
    return translation_values.get(param)
