# coding=utf-8
""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level

from django.conf import settings

from ..dal import integrates_dal
from ..domain import vulnerability as vuln_domain
from ..utils import forms
from .. import util


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
