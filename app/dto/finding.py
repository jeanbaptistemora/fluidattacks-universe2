""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
import base64
from ..utils import forms

class FindingDTO(object):
    """ Class to create an object with the attributes of a finding. """

    #Atributos proyecto
    ANALIST = "32201744"
    LEADER = "38193323"
    INTERESADO = "38392409"
    FLUID_PROJECT = "32201732"
    CLIENT_PROJECT = "38209122"
    CONTEXT = "38404474"

    #Atributos evidencia
    REVISION = "54856382"
    DOC_TOTAL = "53714016"
    DOC_ACHV1 = "32202896"
    DOC_ACHV2 = "53713035"
    DOC_ACHV3 = "53713045"
    DOC_ACHV4 = "53714414"
    DOC_ACHV5 = "53714452"
    DOC_CMNT1 = "53713106"
    DOC_CMNT2 = "53713149"
    DOC_CMNT3 = "53713153"
    DOC_CMNT4 = "53714417"
    DOC_CMNT5 = "53714455"
    ANIMATION = "38307272"
    EXPLOTATION = "38307222"
    EXPLOIT = "38307199"
    REG = "53609444"
    REG_NUM = "49412242"
    REG_FILE = "49412246"

    #Atributos descriptivos
    CLASS = "38392454" #detallado
    FINDING = "32201810"
    SUBSCRIPTION = "54346108"
    CLIENT_CODE = "38193365"
    PROBABILITY = "38193660"
    SEVERITY = "38193659"
    RISK_LEVEL = "38194645"
    RISK_VALUE = "38194645"
    CARDINALITY = "38255025"
    WHERE = "38193357"
    CRITICITY = "38531129"
    VULNERABILITY = "32202728"
    THREAT = "38193361"
    APPLICABLE_COMPONENT = "38209122"
    TEST_TYPE = "38254692"
    FINDING_TYPE = "54319180"
    RISK = "38193362"
    REQUIREMENTS = "38254586"
    EFFECT_SOLUTION = "38619077"
    KB = "38861739"
    TYPE = "38392454"
    ACTOR = "38606398"
    CATEGORY = "46956845"
    SCENARIO = "38692215"
    AMBIT = "38254691"
    AFFECTED_SYSTEMS = "48092123"
    ATTACK_VECTOR = "48092088"
    CWE = "38899046"
    TREATMENT = "59350064"
    TREATMENT_JUSTIFICATION = "59351642"
    TREATMENT_MANAGER = "59381058"
    EXTERNAL_BTS = "56614832"
    LAST_VULNERABILITY = "63672923"
    RELEASE_DATE = "64313858"
    RELATED_FINDINGS = "38606215"

    #Atributos CssV2
    ACCESS_VECTOR = "38529247"
    ACCESS_COMPLEXITY = "38529248"
    AUTHENTICATION = "38529249"
    EXPLOITABILITY = "38529253"
    CRITICITY = "38531129"
    CONFIDENTIALITY_IMPACT = "38529250"
    INTEGRITY_IMPACT = "38529251"
    AVAILABILITY_IMPACT = "38529252"
    RESOLUTION_LEVEL = "38529254"
    CONFIDENCE_LEVEL = "38529255"

    def __init__(self):
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def create_evidence_description(self, parameter): # noqa: C901
        """ Converts the index of a JSON to Formstack index """
        evidence_description_fields = {
            "53713106":"evidenceDescription1",
            "53713149":"evidenceDescription2",
            "53713153":"evidenceDescription3",
            "53714417":"evidenceDescription4",
            "53714455":"evidenceDescription5"
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
            "59350064":"treatment",
            "59351642":"treatmentJustification",
            "59381058":"treatmentManager",
            "56614832":"externalBts"
        }
        parsed_dict = {k:parameter["data[" + v + "]"] \
                       if "data[" + v + "]" in parameter.keys() else "" \
                       for (k,v) in treatment_fields.items()}
        return {"data":parsed_dict, "request_id":parameter["data[id]"]}


    def create_cssv2(self, parameter):
        """ Converts the index of a JSON to Formstack index """
        severity_tab_fields = {
            "38529247":"accessVector",
            "38529248":"accessComplexity",
            "38529249":"authentication",
            "38529253":"exploitability",
            "38531129":"criticity",
            "38529250":"confidentialityImpact",
            "38529251":"integrityImpact",
            "38529252":"availabilityImpact",
            "38529254":"resolutionLevel",
            "38529255":"confidenceLevel"
        }
        parsed_dict = {k:parameter["data[" + v + "]"] \
                for (k,v) in severity_tab_fields.items()}
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
            "32201810":"finding",
            "54346108":"suscripcion",
            "38193365":"codigo_cliente",
            "38193660":"probability",
            "38193659":"severity",
            "38194645":"nivel_riesgo",
            "38255025":"openVulnerabilities",
            "38193357":"where",
            "38531129":"criticity",
            "32202728":"vulnerability",
            "38193361":"threat",
            "38209122":"componente_aplicativo",
            "38254692":"testType",
            "38193362":"riesgo",
            "38254586":"requirements",
            "38619077":"effectSolution",
            "38861739":"kb",
            "38392454":"type",
            "48092123":"affectedSystems",
            "48092088":"attackVector",
            "54319180":"finding_type",
            "54856382":"revision",
            "38692215":"scenario",
            "38254691":"ambito",
            "46956845":"category",
            "38606398":"actor",
            "59350064":"treatment",
            "59351642":"treatmentJustification",
            "59381058":"treatmentManager",
            "56614832":"externalBts",
            "63672923":"lastVulnerability",
            "64313858":"releaseDate",
            "38899046":"cwe"
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
            "38529247":"accessVector",
            "38529248":"accessComplexity",
            "38529249":"authentication",
            "38529250":"confidentialityImpact",
            "38529251":"integrityImpact",
            "38529252":"availabilityImpact",
            "38529253":"exploitability",
            "38529254":"resolutionLevel",
            "38529255":"confidenceLevel"
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
            "32201744":"analyst",
            "38193323":"leader",
            "38392409":"interested",
            "32201732":"fluidProject",
            "38209122":"clientProject",
            "38404474":"context"
        }
        parsed_dict = {v:initial_dict[k] \
                      for (k, v) in project_fields.items() \
                      if k in initial_dict.keys()}
        return parsed_dict


    def parse_evidence_info(self, request_arr): # noqa: C901
        "Convert the score of a finding into a formstack format"
        initial_dict = forms.create_dict(request_arr)
        evidence_tab_fields = {
            "53714016":"evidenceTotal",
            "53713106":"evidence_description_1",
            "53713149":"evidence_description_2",
            "53713153":"evidence_description_3",
            "53714417":"evidence_description_4",
            "53714455":"evidence_description_5",
            "53609444":"records",
            "49412242":"recordsNumber"
        }
        evidence_fields_with_urls = {
            "32202896":"evidence_route_1",
            "53713035":"evidence_route_2",
            "53713045":"evidence_route_3",
            "53714414":"evidence_route_4",
            "53714452":"evidence_route_5",
            "38307272":"animation",
            "38307222":"exploitation",
            "38307199":"exploit",
            "49412246":"fileRecords"
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
