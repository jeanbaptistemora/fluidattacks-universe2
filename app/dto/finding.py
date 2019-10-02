# coding=utf-8
""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
from datetime import datetime
import base64

from django.conf import settings
import pytz
import rollbar

from ..dal import integrates_dal
from ..dal.helpers.formstack import FormstackAPI
from ..domain import vulnerability as vuln_domain
from ..utils import forms
from ..utils import cvss
from .. import util


# pylint: disable=E0402

class FindingDTO(object):
    """Class to create an object with the attributes of a finding."""

    FIELDS_FINDING = settings.FIELDS_FINDING
    # Atributos proyecto
    ANALIST = FIELDS_FINDING['ANALIST']
    LEADER = FIELDS_FINDING['LEADER']
    INTERESADO = FIELDS_FINDING['INTERESADO']
    PROJECT_NAME = FIELDS_FINDING['PROJECT_NAME']
    CLIENT_PROJECT = FIELDS_FINDING['CLIENT_PROJECT']
    CONTEXT = FIELDS_FINDING['CONTEXT']

    # Atributos evidencia
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

    # Atributos descriptivos
    REPORT_LEVEL = FIELDS_FINDING['REPORT_LEVEL']  # detallado
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
    ATTACK_VECTOR_DESC = FIELDS_FINDING['ATTACK_VECTOR_DESC']
    CWE = FIELDS_FINDING['CWE']
    TREATMENT = FIELDS_FINDING['TREATMENT']
    TREATMENT_JUSTIFICATION = FIELDS_FINDING['TREATMENT_JUSTIFICATION']
    TREATMENT_MANAGER = FIELDS_FINDING['TREATMENT_MANAGER']
    EXTERNAL_BTS = FIELDS_FINDING['EXTERNAL_BTS']
    LAST_VULNERABILITY = FIELDS_FINDING['LAST_VULNERABILITY']
    RELEASE_DATE = FIELDS_FINDING['RELEASE_DATE']
    RELATED_FINDINGS = FIELDS_FINDING['RELATED_FINDINGS']

    # Atributos CssV2
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
    CVSS_PARAMETERS = {'bs_factor_1': 0.6, 'bs_factor_2': 0.4, 'bs_factor_3': 1.5,
                       'impact_factor': 10.41, 'exploitability_factor': 20}

    # Attributes CVSS V3
    CVSS_VERSION = FIELDS_FINDING['CVSS_VERSION']
    ATTACK_VECTOR_V3 = FIELDS_FINDING['ATTACK_VECTOR_V3']
    ATTACK_COMPLEXITY = FIELDS_FINDING['ATTACK_COMPLEXITY']
    PRIVILEGES_REQUIRED = FIELDS_FINDING['PRIVILEGES_REQUIRED']
    USER_INTERACTION = FIELDS_FINDING['USER_INTERACTION']
    SEVERITY_SCOPE = FIELDS_FINDING['SEVERITY_SCOPE']
    CONFIDENTIALITY_IMPACT_V3 = FIELDS_FINDING['CONFIDENTIALITY_IMPACT_V3']
    INTEGRITY_IMPACT_V3 = FIELDS_FINDING['INTEGRITY_IMPACT_V3']
    AVAILABILITY_IMPACT_V3 = FIELDS_FINDING['AVAILABILITY_IMPACT_V3']
    EXPLOITABILITY_V3 = FIELDS_FINDING['EXPLOITABILITY_V3']
    REMEDIATION_LEVEL = FIELDS_FINDING['REMEDIATION_LEVEL']
    REPORT_CONFIDENCE = FIELDS_FINDING['REPORT_CONFIDENCE']
    CONFIDENTIALITY_REQUIREMENT_V3 = FIELDS_FINDING['CONFIDENTIALITY_REQUIREMENT_V3']
    INTEGRITY_REQUIREMENT_V3 = FIELDS_FINDING['INTEGRITY_REQUIREMENT_V3']
    AVAILABILITY_REQUIREMENT_V3 = FIELDS_FINDING['AVAILABILITY_REQUIREMENT_V3']
    MODIFIED_ATTACK_VECTOR = FIELDS_FINDING['MODIFIED_ATTACK_VECTOR']
    MODIFIED_ATTACK_COMPLEXITY = FIELDS_FINDING['MODIFIED_ATTACK_COMPLEXITY']
    MODIFIED_PRIVILEGES_REQUIRED = FIELDS_FINDING['MODIFIED_PRIVILEGES_REQUIRED']
    MODIFIED_USER_INTERACTION = FIELDS_FINDING['MODIFIED_USER_INTERACTION']
    MODIFIED_SEVERITY_SCOPE = FIELDS_FINDING['MODIFIED_SEVERITY_SCOPE']
    MODIFIED_CONFIDENTIALITY_IMPACT = FIELDS_FINDING['MODIFIED_CONFIDENTIALITY_IMPACT']
    MODIFIED_INTEGRITY_IMPACT = FIELDS_FINDING['MODIFIED_INTEGRITY_IMPACT']
    MODIFIED_AVAILABILITY_IMPACT = FIELDS_FINDING['MODIFIED_AVAILABILITY_IMPACT']
    CVSS3_PARAMETERS = {'impact_factor_1': 6.42, 'impact_factor_2': 7.52,
                        'impact_factor_3': 0.029, 'impact_factor_4': 3.25,
                        'impact_factor_5': 0.02, 'impact_factor_6': 15,
                        'exploitability_factor_1': 8.22, 'basescore_factor': 1.08,
                        'mod_impact_factor_1': 0.915, 'mod_impact_factor_2': 6.42,
                        'mod_impact_factor_3': 7.52, 'mod_impact_factor_4': 0.029,
                        'mod_impact_factor_5': 3.25, 'mod_impact_factor_6': 0.02,
                        'mod_impact_factor_7': 15}

    def __init__(self):
        """Class constructor."""
        self.request_id = None
        self.data = dict()

    def create_description(self, parameter):  # noqa: C901
        """Convert the index of a JSON to Formstack index."""
        if 'data[id]' in parameter:
            self.request_id \
                = parameter['data[id]']
        if 'data[openVulnerabilities]' in parameter:
            self.data[self.CARDINALITY] \
                = parameter['data[openVulnerabilities]']
        if 'data[where]' in parameter:
            self.data[self.WHERE] \
                = parameter['data[where]']
        if 'data[lastVulnerability]' in parameter:
            self.data[self.LAST_VULNERABILITY] \
                = parameter['data[lastVulnerability]']
        if 'data[releaseDate]' in parameter:
            self.data[self.RELEASE_DATE] \
                = parameter['data[releaseDate]']

    def parse(self, submission_id, request_arr):
        self.data = dict()
        self.data['id'] = submission_id
        report_title = ['report_date']
        report_date = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            report_title)
        if report_date:
            self.data['reportDate'] = report_date.get('report_date')
        else:
            self.data['reportDate'] = request_arr['timestamp']
        self.data = \
            forms.dict_concatenation(self.data,
                                     self.parse_description(request_arr,
                                                            submission_id))
        if self.data.get('cvssVersion', '') == '3':
            self.data = \
                forms.dict_concatenation(self.data,
                                         self.parse_cvssv3(request_arr,
                                                           submission_id))
        else:
            self.data = \
                forms.dict_concatenation(self.data,
                                         self.parse_cvssv2(request_arr,
                                                           submission_id))
        self.data = \
            forms.dict_concatenation(self.data,
                                     self.parse_project(request_arr,
                                                        submission_id))
        self.data = \
            forms.dict_concatenation(self.data,
                                     self.parse_evidence_info(request_arr,
                                                              submission_id))
        return self.data

    def parse_description(self, request_arr, submission_id): # noqa: C901
        """Convert description of a finding into a formstack format."""
        initial_dict = forms.create_dict(request_arr)
        migrated_dict = {}
        migrated_aditional_info_dict = {}
        description_title = ['report_level', 'subscription', 'client_code',
                             'finding', 'probability', 'severity',
                             'risk_value', 'ambit', 'category', 'test_type',
                             'related_findings', 'actor', 'scenario']
        description = integrates_dal.get_finding_attributes_dynamo(
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
                self.ACTOR: 'actor'
            }
            migrated_dict = {v: initial_dict[k]
                             for (k, v) in migrated_description_fields.items()
                             if k in initial_dict.keys()}
            if migrated_dict.get('probability'):
                migrated_dict['probability'] = int(migrated_dict['probability']
                                                   .split(' ')[0].replace('%', ''))
            else:
                # Finding doesn't have probability attribute because is general
                pass
        aditional_info_title = ['vulnerability', 'attack_vector_desc',
                                'affected_systems', 'threat', 'risk',
                                'requirements', 'cwe', 'effect_solution',
                                'kb', 'finding_type']
        aditional_info = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            aditional_info_title)
        if aditional_info:
            migrated_aditional_info_fields = {k: util.snakecase_to_camelcase(k)
                                              for k in aditional_info_title}
            migrated_aditional_info_dict = {
                v: aditional_info[k]
                for (k, v) in migrated_aditional_info_fields.items()
                if k in aditional_info.keys()}
        else:
            migrated_aditional_info_fields = {
                self.VULNERABILITY: 'vulnerability',
                self.ATTACK_VECTOR_DESC: 'attackVectorDesc',
                self.AFFECTED_SYSTEMS: 'affectedSystems',
                self.THREAT: 'threat',
                self.RISK: 'risk',
                self.REQUIREMENTS: 'requirements',
                self.CWE: 'cwe',
                self.EFFECT_SOLUTION: 'effectSolution',
                self.KB_LINK: 'kb',
                self.FINDING_TYPE: 'findingType'
            }
            migrated_aditional_info_dict = {
                v: initial_dict[k]
                for (k, v) in migrated_aditional_info_fields.items()
                if k in initial_dict.keys()}
        migrated_data = forms.dict_concatenation(
            migrated_dict,
            migrated_aditional_info_dict)
        treatment_title = ['treatment', 'treatment_justification',
                           'treatment_manager', 'external_bts']
        treatment_info = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            treatment_title)
        if treatment_info:
            treatment_fields = {k: util.snakecase_to_camelcase(k)
                                for k in treatment_title}
            treatment_dict = {
                v: treatment_info[k]
                for (k, v) in treatment_fields.items()
                if k in treatment_info.keys()}
        else:
            treatment_fields = {
                self.TREATMENT: 'treatment',
                self.TREATMENT_JUSTIFICATION: 'treatmentJustification',
                self.TREATMENT_MANAGER: 'treatmentManager',
                self.EXTERNAL_BTS: 'externalBts'
            }
            treatment_dict = {
                v: initial_dict[k]
                for (k, v) in treatment_fields.items()
                if k in initial_dict.keys()}
        migrated_data = forms.dict_concatenation(
            migrated_data,
            treatment_dict)
        cvss_version_info = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            ['cvss_version'])
        if cvss_version_info:
            cvss_version_fields = {k: util.snakecase_to_camelcase(k)
                                   for k in ['cvss_version']}
            cvss_version_dict = {
                v: cvss_version_info[k]
                for (k, v) in cvss_version_fields.items()
                if k in cvss_version_info.keys()}
        else:
            cvss_version_fields = {
                self.CVSS_VERSION: 'cvssVersion'
            }
            cvss_version_dict = {
                v: initial_dict[k]
                for (k, v) in cvss_version_fields.items()
                if k in initial_dict.keys()}
        migrated_data = forms.dict_concatenation(
            migrated_data,
            cvss_version_dict)
        description_fields = {
            self.CARDINALITY: 'openVulnerabilities',
            self.WHERE: 'where',
            self.LAST_VULNERABILITY: 'lastVulnerability',
            self.RELEASE_DATE: 'releaseDate',
        }
        parsed_dict = {v: initial_dict[k]
                       for (k, v) in description_fields.items()
                       if k in initial_dict.keys()}
        parsed_dict = forms.dict_concatenation(parsed_dict, migrated_data)
        parsed_dict = forms.cast_finding_attributes(parsed_dict)
        if migrated_dict.get('type') == 'DETAILED':
            migrated_dict['probability'] = \
                int(migrated_dict.get('probability', '0'))
        else:
            # Finding doesn't have probability attribute because is general
            pass
        return parsed_dict

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
        severity = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            severity_title)
        if severity and len(severity.keys()) > 1:
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
        cvss_version = '2'
        base_score = float(cvss.calculate_cvss_basescore(
            parsed_dict, self.CVSS_PARAMETERS, cvss_version))
        parsed_dict['baseScore'] = base_score
        parsed_dict['severityCvss'] = cvss.calculate_cvss_temporal(
            parsed_dict, base_score, cvss_version)
        parsed_dict['impact'] = forms.get_impact(
            parsed_dict['severityCvss'], cvss_version)
        parsed_dict['exploitable'] = forms.is_exploitable(
            parsed_dict['exploitability'], cvss_version)
        return parsed_dict

    def parse_cvssv3(self, request_arr, submission_id): # noqa: C901
        """Convert the score of a finding into a formstack format."""
        initial_dict = forms.create_dict(request_arr)
        severity_title = ['attack_vector', 'attack_complexity',
                          'privileges_required', 'user_interaction',
                          'severity_scope', 'confidentiality_impact',
                          'integrity_impact', 'availability_impact',
                          'exploitability', 'remediation_level',
                          'report_confidence', 'confidentiality_requirement',
                          'integrity_requirement', 'availability_requirement',
                          'modified_attack_vector', 'modified_attack_complexity',
                          'modified_privileges_required', 'modified_user_interaction',
                          'modified_severity_scope', 'modified_confidentiality_impact',
                          'modified_integrity_impact', 'modified_availability_impact']
        severity = integrates_dal.get_finding_attributes_dynamo(
            str(submission_id),
            severity_title)
        if severity and len(severity.keys()) > 1:
            severity_fields = {k: util.snakecase_to_camelcase(k)
                               for k in severity_title}
            parsed_dict = {v: float(severity[k])
                           for (k, v) in severity_fields.items()
                           if k in severity.keys()}
        else:
            severity_fields = {
                self.ATTACK_VECTOR_V3: 'attackVector',
                self.ATTACK_COMPLEXITY: 'attackComplexity',
                self.PRIVILEGES_REQUIRED: 'privilegesRequired',
                self.USER_INTERACTION: 'userInteraction',
                self.SEVERITY_SCOPE: 'severityScope',
                self.CONFIDENTIALITY_IMPACT_V3: 'confidentialityImpact',
                self.INTEGRITY_IMPACT_V3: 'integrityImpact',
                self.AVAILABILITY_IMPACT_V3: 'availabilityImpact',
                self.EXPLOITABILITY_V3: 'exploitability',
                self.REMEDIATION_LEVEL: 'remediationLevel',
                self.REPORT_CONFIDENCE: 'reportConfidence',
                self.CONFIDENTIALITY_REQUIREMENT_V3: 'confidentialityRequirement',
                self.INTEGRITY_REQUIREMENT_V3: 'integrityRequirement',
                self.AVAILABILITY_REQUIREMENT_V3: 'availabilityRequirement',
                self.MODIFIED_ATTACK_VECTOR: 'modifiedAttackVector',
                self.MODIFIED_ATTACK_COMPLEXITY: 'modifiedAttackComplexity',
                self.MODIFIED_PRIVILEGES_REQUIRED: 'modifiedPrivilegesRequired',
                self.MODIFIED_USER_INTERACTION: 'modifiedUserInteraction',
                self.MODIFIED_SEVERITY_SCOPE: 'modifiedSeverityScope',
                self.MODIFIED_CONFIDENTIALITY_IMPACT: 'modifiedConfidentialityImpact',
                self.MODIFIED_INTEGRITY_IMPACT: 'modifiedIntegrityImpact',
                self.MODIFIED_AVAILABILITY_IMPACT: 'modifiedAvailabilityImpact'
            }
            parsed_dict = {v: float(initial_dict[k])
                           for (k, v) in severity_fields.items()
                           if k in initial_dict.keys()}
        cvss_version = '3'
        if parsed_dict.get('severityScope'):
            if parsed_dict['privilegesRequired'] == 0.62:
                parsed_dict['privilegesRequired'] = 0.68
            elif parsed_dict['privilegesRequired'] == 0.27:
                parsed_dict['privilegesRequired'] = 0.5
        else:
            # privileges required continue with its initial value
            pass
        if parsed_dict.get('modifiedSeverityScope'):
            if parsed_dict['modifiedPrivilegesRequired'] == 0.62:
                parsed_dict['modifiedPrivilegesRequired'] = 0.68
            elif parsed_dict['modifiedPrivilegesRequired'] == 0.27:
                parsed_dict['modifiedPrivilegesRequired'] = 0.5
        else:
            # Modified privileges required continue with its initial value
            pass
        base_score = float(cvss.calculate_cvss_basescore(
            parsed_dict, self.CVSS3_PARAMETERS, cvss_version))
        parsed_dict['baseScore'] = base_score
        parsed_dict['severityCvss'] = cvss.calculate_cvss_temporal(
            parsed_dict, base_score, cvss_version)
        parsed_dict['impact'] = forms.get_impact(
            parsed_dict['severityCvss'], cvss_version)
        parsed_dict['exploitable'] = forms.is_exploitable(
            parsed_dict['exploitability'], cvss_version)
        return parsed_dict

    def parse_project(self, request_arr, submission_id):
        "Convert project info in formstack format"
        project_title = ['analyst', 'leader', 'interested', 'project_name',
                         'client_project', 'context']
        project_info = integrates_dal.get_finding_attributes_dynamo(
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
        evidence_info = integrates_dal.get_finding_attributes_dynamo(
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
        files_field = ['files']
        description_fields = {
            'evidence_route_1': 'evidence_description_1',
            'evidence_route_2': 'evidence_description_2',
            'evidence_route_3': 'evidence_description_3',
            'evidence_route_4': 'evidence_description_4',
            'evidence_route_5': 'evidence_description_5'
        }
        if has_migrated_evidence(submission_id):
            files_info = integrates_dal.get_finding_attributes_dynamo(
                str(submission_id),
                files_field)
            evidence_tab_info = {description_fields[file_obj['name']]: file_obj.get('description')
                                 for file_obj in files_info.get('files')
                                 if file_obj.get('name') in description_fields and
                                 file_obj.get('description')}
        else:
            evidence_tab_fields = {
                self.DOC_CMNT1: 'evidence_description_1',
                self.DOC_CMNT2: 'evidence_description_2',
                self.DOC_CMNT3: 'evidence_description_3',
                self.DOC_CMNT4: 'evidence_description_4',
                self.DOC_CMNT5: 'evidence_description_5',
            }
            evidence_tab_info = {v: initial_dict[k]
                                 for (k, v) in evidence_tab_fields.items()
                                 if k in initial_dict.keys()}
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
        self.data[self.ATTACK_VECTOR_DESC] = mask_value
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


def mask_finding_fields_dynamo(finding_id, fields, mask_value):
    primary_keys = ['finding_id', str(finding_id)]
    description = {k: mask_value for k in fields}
    is_description_masked = integrates_dal.\
        add_multiple_attributes_dynamo('FI_findings', primary_keys, description)
    vulns = integrates_dal.get_vulnerabilities_dynamo(finding_id)
    vuln_fields = ['specific', 'where']
    are_vulns_masked = list(map(lambda x:
                                mask_vulns_fields_dynamo(x, vuln_fields,
                                                         'Masked'), vulns))
    are_evidences_masked = mask_evidence_dynamo(finding_id)
    is_finding_masked = [is_description_masked, all(are_vulns_masked), are_evidences_masked]
    return is_finding_masked


def mask_vulns_fields_dynamo(vulnerability, fields, mask_value):
    are_masked = []
    keys = {'finding_id': str(vulnerability.get('finding_id')),
            'UUID': str(vulnerability.get('UUID'))}
    for field in fields:
        is_masked = integrates_dal.\
            update_in_multikey_table_dynamo('FI_vulnerabilities', keys, field,
                                            mask_value)
        are_masked.append(is_masked)
    response = all(are_masked)
    return response


def mask_evidence_dynamo(finding_id):
    attr_name = 'files'
    files = integrates_dal.get_finding_attributes_dynamo(finding_id, [attr_name])
    primary_keys = ['finding_id', finding_id]
    index = 0
    if files and files.get(attr_name):
        for file_obj in files.get(attr_name):
            are_evidences_masked = \
                list(map(lambda x: integrates_dal.
                         update_item_list_dynamo(primary_keys, attr_name, index,
                                                 x, 'Masked'),
                         file_obj.keys()))
            index += 1
        response = all(are_evidences_masked)
    else:
        response = False
    return response


def vulnerabilities_status(finding_new):
    if (finding_new.get('closedVulnerabilities') > 0 and
            finding_new.get('openVulnerabilities') == 0):
        status = 'Cerrado'
    else:
        status = 'Abierto'
    return status


def finding_vulnerabilities(submission_id):
    finding = []
    if str(submission_id).isdigit() is True:
        fin_dto = FindingDTO()
        api = FormstackAPI()
        finding = fin_dto.parse(
            submission_id,
            api.get_submission(submission_id)
        )
        finding_new = total_vulnerabilities(submission_id)
        finding['cardinalidad_total'] = finding.get('openVulnerabilities')
        if (finding_new and
                (finding_new.get('openVulnerabilities') or
                    finding_new.get('closedVulnerabilities'))):
            total_cardinality = finding_new.get('openVulnerabilities') + \
                finding_new.get('closedVulnerabilities')
            finding['cardinalidad_total'] = str(total_cardinality)
            finding['estado'] = vulnerabilities_status(finding_new)
            if finding_new.get('openVulnerabilities') >= 0:
                finding['openVulnerabilities'] = \
                    str(finding_new.get('openVulnerabilities'))
            else:
                # This finding does not have open vulnerabilities
                pass
        else:
            finding['estado'] = 'Abierto'
        if finding.get('estado') == 'Cerrado':
            finding['where'] = '-'
            finding['treatmentManager'] = '-'
            finding['treatmentJustification'] = '-'
            finding['treatment'] = '-'
        finding = format_release(finding)
        return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error')
        return None


def format_release(finding):
    """Format formstack information to show release date."""
    primary_keys = ['finding_id', finding['id']]
    finding_dynamo = integrates_dal.get_data_dynamo(
        'FI_findings', primary_keys[0], primary_keys[1])
    if finding_dynamo:
        finding_data = finding_dynamo[0]
        if finding_data.get('releaseDate'):
            finding['releaseDate'] = finding_data.get('releaseDate')
        if finding_data.get('lastVulnerability'):
            finding['lastVulnerability'] = finding_data.get('lastVulnerability')
    if finding.get('releaseDate'):
        tzn = pytz.timezone(settings.TIME_ZONE)
        today_day = datetime.now(tz=tzn).date()
        finding_last_vuln = datetime.strptime(
            finding['releaseDate'].split(' ')[0],
            '%Y-%m-%d'
        )
        finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
        if finding_last_vuln <= today_day:
            final_date = util.calculate_datediff_since(finding['releaseDate'])
            finding['edad'] = ':n'.replace(':n', str(final_date.days))
    return finding


def total_vulnerabilities(finding_id):
    """Get total vulnerabilities in new format."""
    vulnerabilities = integrates_dal.get_vulnerabilities_dynamo(finding_id)
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    for vuln in vulnerabilities:
        current_state = vuln_domain.get_last_approved_status(vuln)
        if current_state == 'open':
            finding['openVulnerabilities'] += 1
        elif current_state == 'closed':
            finding['closedVulnerabilities'] += 1
        else:
            # Vulnerability does not have a valid state
            pass
    return finding


def has_migrated_evidence(finding_id):
    """Validate if a finding has evidence description in dynamo."""
    attr_name = 'files'
    files = integrates_dal.get_finding_attributes_dynamo(finding_id, [attr_name])
    if files and files.get(attr_name):
        for file_obj in files.get(attr_name):
            if (file_obj.get('name') == 'evidence_route_1' and
                    file_obj.get('description')):
                response = True
                break
            else:
                response = False
    else:
        response = False
    return response


def parse_finding(finding):
    """Parse data from dynamo."""
    finding_titles = [
        'report_date', 'report_level', 'subscription', 'client_code',
        'finding', 'probability', 'severity', 'risk_value', 'ambit', 'risk',
        'category', 'test_type', 'related_findings', 'actor', 'scenario',
        'vulnerability', 'attack_vector_desc', 'affected_systems',
        'requirements', 'cwe', 'effect_solution', 'kb', 'finding_type',
        'treatment', 'treatment_justification', 'treatment_manager', 'threat',
        'external_bts', 'analyst', 'leader', 'interested', 'project_name',
        'client_project', 'context', 'records_number', 'records'
    ]
    if finding:
        finding_fields = {k: util.snakecase_to_camelcase(k)
                          for k in finding_titles}
        parsed_dict = {v: finding[k]
                       for (k, v) in finding_fields.items()
                       if k in finding.keys()}

        parsed_dict['id'] = finding.get('finding_id')
        parsed_dict['lastVulnerability'] = finding.get('lastVulnerability')
        parsed_dict['releaseDate'] = finding.get('releaseDate')
        parsed_severity = parse_severity(finding)
        parsed_evidence_description = parse_evidence_description(finding)
        parsed_values = forms.dict_concatenation(parsed_severity, parsed_evidence_description)
        parsed_dict = forms.dict_concatenation(parsed_dict, parsed_values)
        if parsed_dict.get('type') == 'DETAILED':
            parsed_dict['probability'] = int(parsed_dict.get('probability', '0'))
        else:
            # Finding doesn't have probability attribute because is general
            pass
    return parsed_dict


def parse_severity(finding):
    """Parse finding severity."""
    fin_dto = FindingDTO()
    cvss_version = finding.get('cvss_version')
    if cvss_version == '3':
        severity_title = ['attack_vector', 'attack_complexity',
                          'privileges_required', 'user_interaction',
                          'severity_scope', 'confidentiality_impact',
                          'integrity_impact', 'availability_impact',
                          'exploitability', 'remediation_level',
                          'report_confidence', 'confidentiality_requirement',
                          'integrity_requirement', 'availability_requirement',
                          'modified_attack_vector', 'modified_attack_complexity',
                          'modified_privileges_required', 'modified_user_interaction',
                          'modified_severity_scope', 'modified_confidentiality_impact',
                          'modified_integrity_impact', 'modified_availability_impact']
        severity_fields = {k: util.snakecase_to_camelcase(k) for k in severity_title}
        parsed_dict = {v: float(finding[k]) for (k, v) in severity_fields.items()
                       if k in finding.keys()}
        cvss_parameters = fin_dto.CVSS3_PARAMETERS
    else:
        severity_title = ['access_complexity', 'authentication', 'availability_impact',
                          'exploitability', 'confidentiality_impact', 'access_vector',
                          'resolution_level', 'integrity_impact',
                          'confidence_level', 'collateral_damage_potential',
                          'finding_distribution', 'confidentiality_requirement',
                          'integrity_requirement', 'availability_requirement']
        severity_fields = {k: util.snakecase_to_camelcase(k) for k in severity_title}
        parsed_dict = {v: float(finding[k]) for (k, v) in severity_fields.items()
                       if k in finding.keys()}
        cvss_parameters = fin_dto.CVSS_PARAMETERS
    base_score = float(cvss.calculate_cvss_basescore(
        parsed_dict, cvss_parameters, cvss_version))
    parsed_dict['baseScore'] = base_score
    parsed_dict['severityCvss'] = \
        cvss.calculate_cvss_temporal(parsed_dict, base_score, cvss_version)
    parsed_dict['impact'] = forms.get_impact(
        parsed_dict['severityCvss'], cvss_version)
    parsed_dict['exploitable'] = forms.is_exploitable(
        parsed_dict['exploitability'], cvss_version)
    parsed_dict['cvssVersion'] = cvss_version
    return parsed_dict


def parse_evidence_description(finding):
    """Parse evidence description."""
    description_fields = {
        'evidence_route_1': 'evidence_description_1',
        'evidence_route_2': 'evidence_description_2',
        'evidence_route_3': 'evidence_description_3',
        'evidence_route_4': 'evidence_description_4',
        'evidence_route_5': 'evidence_description_5'
    }
    if has_migrated_evidence(finding.get('finding_id')):
        evidence_tab_info = {description_fields[file_obj['name']]: file_obj.get('description')
                             for file_obj in finding.get('files')
                             if file_obj.get('name') in description_fields and
                             file_obj.get('description')}
    else:
        evidence_tab_info = {}
    return evidence_tab_info


def get_project_name(finding_id):
    """Get the name of the project of a finding."""
    project = integrates_dal.get_finding_project(finding_id)
    if not project:
        api = FormstackAPI()
        fin_dto = FindingDTO()
        finding_data = fin_dto.parse_project(api.get_submission(finding_id), finding_id)
        project = finding_data.get('projectName')
    else:
        # Project exist in dynamo
        pass
    return project
