from graphene import String, ObjectType, Boolean, List, Int, JSONString, Float
from graphene.types.generic import GenericScalar
from app.entity.vulnerability import Vulnerability


class FindingType(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    id = String()  # noqa pylint: disable=invalid-name
    state = String()
    vulnerabilities = List(
        Vulnerability,
        vuln_type=String(),
        state=String())
    open_vulnerabilities = Int()
    closed_vulnerabilities = Int()
    project_name = String()
    release_date = String()
    records = JSONString()
    tracking = List(GenericScalar)
    severity = GenericScalar()
    exploit = String()
    evidence = GenericScalar()
    comments = List(GenericScalar)
    observations = List(GenericScalar)
    report_level = String()
    title = String()
    scenario = String()
    actor = String()
    description = String()
    requirements = String()
    attack_vector_desc = String()
    threat = String()
    recommendation = String()
    affected_systems = String()
    compromised_attributes = String()
    compromised_records = Int()
    cwe_url = String()
    bts_url = String()
    treatment = String()
    treatment_manager = String()
    treatment_justification = String()
    remediated = Boolean()
    type = String()
    cvss_version = String()
    age = Int()
    last_vulnerability = Int()
    severity_score = Float()
    is_exploitable = Boolean()
    report_date = String()
    analyst = String()

    # Additional attributes of detailed findings
    client_code = String()
    client_project = String()
    probability = Int()
    detailed_severity = Int()
    risk = String()
    risk_level = String()
    ambit = String()
    category = String()

    def __init__(self, *args, **kwargs):
        super(FindingType, self).__init__(args, kwargs)

        self.id = ''  # noqa pylint: disable=invalid-name
        self.vulnerabilities = []
        self.open_vulnerabilities = 0
        self.closed_vulnerabilities = 0
        self.project_name = ''
        self.release_date = ''
        self.records = {}
        self.severity = {}
        self.tracking = []
        self.comments = []
        self.observations = []
        self.report_level = ''
        self.title = ''
        self.scenario = ''
        self.actor = ''
        self.description = ''
        self.requirements = ''
        self.attack_vector_desc = ''
        self.threat = ''
        self.recommendation = ''
        self.affected_systems = ''
        self.compromised_attributes = ''
        self.compromised_records = 0
        self.cwe_url = ''
        self.bts_url = ''
        self.treatment = ''
        self.treatment_manager = ''
        self.treatment_justification = ''
        self.type = ''
        self.cvss_version = ''
        self.exploit = ''
        self.age = 0
        self.last_vulnerability = 0
        self.severity_score = 0.0
        self.is_exploitable = False
        self.remediated = ''
        self.report_date = ''
