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
