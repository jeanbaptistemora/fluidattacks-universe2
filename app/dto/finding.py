""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
import base64
from datetime import datetime
import uuid

import pytz
import rollbar
import itertools
from operator import itemgetter
from django.conf import settings

from ..dao import integrates_dao
from . import closing
from ..api.formstack import FormstackAPI
from ..utils import forms
from .. import util
from ..exceptions import InvalidRange
from decimal import Decimal


# pylint: disable=E0402

class FindingDTO(object):
    """Class to create an object with the attributes of a finding."""

    FIELDS_FINDING = settings.FIELDS_FINDING
    #Atributos proyecto
    ANALIST = FIELDS_FINDING['ANALIST']
    LEADER = FIELDS_FINDING['LEADER']
    INTERESADO = FIELDS_FINDING['INTERESADO']
    PROJECT_NAME = FIELDS_FINDING['PROJECT_NAME']
    CLIENT_PROJECT = FIELDS_FINDING['CLIENT_PROJECT']
    CONTEXT = FIELDS_FINDING['CONTEXT']
    REVISION = FIELDS_FINDING['REVISION']

    #Atributos evidencia
    DOC_TOTAL = FIELDS_FINDING['DOC_TOTAL']
    DOC_ACHV1 = FIELDS_FINDING['DOC_ACHV1']
    DOC_ACHV2 = FIELDS_FINDING['DOC_ACHV2']
    DOC_ACHV3 = FIELDS_FINDING['DOC_ACHV3']
    DOC_ACHV4 = FIELDS_FINDING['DOC_ACHV4']
    DOC_ACHV5 = FIELDS_FINDING['DOC_ACHV5']
    DOC_CMNT1 = FIELDS_FINDING['DOC_CMNT1']
    DOC_CMNT2 = FIELDS_FINDING['DOC_CMNT2']
    DOC_CMNT3 = FIELDS_FINDING['DOC_CMNT3']
    DOC_CMNT4 = FIELDS_FINDING['DOC_CMNT4']
    DOC_CMNT5 = FIELDS_FINDING['DOC_CMNT5']
    ANIMATION = FIELDS_FINDING['ANIMATION']
    EXPLOTATION = FIELDS_FINDING['EXPLOTATION']
    EXPLOIT = FIELDS_FINDING['EXPLOIT']
    REG = FIELDS_FINDING['REG']
    REG_NUM = FIELDS_FINDING['REG_NUM']
    REG_FILE = FIELDS_FINDING['REG_FILE']
    VULNERABILITIES_FILE = FIELDS_FINDING['VULNERABILITIES_FILE']

    #Atributos descriptivos
    REPORT_LEVEL = FIELDS_FINDING['REPORT_LEVEL'] #detallado
    FINDING = FIELDS_FINDING['FINDING']
    TEST_TYPE = FIELDS_FINDING['TEST_TYPE']
    SUBSCRIPTION = FIELDS_FINDING['SUBSCRIPTION']
    CLIENT_CODE = FIELDS_FINDING['CLIENT_CODE']
    PROBABILITY = FIELDS_FINDING['PROBABILITY']
    SEVERITY = FIELDS_FINDING['SEVERITY']
    RISK_VALUE = FIELDS_FINDING['RISK_VALUE']
    CARDINALITY = FIELDS_FINDING['CARDINALITY']
    WHERE = FIELDS_FINDING['WHERE']
    VULNERABILITY = FIELDS_FINDING['VULNERABILITY']
    THREAT = FIELDS_FINDING['THREAT']
    FINDING_TYPE = FIELDS_FINDING['FINDING_TYPE']
    RISK = FIELDS_FINDING['RISK']
    REQUIREMENTS = FIELDS_FINDING['REQUIREMENTS']
    EFFECT_SOLUTION = FIELDS_FINDING['EFFECT_SOLUTION']
    KB_LINK = FIELDS_FINDING['KB']
    ACTOR = FIELDS_FINDING['ACTOR']
    CATEGORY = FIELDS_FINDING['CATEGORY']
    SCENARIO = FIELDS_FINDING['SCENARIO']
    AMBIT = FIELDS_FINDING['AMBIT']
    AFFECTED_SYSTEMS = FIELDS_FINDING['AFFECTED_SYSTEMS']
    ATTACK_VECTOR = FIELDS_FINDING['ATTACK_VECTOR']
    CWE = FIELDS_FINDING['CWE']
    TREATMENT = FIELDS_FINDING['TREATMENT']
    TREATMENT_JUSTIFICATION = FIELDS_FINDING['TREATMENT_JUSTIFICATION']
    TREATMENT_MANAGER = FIELDS_FINDING['TREATMENT_MANAGER']
    EXTERNAL_BTS = FIELDS_FINDING['EXTERNAL_BTS']
    LAST_VULNERABILITY = FIELDS_FINDING['LAST_VULNERABILITY']
    RELEASE_DATE = FIELDS_FINDING['RELEASE_DATE']
    RELATED_FINDINGS = FIELDS_FINDING['RELATED_FINDINGS']

    #Atributos CssV2
    ACCESS_VECTOR = FIELDS_FINDING['ACCESS_VECTOR']
    ACCESS_COMPLEXITY = FIELDS_FINDING['ACCESS_COMPLEXITY']
    AUTHENTICATION = FIELDS_FINDING['AUTHENTICATION']
    EXPLOITABILITY = FIELDS_FINDING['EXPLOITABILITY']
    CONFIDENTIALITY_IMPACT = FIELDS_FINDING['CONFIDENTIALITY_IMPACT']
    INTEGRITY_IMPACT = FIELDS_FINDING['INTEGRITY_IMPACT']
    AVAILABILITY_IMPACT = FIELDS_FINDING['AVAILABILITY_IMPACT']
    RESOLUTION_LEVEL = FIELDS_FINDING['RESOLUTION_LEVEL']
    CONFIDENCE_LEVEL = FIELDS_FINDING['CONFIDENCE_LEVEL']
    COLLATERAL_DAMAGE_POTENTIAL = FIELDS_FINDING['COLLATERAL_DAMAGE_POTENTIAL']
    FINDING_DISTRIBUTION = FIELDS_FINDING['FINDING_DISTRIBUTION']
    CONFIDENTIALITY_REQUIREMENT = FIELDS_FINDING['CONFIDENTIALITY_REQUIREMENT']
    INTEGRITY_REQUIREMENT = FIELDS_FINDING['INTEGRITY_REQUIREMENT']
    AVAILABILITY_REQUIREMENT = FIELDS_FINDING['AVAILABILITY_REQUIREMENT']

    def __init__(self):
        """Class constructor."""
        self.request_id = None
        self.data = dict()

    def create_evidence_description(self, parameter): # noqa: C901
        """Convert the index of a JSON to Formstack index."""
        evidence_description_fields = {
            self.DOC_CMNT1: 'evidenceDescription1',
            self.DOC_CMNT2: 'evidenceDescription2',
            self.DOC_CMNT3: 'evidenceDescription3',
            self.DOC_CMNT4: 'evidenceDescription4',
            self.DOC_CMNT5: 'evidenceDescription5'
        }
        parsed_dict = {k: parameter['data[' + v + ']']
                       for (k, v) in evidence_description_fields.items()
                       if 'data[' + v + ']' in parameter.keys()}
        return {'data': parsed_dict, 'request_id': parameter['data[id]']}

    def parse_evidence_description(self, description_field, value):
        """ Convert evidence description data to Formstack payload format. """
        formstack_fields = {
            'evidence2_description': self.DOC_CMNT1,
            'evidence3_description': self.DOC_CMNT2,
            'evidence4_description': self.DOC_CMNT3,
            'evidence5_description': self.DOC_CMNT4,
            'evidence6_description': self.DOC_CMNT5,
        }
        return {'data': {formstack_fields[description_field]: value}}

    def create_description(self, parameter): # noqa: C901
        """Convert the index of a JSON to Formstack index."""
        if 'data[id]' in parameter:
            self.request_id \
                = parameter['data[id]']
        if 'data[openVulnerabilities]' in parameter:
            self.data[self.CARDINALITY] \
                = parameter['data[openVulnerabilities]']
        if 'data[vulnerability]' in parameter:
            self.data[self.VULNERABILITY] \
                = parameter['data[vulnerability]']
        if 'data[requirements]' in parameter:
            self.data[self.REQUIREMENTS] \
                = parameter['data[requirements]']
        if 'data[where]' in parameter:
            self.data[self.WHERE] \
                = parameter['data[where]']
        if 'data[effectSolution]' in parameter:
            self.data[self.EFFECT_SOLUTION] \
                = parameter['data[effectSolution]']
        if 'data[threat]' in parameter:
            self.data[self.THREAT] \
                = parameter['data[threat]']
        if 'data[attackVector]' in parameter:
            self.data[self.ATTACK_VECTOR] \
                = parameter['data[attackVector]']
        if 'data[affectedSystems]' in parameter:
            self.data[self.AFFECTED_SYSTEMS] \
                = parameter['data[affectedSystems]']
        if 'data[cwe]' in parameter:
            self.data[self.CWE] \
                = parameter['data[cwe]']
        if 'data[lastVulnerability]' in parameter:
            self.data[self.LAST_VULNERABILITY] \
                = parameter['data[lastVulnerability]']
        if 'data[releaseDate]' in parameter:
            self.data[self.RELEASE_DATE] \
                = parameter['data[releaseDate]']


    def create_treatment(self, parameter):
        """Convert the index of a JSON to Formstack index."""
        treatment_fields = {
            self.TREATMENT: 'treatment',
            self.TREATMENT_JUSTIFICATION: 'treatmentJustification',
            self.TREATMENT_MANAGER: 'treatmentManager',
            self.EXTERNAL_BTS: 'externalBts'
        }
        parsed_dict = {k: parameter['data[' + v + ']']
                       if 'data[' + v + ']' in parameter.keys() else '' \
                       for (k, v) in treatment_fields.items()}
        return {'data': parsed_dict, 'request_id': parameter['data[id]']}

    def create_delete(self, parameter, analyst, project, finding):
        """ Create a data set to send in the finding deletion email """
        return {
            'mail_analista': analyst,
            'name_finding': finding,
            'id_finding': finding,
            'description': parameter['data[justification]'],
            'project': project,
        }

    def parse(self, submission_id, request_arr):
        self.data = dict()
        self.data['id'] = submission_id
        self.data['timestamp'] = request_arr['timestamp']
        self.data = forms.dict_concatenation(self.data, self.parse_description(request_arr, submission_id))
        self.data = forms.dict_concatenation(self.data, self.parse_cvssv2(request_arr, submission_id))
        self.data = forms.dict_concatenation(self.data, self.parse_project(request_arr, submission_id))
        self.data = forms.dict_concatenation(self.data, self.parse_evidence_info(request_arr, submission_id))
        return self.data

    def parse_description(self, request_arr, submission_id): # noqa: C901
        """Convert description of a finding into a formstack format."""
        initial_dict = forms.create_dict(request_arr)
        description_title = ['report_level', 'subscription', 'client_code',
                             'finding', 'probability', 'severity',
                             'risk_value', 'ambit', 'category', 'test_type',
                             'related_findings', 'actor', 'scenario']
        description = integrates_dao.get_finding_attributes_dynamo(
            str(submission_id),
            description_title)
        if description:
            migrated_description_fields = {k: util.snakecase_to_camelcase(k)
                                           for k in description_title}
            migrated_dict = {v: description[k]
                             for (k, v) in migrated_description_fields.items()
                             if k in description.keys()}
        else:
            migrated_description_fields = {
                self.FINDING: 'finding',
                self.SUBSCRIPTION: 'subscription',
                self.CLIENT_CODE: 'clientCode',
                self.PROBABILITY: 'probability',
                self.SEVERITY: 'severity',
                self.RISK_VALUE: 'riskValue',
                self.RELATED_FINDINGS: 'relatedFindings',
                self.REPORT_LEVEL: 'reportLevel',
                self.TEST_TYPE: 'testType',
                self.SCENARIO: 'scenario',
                self.AMBIT: 'ambit',
                self.CATEGORY: 'category',
                self.ACTOR: 'actor',
            }
            migrated_dict = {v: initial_dict[k]
                             for (k, v) in migrated_description_fields.items()
                             if k in initial_dict.keys()}
        description_fields = {
            self.CARDINALITY: 'openVulnerabilities',
            self.WHERE: 'where',
            self.VULNERABILITY: 'vulnerability',
            self.THREAT: 'threat',
            self.RISK: 'risk',
            self.REQUIREMENTS: 'requirements',
            self.EFFECT_SOLUTION: 'effectSolution',
            self.KB_LINK: 'kb',
            self.AFFECTED_SYSTEMS: 'affectedSystems',
            self.ATTACK_VECTOR: 'attackVector',
            self.FINDING_TYPE: 'findingType',
            self.REVISION: 'revision',
            self.TREATMENT: 'treatment',
            self.TREATMENT_JUSTIFICATION: 'treatmentJustification',
            self.TREATMENT_MANAGER: 'treatmentManager',
            self.EXTERNAL_BTS: 'externalBts',
            self.LAST_VULNERABILITY: 'lastVulnerability',
            self.RELEASE_DATE: 'releaseDate',
            self.CWE: 'cwe',
            self.FINDING_TYPE: 'findingType'
        }
        parsed_dict = {v: initial_dict[k]
                       for (k, v) in description_fields.items()
                       if k in initial_dict.keys()}
        parsed_dict = forms.dict_concatenation(parsed_dict, migrated_dict)
        parsed_dict['clientFindingType'] = forms.get_finding_type(parsed_dict)
        if 'cwe' in parsed_dict.keys():
            parsed_dict['cwe'] = forms.get_cwe_url(parsed_dict['cwe'])
        else:
            # The finding does not have cwe attribute
            pass
        return parsed_dict

    def parse_description_mail(self, request_arr): # noqa: C901
        """Convert description of a finding into a formstack format para envio de mail."""
        self.data['timestamp'] = request_arr['timestamp']
        for finding in request_arr['data']:
            if finding['field'] == self.FINDING:
                self.data['finding'] = finding['value']
        return self.data

    def parse_description_vuln(self, request_arr): # noqa: C901
        """Convert description of a finding into a formstack format."""
        self.data['timestamp'] = request_arr['timestamp']
        for finding in request_arr['data']:
            if finding['field'] == self.CARDINALITY:
                self.data['openVulnerabilities'] = finding['value']
        return self.data

    def parse_cvssv2(self, request_arr, submission_id): # noqa: C901
        """Convert the score of a finding into a formstack format."""
        initial_dict = forms.create_dict(request_arr)
        severity_title = ['access_vector', 'access_complexity',
                          'authentication', 'exploitability',
                          'confidentiality_impact', 'integrity_impact',
                          'availability_impact', 'resolution_level',
                          'confidence_level', 'collateral_damage_potential',
                          'finding_distribution', 'confidentiality_requirement',
                          'integrity_requirement', 'availability_requirement']
        severity = integrates_dao.get_finding_attributes_dynamo(
            str(submission_id),
            severity_title)
        if severity:
            severity_fields = {k: util.snakecase_to_camelcase(k)
                               for k in severity_title}
            parsed_dict = {v: float(severity[k])
                           for (k, v) in severity_fields.items()
                           if k in severity.keys()}
        else:
            severity_fields = {
                self.ACCESS_VECTOR: 'accessVector',
                self.ACCESS_COMPLEXITY: 'accessComplexity',
                self.AUTHENTICATION: 'authentication',
                self.CONFIDENTIALITY_IMPACT: 'confidentialityImpact',
                self.INTEGRITY_IMPACT: 'integrityImpact',
                self.AVAILABILITY_IMPACT: 'availabilityImpact',
                self.EXPLOITABILITY: 'exploitability',
                self.RESOLUTION_LEVEL: 'resolutionLevel',
                self.CONFIDENCE_LEVEL: 'confidenceLevel',
                self.COLLATERAL_DAMAGE_POTENTIAL: 'collateralDamagePotential',
                self.FINDING_DISTRIBUTION: 'findingDistribution',
                self.CONFIDENTIALITY_REQUIREMENT: 'confidentialityRequirement',
                self.INTEGRITY_REQUIREMENT: 'integrityRequirement',
                self.AVAILABILITY_REQUIREMENT: 'availabilityRequirement',
            }
            parsed_dict = {v: float(initial_dict[k].split(' | ')[0])
                           for (k, v) in severity_fields.items()
                           if k in initial_dict.keys()}
        BASE_SCORE_FACTOR_1 = 0.6
        BASE_SCORE_FACTOR_2 = 0.4
        BASE_SCORE_FACTOR_3 = 1.5
        IMPACT_FACTOR = 10.41
        EXPLOITABILITY_FACTOR = 20
        F_IMPACT_FACTOR = 1.176
        impact = (IMPACT_FACTOR *
                  (1 - ((1 - parsed_dict['confidentialityImpact']) *
                   (1 - parsed_dict['integrityImpact']) *
                   (1 - parsed_dict['availabilityImpact']))))
        exploitability = (EXPLOITABILITY_FACTOR *
                          parsed_dict['accessComplexity'] *
                          parsed_dict['authentication'] * parsed_dict['accessVector'])
        base_score = (((BASE_SCORE_FACTOR_1 * impact) +
                      (BASE_SCORE_FACTOR_2 * exploitability) - BASE_SCORE_FACTOR_3) *
                      F_IMPACT_FACTOR)
        parsed_dict['criticity'] = round((base_score * parsed_dict['exploitability'] *
                                         parsed_dict['resolutionLevel'] *
                                         parsed_dict['confidenceLevel']), 1)
        parsed_dict['impact'] = forms.get_impact(parsed_dict['criticity'])
        parsed_dict['exploitable'] = forms.is_exploitable(parsed_dict['exploitability'])
        return parsed_dict

    def parse_project(self, request_arr, submission_id):
        "Convert project info in formstack format"
        project_title = ['analyst', 'leader', 'interested', 'project_name',
                         'client_project', 'context']
        project_info = integrates_dao.get_finding_attributes_dynamo(
            str(submission_id),
            project_title)
        if project_info and project_info.get('analyst'):
            project_fields = {k: util.snakecase_to_camelcase(k)
                              for k in project_title}
            parsed_dict = {v: project_info[k]
                           for (k, v) in project_fields.items()
                           if k in project_info.keys()}
        else:
            initial_dict = forms.create_dict(request_arr)
            project_fields = {
                self.ANALIST: 'analyst',
                self.LEADER: 'leader',
                self.INTERESADO: 'interested',
                self.PROJECT_NAME: 'projectName',
                self.CLIENT_PROJECT: 'clientProject',
                self.CONTEXT: 'context'
            }
            parsed_dict = {v: initial_dict[k]
                           for (k, v) in project_fields.items()
                           if k in initial_dict.keys()}
        return parsed_dict

    def parse_evidence_info(self, request_arr, submission_id): # noqa: C901
        """Convert the score of a finding into a formstack format."""
        initial_dict = forms.create_dict(request_arr)
        evidence_title = ['records_number', 'records']
        evidence_info = integrates_dao.get_finding_attributes_dynamo(
            str(submission_id),
            evidence_title)
        if evidence_info:
            evidence_fields = {k: util.snakecase_to_camelcase(k)
                               for k in evidence_title}
            migrated_dict = {v: evidence_info[k]
                             for (k, v) in evidence_fields.items()
                             if k in evidence_info.keys()}
        else:
            evidence_fields = {
                self.REG: 'records',
                self.REG_NUM: 'recordsNumber'
            }
            migrated_dict = {v: initial_dict[k]
                             for (k, v) in evidence_fields.items()
                             if k in initial_dict.keys()}
        evidence_tab_fields = {
            self.DOC_TOTAL: 'evidenceTotal',
            self.DOC_CMNT1: 'evidence_description_1',
            self.DOC_CMNT2: 'evidence_description_2',
            self.DOC_CMNT3: 'evidence_description_3',
            self.DOC_CMNT4: 'evidence_description_4',
            self.DOC_CMNT5: 'evidence_description_5',
        }
        evidence_fields_with_urls = {
            self.DOC_ACHV1: 'evidence_route_1',
            self.DOC_ACHV2: 'evidence_route_2',
            self.DOC_ACHV3: 'evidence_route_3',
            self.DOC_ACHV4: 'evidence_route_4',
            self.DOC_ACHV5: 'evidence_route_5',
            self.ANIMATION: 'animation',
            self.EXPLOTATION: 'exploitation',
            self.EXPLOIT: 'exploit',
            self.REG_FILE: 'fileRecords',
            self.VULNERABILITIES_FILE: 'vulnerabilities'
        }
        evidence_tab_info = {v: initial_dict[k]
                             for (k, v) in evidence_tab_fields.items()
                             if k in initial_dict.keys()}
        evidence_tab_info = forms.dict_concatenation(evidence_tab_info, migrated_dict)
        evidence_urls_info = {v: forms.drive_url_filter(initial_dict[k])
                              for (k, v) in evidence_fields_with_urls.items()
                              if k in initial_dict.keys()}
        return forms.dict_concatenation(evidence_tab_info, evidence_urls_info)

    def mask_finding(self, findingid, mask_value):
        """Mask finding."""
        self.request_id = findingid
        self.data[self.CLIENT_CODE] = mask_value
        self.data[self.CLIENT_PROJECT] = mask_value
        self.data[self.RELATED_FINDINGS] = mask_value
        self.data[self.REG_FILE] = base64.b64encode(mask_value)
        self.data[self.VULNERABILITY] = mask_value
        self.data[self.WHERE] = mask_value
        self.data[self.ATTACK_VECTOR] = mask_value
        self.data[self.AFFECTED_SYSTEMS] = mask_value
        self.data[self.THREAT] = mask_value
        self.data[self.RISK] = mask_value
        self.data[self.EFFECT_SOLUTION] = mask_value
        self.data[self.DOC_ACHV1] = base64.b64encode(mask_value)
        self.data[self.DOC_CMNT1] = mask_value
        self.data[self.DOC_ACHV2] = base64.b64encode(mask_value)
        self.data[self.DOC_CMNT2] = mask_value
        self.data[self.DOC_ACHV3] = base64.b64encode(mask_value)
        self.data[self.DOC_CMNT3] = mask_value
        self.data[self.DOC_ACHV4] = base64.b64encode(mask_value)
        self.data[self.DOC_CMNT4] = mask_value
        self.data[self.DOC_ACHV5] = base64.b64encode(mask_value)
        self.data[self.DOC_CMNT5] = mask_value
        self.data[self.EXPLOTATION] = base64.b64encode(mask_value)
        self.data[self.ANIMATION] = base64.b64encode(mask_value)
        self.data[self.EXPLOIT] = base64.b64encode(mask_value)
        self.data[self.TREATMENT] = mask_value
        self.data[self.TREATMENT_MANAGER] = mask_value
        self.data[self.TREATMENT_JUSTIFICATION] = mask_value

    def to_formstack(self):
        new_data = dict()
        for key, value in self.data.items():
            new_data['field_' + key] = value
        self.data = new_data

