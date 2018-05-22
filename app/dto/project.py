"""DTO to map the Integrates fields to formstack"""
# pylint: disable=E0402
class ProjectDTO(object):
    """ Class to create an object with the attributes of a finding. """

    #Atributos proyecto
    FLUID_PROJECT = "52601266"
    CLIENT_PROJECT = "60063920"
    CLIENT = "52601817"
    CLASS = "52602145"
    LEADER = "52603216"
    ANALIST = "53626289"
    ARQUITECT = "60154418"
    START_DATE = "52601351"
    END_DATE = "52601570"
    TEST_TYPE = "52762210"
    ENVIRONMENT = "60063680"
    COVERAGE_TYPE = "60064178"
    COVERAGE = "60063976"
    FINDINGS_MAP = "60294068"
    SECURITY_LEVEL = "60294098"
    TOE_VISIBLE_FIELDS = "52762496"
    TOE_VISIBLE_LINES = "52762572"
    TOE_VISIBLE_PORTS = "52762526"
    TOE_TESTED_FIELDS = "52762424"
    TOE_TESTED_LINES = "52602997"
    TOE_TESTED_PORTS = "52602989"
    RELEVANT_IMPACT = "60155980"
    OBSERVATIONS = "60063218"
    CONCLUSIONS = "60063227"
    RECOMMENDATIONS = "60294226"
    INDUSTRY_TYPE = "52765044"
    LANGUAGE = "52764314"
    APPLICATION_TYPE = "52762843"
    SUPPLIES = "60185565"
    ENVIRONMENT_CHANGES = "60185445"

    def __init__(self):
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def parse(self, request_arr): # noqa: C901
        self.data["timestamp"] = request_arr["timestamp"]
        self.request_id = request_arr["id"]
        self.parse_general(request_arr)
        self.parse_coverage(request_arr)
        self.parse_resume(request_arr)
        return self.data

    def parse_general(self, request_arr): # noqa: C901
        "Convert the description of a find into Formstack format."
        for finding in request_arr["data"]:
            if finding["field"] == self.FLUID_PROJECT:
                self.data["fluidProject"] = finding["value"]
            if finding["field"] == self.CLIENT_PROJECT:
                self.data["clientProject"] = finding["value"]
            if finding["field"] == self.CLIENT:
                self.data["client"] = finding["value"]
            if finding["field"] == self.CLASS:
                self.data["class"] = finding["value"]
            if finding["field"] == self.LEADER:
                self.data["leader"] = finding["value"]
            if finding["field"] == self.ANALIST:
                self.data["analyst"] = finding["value"]
            if finding["field"] == self.ARQUITECT:
                self.data["arquitect"] = finding["value"]
            if finding["field"] == self.START_DATE:
                self.data["startDate"] = finding["value"]
            if finding["field"] == self.END_DATE:
                self.data["endDate"] = finding["value"]
            if finding["field"] == self.TEST_TYPE:
                self.data["testType"] = finding["value"]
            if finding["field"] == self.ENVIRONMENT:
                self.data["environment"] = finding["value"]
            if finding["field"] == self.ENVIRONMENT_CHANGES:
                self.data["environment_changes"] = finding["value"]
            if finding["field"] == self.SUPPLIES:
                self.data["supplies"] = finding["value"]

    def parse_coverage(self, request_arr): # noqa: C901
        "Convert coverage of finding into project format."
        for finding in request_arr["data"]:
            if finding["field"] == self.COVERAGE_TYPE:
                self.data["coverageType"] = finding["value"]
            if finding["field"] == self.COVERAGE:
                self.data["coverage"] = finding["value"]
            if finding["field"] == self.TOE_VISIBLE_FIELDS:
                self.data["toeVisibleFields"] = finding["value"]
            if finding["field"] == self.TOE_VISIBLE_LINES:
                self.data["toeVisibleLines"] = finding["value"]
            if finding["field"] == self.TOE_VISIBLE_PORTS:
                self.data["toeVisiblePorts"] = finding["value"]
            if finding["field"] == self.TOE_TESTED_FIELDS:
                self.data["toeTestedFields"] = finding["value"]
            if finding["field"] == self.TOE_TESTED_LINES:
                self.data["toeTestedLines"] = finding["value"]
            if finding["field"] == self.TOE_TESTED_PORTS:
                self.data["toeTestedPorts"] = finding["value"]

    def parse_resume(self, request_arr): # noqa: C901
        "Convert the summary of a project"
        for finding in request_arr["data"]:
            if finding["field"] == self.FINDINGS_MAP:
                self.data["findingsMap"] = finding["value"]
            if finding["field"] == self.SECURITY_LEVEL:
                self.data["securityLevel"] = finding["value"]
            if finding["field"] == self.RELEVANT_IMPACT:
                self.data["relevantImpact"] = finding["value"]
            if finding["field"] == self.OBSERVATIONS:
                self.data["observations"] = finding["value"]
            if finding["field"] == self.CONCLUSIONS:
                self.data["conclusions"] = finding["value"]
            if finding["field"] == self.RECOMMENDATIONS:
                self.data["recommendations"] = finding["value"]
            if finding["field"] == self.INDUSTRY_TYPE:
                self.data["industryType"] = finding["value"]
            if finding["field"] == self.LANGUAGE:
                self.data["language"] = finding["value"]
            if finding["field"] == self.APPLICATION_TYPE:
                self.data["applicationType"] = finding["value"]
