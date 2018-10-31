""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
import base64
from datetime import datetime
import uuid

import pytz
import rollbar

from django.conf import settings

from ..dao import integrates_dao
from . import closing
from ..api.formstack import FormstackAPI
from ..utils import forms
from .. import util
from ..exceptions import InvalidRange


# pylint: disable=E0402

class FindingDTO(object):
    """ Class to create an object with the attributes of a finding. """
    FIELDS_FINDING = settings.FIELDS_FINDING
    #Atributos proyecto
    ANALIST = FIELDS_FINDING["ANALIST"]
    LEADER = FIELDS_FINDING["LEADER"]
    INTERESADO = FIELDS_FINDING["INTERESADO"]
    FLUID_PROJECT = FIELDS_FINDING["FLUID_PROJECT"]
    CLIENT_PROJECT = FIELDS_FINDING["CLIENT_PROJECT"]
    CONTEXT = FIELDS_FINDING["CONTEXT"]
    REVISION = FIELDS_FINDING["REVISION"]

    #Atributos evidencia
    DOC_TOTAL = FIELDS_FINDING["DOC_TOTAL"]
    DOC_ACHV1 = FIELDS_FINDING["DOC_ACHV1"]
    DOC_ACHV2 = FIELDS_FINDING["DOC_ACHV2"]
    DOC_ACHV3 = FIELDS_FINDING["DOC_ACHV3"]
    DOC_ACHV4 = FIELDS_FINDING["DOC_ACHV4"]
    DOC_ACHV5 = FIELDS_FINDING["DOC_ACHV5"]
    DOC_CMNT1 = FIELDS_FINDING["DOC_CMNT1"]
    DOC_CMNT2 = FIELDS_FINDING["DOC_CMNT2"]
    DOC_CMNT3 = FIELDS_FINDING["DOC_CMNT3"]
    DOC_CMNT4 = FIELDS_FINDING["DOC_CMNT4"]
    DOC_CMNT5 = FIELDS_FINDING["DOC_CMNT5"]
    ANIMATION = FIELDS_FINDING["ANIMATION"]
    EXPLOTATION = FIELDS_FINDING["EXPLOTATION"]
    EXPLOIT = FIELDS_FINDING["EXPLOIT"]
    REG = FIELDS_FINDING["REG"]
    REG_NUM = FIELDS_FINDING["REG_NUM"]
    REG_FILE = FIELDS_FINDING["REG_FILE"]
    VULNERABILITIES_FILE = FIELDS_FINDING["VULNERABILITIES_FILE"]

    #Atributos descriptivos
    CLASS = FIELDS_FINDING["CLASS"] #detallado
    FINDING = FIELDS_FINDING["FINDING"]
    SUBSCRIPTION = FIELDS_FINDING["SUBSCRIPTION"]
    CLIENT_CODE = FIELDS_FINDING["CLIENT_CODE"]
    PROBABILITY = FIELDS_FINDING["PROBABILITY"]
    SEVERITY = FIELDS_FINDING["SEVERITY"]
    RISK_LEVEL = FIELDS_FINDING["RISK_LEVEL"]
    RISK_VALUE = FIELDS_FINDING["RISK_VALUE"]
    CARDINALITY = FIELDS_FINDING["CARDINALITY"]
    WHERE = FIELDS_FINDING["WHERE"]
    VULNERABILITY = FIELDS_FINDING["VULNERABILITY"]
    THREAT = FIELDS_FINDING["THREAT"]
    APPLICABLE_COMPONENT = FIELDS_FINDING["APPLICABLE_COMPONENT"]
    TEST_TYPE = FIELDS_FINDING["TEST_TYPE"]
    FINDING_TYPE = FIELDS_FINDING["FINDING_TYPE"]
    RISK = FIELDS_FINDING["RISK"]
    REQUIREMENTS = FIELDS_FINDING["REQUIREMENTS"]
    EFFECT_SOLUTION = FIELDS_FINDING["EFFECT_SOLUTION"]
    KB_LINK = FIELDS_FINDING["KB"]
    TYPE = FIELDS_FINDING["TYPE"]
    ACTOR = FIELDS_FINDING["ACTOR"]
    CATEGORY = FIELDS_FINDING["CATEGORY"]
    SCENARIO = FIELDS_FINDING["SCENARIO"]
    AMBIT = FIELDS_FINDING["AMBIT"]
    AFFECTED_SYSTEMS = FIELDS_FINDING["AFFECTED_SYSTEMS"]
    ATTACK_VECTOR = FIELDS_FINDING["ATTACK_VECTOR"]
    CWE = FIELDS_FINDING["CWE"]
    TREATMENT = FIELDS_FINDING["TREATMENT"]
    TREATMENT_JUSTIFICATION = FIELDS_FINDING["TREATMENT_JUSTIFICATION"]
    TREATMENT_MANAGER = FIELDS_FINDING["TREATMENT_MANAGER"]
    EXTERNAL_BTS = FIELDS_FINDING["EXTERNAL_BTS"]
    LAST_VULNERABILITY = FIELDS_FINDING["LAST_VULNERABILITY"]
    RELEASE_DATE = FIELDS_FINDING["RELEASE_DATE"]
    RELATED_FINDINGS = FIELDS_FINDING["RELATED_FINDINGS"]

    #Atributos CssV2
    ACCESS_VECTOR = FIELDS_FINDING["ACCESS_VECTOR"]
    ACCESS_COMPLEXITY = FIELDS_FINDING["ACCESS_COMPLEXITY"]
    AUTHENTICATION = FIELDS_FINDING["AUTHENTICATION"]
    EXPLOITABILITY = FIELDS_FINDING["EXPLOITABILITY"]
    CRITICITY = FIELDS_FINDING["CRITICITY"]
    CONFIDENTIALITY_IMPACT = FIELDS_FINDING["CONFIDENTIALITY_IMPACT"]
    INTEGRITY_IMPACT = FIELDS_FINDING["INTEGRITY_IMPACT"]
    AVAILABILITY_IMPACT = FIELDS_FINDING["AVAILABILITY_IMPACT"]
    RESOLUTION_LEVEL = FIELDS_FINDING["RESOLUTION_LEVEL"]
    CONFIDENCE_LEVEL = FIELDS_FINDING["CONFIDENCE_LEVEL"]

    def __init__(self):
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def create_evidence_description(self, parameter): # noqa: C901
        """ Converts the index of a JSON to Formstack index """
        evidence_description_fields = {
            self.DOC_CMNT1: "evidenceDescription1",
            self.DOC_CMNT2: "evidenceDescription2",
            self.DOC_CMNT3: "evidenceDescription3",
            self.DOC_CMNT4: "evidenceDescription4",
            self.DOC_CMNT5: "evidenceDescription5"
        }
        parsed_dict = {k:parameter["data[" + v + "]"] \
                      for (k, v) in evidence_description_fields.items() \
                      if "data[" + v + "]" in parameter.keys()}
        return {"data":parsed_dict, "request_id":parameter["data[id]"]}

    def create_description(self, parameter): # noqa: C901
        """ Converts the index of a JSON to Formstack index """
        if "data[id]" in parameter:
            self.request_id \
                = parameter["data[id]"]
        if "data[finding]" in parameter:
            self.data[self.FINDING] \
                = parameter["data[finding]"]
        if "data[scenario]" in parameter:
            self.data[self.SCENARIO] \
                = parameter["data[scenario]"]
        if "data[openVulnerabilities]" in parameter:
            self.data[self.CARDINALITY] \
                = parameter["data[openVulnerabilities]"]
        if "data[actor]" in parameter:
            self.data[self.ACTOR] \
                = parameter["data[actor]"]
        if "data[vulnerability]" in parameter:
            self.data[self.VULNERABILITY] \
                = parameter["data[vulnerability]"]
        if "data[requirements]" in parameter:
            self.data[self.REQUIREMENTS] \
                = parameter["data[requirements]"]
        if "data[where]" in parameter:
            self.data[self.WHERE] \
                = parameter["data[where]"]
        if "data[effectSolution]" in parameter:
            self.data[self.EFFECT_SOLUTION] \
                = parameter["data[effectSolution]"]
        if "data[threat]" in parameter:
            self.data[self.THREAT] \
                = parameter["data[threat]"]
        if "data[attackVector]" in parameter:
            self.data[self.ATTACK_VECTOR] \
                = parameter["data[attackVector]"]
        if "data[affectedSystems]" in parameter:
            self.data[self.AFFECTED_SYSTEMS] \
                = parameter["data[affectedSystems]"]
        if "data[cwe]" in parameter:
            self.data[self.CWE] \
                = parameter["data[cwe]"]
        if "data[records]" in parameter:
            self.data[self.REG] \
                = parameter["data[records]"]
        if "data[recordsNumber]" in parameter:
            self.data[self.REG_NUM] \
                = parameter["data[recordsNumber]"]
        if "data[lastVulnerability]" in parameter:
            self.data[self.LAST_VULNERABILITY] \
                = parameter["data[lastVulnerability]"]
        if "data[releaseDate]" in parameter:
            self.data[self.RELEASE_DATE] \
                = parameter["data[releaseDate]"]
        if "data[level]" in parameter:
            self.data[self.CLASS] \
                = parameter["data[level]"]
            if self.data[self.CLASS] == "Detallado":
                if "data[category]" in parameter:
                    self.data[self.CATEGORY] \
                        = parameter["data[category]"]
                if "data[riskValue]" in parameter:
                    self.data[self.RISK_VALUE] \
                        = parameter["data[riskValue]"]
                if "data[probability]" in parameter:
                    self.data[self.PROBABILITY] \
                        = parameter["data[probability]"]
                if "data[severity]" in parameter:
                    self.data[self.SEVERITY] \
                        = parameter["data[severity]"]

    def create_treatment(self, parameter):
        """ Converts the index of a JSON to Formstack index """
        treatment_fields = {
            self.TREATMENT:"treatment",
            self.TREATMENT_JUSTIFICATION:"treatmentJustification",
            self.TREATMENT_MANAGER:"treatmentManager",
            self.EXTERNAL_BTS:"externalBts"
        }
        parsed_dict = {k:parameter["data[" + v + "]"] \
                       if "data[" + v + "]" in parameter.keys() else "" \
                       for (k, v) in treatment_fields.items()}
        return {"data":parsed_dict, "request_id":parameter["data[id]"]}


    def create_cssv2(self, parameter):
        """ Converts the index of a JSON to Formstack index """
        severity_tab_fields = {
            self.ACCESS_VECTOR: "accessVector",
            self.ACCESS_COMPLEXITY: "accessComplexity",
            self.AUTHENTICATION: "authentication",
            self.EXPLOITABILITY: "exploitability",
            self.CRITICITY: "criticity",
            self.CONFIDENTIALITY_IMPACT: "confidentialityImpact",
            self.INTEGRITY_IMPACT: "integrityImpact",
            self.AVAILABILITY_IMPACT: "availabilityImpact",
            self.RESOLUTION_LEVEL: "resolutionLevel",
            self.CONFIDENCE_LEVEL: "confidenceLevel"
        }
        parsed_dict = {k:parameter["data[" + v + "]"] \
                for (k, v) in severity_tab_fields.items()}
        return {"data":parsed_dict, "request_id":parameter["data[id]"]}

    def create_delete(self, parameter, analyst, project, finding):
        """ Create a data set to send in the finding deletion email """
        return {
            'mail_analista': analyst,
            'name_finding': finding,
            'id_finding': finding,
            'description': parameter["data[justification]"],
            'project': project,
        }

    def parse(self, submission_id, request_arr, sess_obj):
        self.data = dict()
        self.data["id"] = submission_id
        self.data["timestamp"] = request_arr["timestamp"]
        if sess_obj is not None:
            sess_obj.session["drive_urls"] = []
        self.data = forms.dict_concatenation(self.data, self.parse_description(request_arr))
        self.data = forms.dict_concatenation(self.data, self.parse_cssv2(request_arr))
        self.data = forms.dict_concatenation(self.data, self.parse_project(request_arr))
        self.data = forms.dict_concatenation(self.data, self.parse_evidence_info(request_arr))
        return self.data

    def parse_vulns_by_id(self, submission_id, request_arr):
        self.data = dict()
        self.data["id"] = submission_id
        self.data["timestamp"] = request_arr["timestamp"]
        self.data = forms.dict_concatenation(self.data, self.parse_description(request_arr))
        self.data = forms.dict_concatenation(self.data, self.parse_project(request_arr))
        self.data = forms.dict_concatenation(self.data, self.parse_evidence_info(request_arr))
        return self.data

    def parse_description(self, request_arr): # noqa: C901
        "Convert description of a finding into a formstack format"
        initial_dict = forms.create_dict(request_arr)
        self.data["timestamp"] = request_arr["timestamp"]
        evidence_description_fields = {
            self.FINDING:"finding",
            self.SUBSCRIPTION:"suscripcion",
            self.CLIENT_CODE:"codigo_cliente",
            self.PROBABILITY:"probability",
            self.SEVERITY:"severity",
            self.RISK_LEVEL:"nivel_riesgo",
            self.CARDINALITY:"openVulnerabilities",
            self.WHERE:"where",
            self.CRITICITY:"criticity",
            self.VULNERABILITY:"vulnerability",
            self.THREAT:"threat",
            self.CLIENT_PROJECT:"componente_aplicativo",
            self.TEST_TYPE:"testType",
            self.RISK:"riesgo",
            self.REQUIREMENTS:"requirements",
            self.EFFECT_SOLUTION:"effectSolution",
            self.KB_LINK:"kb",
            self.CLASS:"type",
            self.AFFECTED_SYSTEMS:"affectedSystems",
            self.ATTACK_VECTOR:"attackVector",
            self.FINDING_TYPE:"finding_type",
            self.REVISION:"revision",
            self.SCENARIO:"scenario",
            self.AMBIT:"ambito",
            self.CATEGORY:"category",
            self.ACTOR:"actor",
            self.TREATMENT:"treatment",
            self.TREATMENT_JUSTIFICATION:"treatmentJustification",
            self.TREATMENT_MANAGER:"treatmentManager",
            self.EXTERNAL_BTS:"externalBts",
            self.LAST_VULNERABILITY:"lastVulnerability",
            self.RELEASE_DATE:"releaseDate",
            self.CWE:"cwe"
        }
        parsed_dict = {v:initial_dict[k] \
                      for (k, v) in evidence_description_fields.items() \
                      if k in initial_dict.keys()}
        parsed_dict["impact"] = forms.get_impact(parsed_dict["criticity"])
        if "cwe" in parsed_dict.keys():
            parsed_dict["cwe"] = forms.get_cwe_url(parsed_dict["cwe"])
        else:
            return parsed_dict
        return parsed_dict

    def parse_description_mail(self, request_arr): # noqa: C901
        "Convert description of a finding into a formstack format para envio de mail"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.FINDING:
                self.data["finding"] = finding["value"]
        return self.data

    def parse_description_vuln(self, request_arr): # noqa: C901
        "Convert description of a finding into a formstack format"
        self.data["timestamp"] = request_arr["timestamp"]
        for finding in request_arr["data"]:
            if finding["field"] == self.CARDINALITY:
                self.data["openVulnerabilities"] = finding["value"]
        return self.data

    def parse_cssv2(self, request_arr): # noqa: C901
        "Convert the score of a finding into a formstack format"
        initial_dict = forms.create_dict(request_arr)
        severity_fields = {
            self.ACCESS_VECTOR:"accessVector",
            self.ACCESS_COMPLEXITY:"accessComplexity",
            self.AUTHENTICATION:"authentication",
            self.CONFIDENTIALITY_IMPACT:"confidentialityImpact",
            self.INTEGRITY_IMPACT:"integrityImpact",
            self.AVAILABILITY_IMPACT:"availabilityImpact",
            self.EXPLOITABILITY:"exploitability",
            self.RESOLUTION_LEVEL:"resolutionLevel",
            self.CONFIDENCE_LEVEL:"confidenceLevel"
        }
        parsed_dict = {v:initial_dict[k] \
                      for (k, v) in severity_fields.items() \
                      if k in initial_dict.keys()}
        parsed_dict['exploitable'] = forms.is_exploitable(parsed_dict['exploitability'])
        parsed_dict['clientFindingType'] = forms.get_finding_type(parsed_dict)
        return parsed_dict

    def parse_project(self, request_arr):
        "Convert project info in formstack format"
        initial_dict = forms.create_dict(request_arr)
        project_fields = {
            self.ANALIST:"analyst",
            self.LEADER:"leader",
            self.INTERESADO:"interested",
            self.FLUID_PROJECT:"fluidProject",
            self.CLIENT_PROJECT:"clientProject",
            self.CONTEXT:"context"
        }
        parsed_dict = {v:initial_dict[k] \
                      for (k, v) in project_fields.items() \
                      if k in initial_dict.keys()}
        return parsed_dict


    def parse_evidence_info(self, request_arr): # noqa: C901
        "Convert the score of a finding into a formstack format"
        initial_dict = forms.create_dict(request_arr)
        evidence_tab_fields = {
            self.DOC_TOTAL:"evidenceTotal",
            self.DOC_CMNT1:"evidence_description_1",
            self.DOC_CMNT2:"evidence_description_2",
            self.DOC_CMNT3:"evidence_description_3",
            self.DOC_CMNT4:"evidence_description_4",
            self.DOC_CMNT5:"evidence_description_5",
            self.REG:"records",
            self.REG_NUM:"recordsNumber"
        }
        evidence_fields_with_urls = {
            self.DOC_ACHV1:"evidence_route_1",
            self.DOC_ACHV2:"evidence_route_2",
            self.DOC_ACHV3:"evidence_route_3",
            self.DOC_ACHV4:"evidence_route_4",
            self.DOC_ACHV5:"evidence_route_5",
            self.ANIMATION:"animation",
            self.EXPLOTATION:"exploitation",
            self.EXPLOIT:"exploit",
            self.REG_FILE:"fileRecords",
            self.VULNERABILITIES_FILE:"vulnerabilities"
        }
        evidence_tab_info = {v:initial_dict[k] \
                      for (k, v) in evidence_tab_fields.items() \
                      if k in initial_dict.keys()}
        evidence_urls_info = {v:forms.drive_url_filter(initial_dict[k]) \
                      for (k, v) in evidence_fields_with_urls.items() \
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
        for key, value in self.data.iteritems():
            new_data["field_"+key] = value
        self.data = new_data

def format_finding_date(format_attr):
    tzn = pytz.timezone('America/Bogota')
    finding_date = datetime.strptime(
        format_attr.split(" ")[0],
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
        finding = fin_dto.parse_vulns_by_id(
            submission_id,
            api.get_submission(submission_id)
        )
        closingreqset = api.get_closings_by_id(submission_id)["submissions"]
        findingcloseset = []
        for closingreq in closingreqset:
            closingset = closing.parse(api.get_submission(closingreq["id"]))
            findingcloseset.append(closingset)
            state = closingset
        finding["estado"] = state["estado"]
        finding["cierres"] = findingcloseset
        finding['cardinalidad_total'] = finding['openVulnerabilities']
        if state.get("opened"):
            finding['openVulnerabilities'] = state['opened']
        if state.get("estado") == 'Cerrado':
            finding['where'] = '-'
            finding['edad'] = '-'
            finding['lastVulnerability'] = '-'
        if 'whichOpened' in state:
            finding['where'] = state['whichOpened']
        if 'whichClosed' in state:
            finding['closed'] = state['whichClosed']
        primary_keys = ["finding_id", submission_id]
        finding_dynamo = integrates_dao.get_data_dynamo(
            "FI_findings", primary_keys[0], primary_keys[1])
        if finding_dynamo:
            if finding_dynamo[0].get("releaseDate"):
                finding["releaseDate"] = finding_dynamo[0].get("releaseDate")
            if finding_dynamo[0].get("lastVulnerability"):
                finding["lastVulnerability"] = finding_dynamo[0].get("lastVulnerability")
        if finding.get("releaseDate"):
            tzn = pytz.timezone('America/Bogota')
            today_day = datetime.now(tz=tzn).date()
            finding_last_vuln = datetime.strptime(
                finding["releaseDate"].split(" ")[0],
                '%Y-%m-%d'
            )
            finding_last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
            if finding_last_vuln <= today_day:
                final_date = format_finding_date(finding["releaseDate"])
                finding['edad'] = ":n".replace(":n", str(final_date.days))
        return finding
    else:
        rollbar.report_message('Error: An error occurred catching finding', 'error')
        return None


def ungroup_specific(specific):
    """Ungroup specific value."""
    values = specific.split(",")
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
    limits = range_value.split("-")
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
    if vulnerability:
        response = update_vuln_state(vulnerability, item, finding_id, current_day)
    else:
        data = {}
        data['vuln_type'] = vuln
        data['where'] = where
        data['specific'] = specific
        data['finding_id'] = finding_id
        data['UUID'] = str(uuid.uuid4())
        if item.get('state'):
            historic_state.append({'date': current_day, 'state': item.get('state')})
            data['historic_state'] = historic_state
            response = integrates_dao.add_vulnerability_dynamo('FI_vulnerabilities', data)
        else:
            util.cloudwatch_log(
                info.context,
                'Security: Attempted to add vulnerability without state')
    return response