def format_finding_date(format_attr):
    tzn = pytz.timezone('America/Bogota')
    finding_date = datetime.strptime(
        format_attr.split(' ')[0],
        '%Y-%m-%d'
    )
    finding_date = finding_date.replace(tzinfo=tzn).date()
    final_date = (datetime.now(tz=tzn).date() - finding_date)
    return final_date

def finding_vulnerabilities(submission_id):
    finding = []
    state = {'estado': 'Abierto'}
    fin_dto = FindingDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        finding = fin_dto.parse(
            submission_id,
            api.get_submission(submission_id)
        )
        closingreqset = api.get_closings_by_id(submission_id)['submissions']
        findingcloseset = []
        for closingreq in closingreqset:
            closingset = closing.parse(api.get_submission(closingreq['id']))
            findingcloseset.append(closingset)
            state = closingset
        finding['estado'] = state['estado']
        finding['cierres'] = findingcloseset
        finding_new = total_vulnerabilities(submission_id)
        finding['cardinalidad_total'] = finding.get('openVulnerabilities')
        if (finding_new and
                (finding_new.get('openVulnerabilities') or
                    finding_new.get('closedVulnerabilities'))):
            total_cardinality = finding_new.get('openVulnerabilities') + \
                finding_new.get('closedVulnerabilities')
            finding['cardinalidad_total'] = str(total_cardinality)
            if (finding_new.get('closedVulnerabilities') > 0 and
                    finding_new.get('openVulnerabilities') == 0):
                finding['estado'] = 'Cerrado'
            else:
                finding['estado'] = 'Abierto'
            if finding_new.get('openVulnerabilities') >= 0:
                finding['openVulnerabilities'] = \
                    str(finding_new.get('openVulnerabilities'))
            else:
                # This finding does not have open vulnerabilities
                pass
        elif 'opened' in state:
            # Hack: This conditional temporarily solves the problem presented
            #      when the number of vulnerabilities open in a closing cycle
            # are higher than the number of vulnerabilities open in a finding
            # which causes negative numbers to be shown in the indicators view.
            if int(state['opened']) > int(finding['cardinalidad_total']):
                finding['cardinalidad_total'] = state['opened']
            if 'whichOpened' in state:
                finding['where'] = state['whichOpened']
            else:
                # This finding does not have old open vulnerabilities
                # after a closing cicle.
                pass
            finding['openVulnerabilities'] = state['opened']
        if finding.get('estado') == 'Cerrado':
            finding['where'] = '-'
            finding['edad'] = '-'
            finding['lastVulnerability'] = '-'
        if 'whichClosed' in state:
            finding['closed'] = state['whichClosed']
        finding = format_release(finding)
        return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error')
        return None


def format_release(finding):
    """Format formstack information to show release date."""
    primary_keys = ['finding_id', finding['id']]
    finding_dynamo = integrates_dao.get_data_dynamo(
        'FI_findings', primary_keys[0], primary_keys[1])
    if finding_dynamo:
        finding_data = finding_dynamo[0]
        if finding_data.get('releaseDate'):
            finding['releaseDate'] = finding_data.get('releaseDate')
        if finding_data.get('lastVulnerability'):
            finding['lastVulnerability'] = finding_data.get('lastVulnerability')
    if finding.get('releaseDate'):
        tzn = pytz.timezone('America/Bogota')
        today_day = datetime.now(tz=tzn).date()
        finding_last_vuln = datetime.strptime(
            finding['releaseDate'].split(' ')[0],
            '%Y-%m-%d'
        )
        finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
        if finding_last_vuln <= today_day:
            final_date = format_finding_date(finding['releaseDate'])
            finding['edad'] = ':n'.replace(':n', str(final_date.days))
    return finding

def ungroup_specific(specific):
    """Ungroup specific value."""
    values = specific.split(',')
    specific_values = []
    for val in values:
        if is_range(val):
            range_list = range_to_list(val)
            specific_values.extend(range_list)
        else:
            specific_values.append(val)
    return specific_values


def is_range(specific):
    """Validate if a specific field has range value."""
    return '-' in specific


def is_secuence(specific):
    """Validate if a specific field has secuence value."""
    return ',' in specific


def range_to_list(range_value):
    """Convert a range value into list."""
    limits = range_value.split('-')
    if int(limits[1]) > int(limits[0]):
        init_val = int(limits[0])
        end_val = int(limits[1]) + 1
    else:
        raise InvalidRange()
    specific_values = map(str, range(init_val, end_val))
    return specific_values


def update_vuln_state(vulnerability, item, finding_id, current_day):
    """Update vulnerability state."""
    historic_state = vulnerability[0].get('historic_state')
    last_state = historic_state[len(historic_state) - 1]
    response = False
    if last_state.get('state') != item.get('state'):
        historic_state = []
        current_state = {'date': current_day, 'state': item.get('state')}
        historic_state.append(current_state)
        response = integrates_dao.update_state_dynamo(
            finding_id,
            vulnerability[0].get('UUID'),
            'historic_state',
            historic_state,
            vulnerability)
    else:
        response = True
    return response


def add_vuln_to_dynamo(item, specific, vuln, finding_id, info):
    """Add vulnerability to dynamo."""
    historic_state = []
    where = item.get('where')
    vulnerability = integrates_dao.get_vulnerability_dynamo(
        finding_id, vuln_type=vuln, where=where, specific=specific)
    response = False
    tzn = pytz.timezone('America/Bogota')
    current_day = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    user_data = util.get_jwt_content(info.context)
    email = user_data['user_email']
    if vulnerability:
        response = update_vuln_state(vulnerability, item, finding_id, current_day)
    else:
        data = {}
        data['vuln_type'] = vuln
        data['where'] = where
        data['specific'] = specific
        data['finding_id'] = finding_id
        data['UUID'] = str(uuid.uuid4())
        data['analyst'] = email
        if item.get('state'):
            historic_state.append({'date': current_day, 'state': item.get('state')})
            data['historic_state'] = historic_state
            response = integrates_dao.add_vulnerability_dynamo('FI_vulnerabilities', data)
        else:
            util.cloudwatch_log(
                info.context,
                'Security: Attempted to add vulnerability without state')
    return response


def sort_vulnerabilities(item):
    """Sort a vulnerability by its where field."""
    sorted_item = sorted(item, key=itemgetter('where'))
    return sorted_item


def group_specific(specific):
    """Group vulnerabilities by its specific field."""
    sorted_specific = sort_vulnerabilities(specific)
    lines = []
    for key, group in itertools.groupby(sorted_specific, key=lambda x: x['where']):
        specific_grouped = list(map(get_specific, list(group)))
        specific_grouped.sort()
        dictlines = {'where': key, 'specific': get_ranges(specific_grouped)}
        lines.append(dictlines)
    return lines


def get_specific(value):
    """Get specific value."""
    return int(value.get('specific'))


def as_range(iterable):
    """Convert range into string."""
    l = list(iterable)
    range_value = ''
    if len(l) > 1:
        range_value = '{0}-{1}'.format(l[0], l[-1])
    else:
        range_value = '{0}'.format(l[0])
    return range_value


def get_ranges(numberlist):
    """Transform list into ranges."""
    range_str = ','.join(as_range(g) for _, g in itertools.groupby(
        numberlist,
        key=lambda n,
        c=itertools.count(): n-next(c))
    )
    return range_str


def total_vulnerabilities(finding_id):
    """Get total vulnerabilities in new format."""
    vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    for vuln in vulnerabilities:
        all_states = vuln.get('historic_state')
        current_state = all_states[len(all_states) - 1].get('state')
        if current_state == 'open':
            finding['openVulnerabilities'] += 1
        elif current_state == 'closed':
            finding['closedVulnerabilities'] += 1
        else:
            util.cloudwatch_log_plain(
                'Error: Vulnerability of finding {finding_id} does not have the right state'.format(finding_id=finding_id)
            )
    return finding


def update_vulnerabilities_date(finding_id):
    """Update vulnerabilities date when a verification is required."""
    vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
    for vuln in vulnerabilities:
        all_states = vuln.get('historic_state')
        current_state = all_states[len(all_states) - 1]
        tzn = pytz.timezone('America/Bogota')
        last_date = datetime.strptime(
            current_state.get('date').split(" ")[0],
            '%Y-%m-%d'
        )
        last_date = last_date.replace(tzinfo=tzn).date()
        current_date = datetime.now(tz=tzn).date()
        if last_date != current_date:
            historic_state = []
            current_time = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
            last_state = {'date': current_time, 'state': current_state.get('state')}
            historic_state.append(last_state)
            integrates_dao.update_state_dynamo(
                finding_id,
                vuln.get('UUID'),
                'historic_state',
                historic_state,
                [vuln])
        else:
            # A finding that change the same day should not be updated
            pass


def save_severity(finding):
    """Organize severity metrics to save in dynamo."""
    primary_keys = ['finding_id', str(finding['id'])]
    severity_fields = ['accessVector', 'accessComplexity',
                       'authentication', 'exploitability',
                       'confidentialityImpact', 'integrityImpact',
                       'availabilityImpact', 'resolutionLevel',
                       'confidenceLevel', 'collateralDamagePotential',
                       'findingDistribution', 'confidentialityRequirement',
                       'integrityRequirement', 'availabilityRequirement']
    severity = {util.camelcase_to_snakecase(k): Decimal(str(finding.get(k)))
                for k in severity_fields}
    response = integrates_dao.add_multiple_attributes_dynamo(primary_keys, severity)
    return response


def migrate_description(finding):
    primary_keys = ['finding_id', str(finding['id'])]
    description_fields = ['analyst', 'leader', 'interested', 'projectName',
                          'clientProject', 'context', 'reportLevel',
                          'subscription', 'clientCode', 'finding',
                          'probability', 'severity', 'riskValue', 'ambit',
                          'category', 'testType', 'relatedFindings', 'actor',
                          'scenario', 'recordsNumber', 'records']
    description = {util.camelcase_to_snakecase(k): finding.get(k)
                   for k in description_fields if finding.get(k)}
    response = integrates_dao.add_multiple_attributes_dynamo(primary_keys, description)
    return response
