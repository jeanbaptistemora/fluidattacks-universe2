import boto3
from decimal import (
    Decimal,
)
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
)

pytestmark = [
    pytest.mark.asyncio,
]

tables_names = ["integrates_vms"]
key_schemas = {
    "integrates_vms": [
        {"AttributeName": "pk", "KeyType": "HASH"},
        {"AttributeName": "sk", "KeyType": "RANGE"},
    ],
}
attribute_definitions = {
    "integrates_vms": [
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "pk", "AttributeType": "S"},
    ],
}
global_secondary_indexes: Dict[str, List[Any]] = {
    "integrates_vms": [
        {
            "IndexName": "inverted_index",
            "KeySchema": [
                {"AttributeName": "sk", "KeyType": "HASH"},
                {"AttributeName": "pk", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        }
    ],
}
data: Dict[str, List[Any]] = dict(
    integrates_vms=[
        dict(
            severity=dict(
                attack_complexity=Decimal("0.4"),
                integrity_impact=Decimal("0"),
                integrity_requirement=Decimal("0.5"),
                modified_confidentiality_impact=Decimal("0"),
                modified_user_interaction=Decimal("0.85"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0"),
                report_confidence=Decimal("0.96"),
                modified_integrity_impact=Decimal("0"),
                attack_vector=Decimal("0.62"),
                modified_attack_complexity=Decimal("0.77"),
                privileges_required=Decimal("0.85"),
                availability_impact=Decimal("0.22"),
                modified_privileges_required=Decimal("0.85"),
                confidentiality_requirement=Decimal("1.5"),
                modified_attack_vector=Decimal("0.85"),
                user_interaction=Decimal("0.62"),
                confidentiality_impact=Decimal("0"),
                exploitability=Decimal("0.97"),
                remediation_level=Decimal("0.97"),
                severity_scope=Decimal("1"),
                availability_requirement=Decimal("1.5"),
            ),
            requirements="""REQ.0176. El sistema debe restringir el acceso a
                objetos del sistema que tengan contenido sensible. Sólo
                permitirá su acceso a usuarios autorizados.""",
            group_name="unittesting",
            approval=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T05:00:00+00:00",
                status="APPROVED",
            ),
            description="""Se obtiene información de negocio, como:\r\n
                - Lista de usuarios\r\n- Información estratégica\r\n
                - Información de empleados\r\n- Información de clientes\r\n
                - Información de proveedores""",
            recommendation="""De acuerdo a la clasificación de la información
                encontrada, establecer los controles necesarios para que la
                información sea accesible sólo a las personas indicadas.""",
            unreliable_indicators=dict(
                unreliable_where="""192.168.1.10, 192.168.1.12, 192.168.1.13,
                    192.168.1.14, 192.168.1.15, 192.168.1.16, 192.168.1.17,
                    192.168.1.2, 192.168.1.3, 192.168.1.4, 192.168.1.5,
                    192.168.1.6, 192.168.1.7, 192.168.1.8, 192.168.1.9,
                    192.168.100.101, 192.168.100.104, 192.168.100.105,
                    192.168.100.108, 192.168.100.111""",
                unreliable_newest_vulnerability_report_date=(
                    "2019-09-16T21:01:24+00:00"
                ),
                unreliable_verification_summary=dict(
                    verified=Decimal("1"),
                    requested=Decimal("1"),
                    on_hold=Decimal("2"),
                ),
                unreliable_open_vulnerabilities=Decimal("24"),
                unreliable_treatment_summary=dict(
                    accepted=Decimal("0"),
                    untreated=Decimal("24"),
                    in_progress=Decimal("0"),
                    accepted_undefined=Decimal("0"),
                ),
                unreliable_oldest_vulnerability_report_date=(
                    "2019-08-30T14:30:13+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    "2019-08-30T14:30:13+00:00"
                ),
                unreliable_closed_vulnerabilities=Decimal("4"),
                unreliable_status="OPEN",
            ),
            title="038. Business information leak",
            analyst_email="unittest@fluidattacks.com",
            cvss_version="3.1",
            sk="GROUP#unittesting",
            submission=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T00:45:11+00:00",
                status="SUBMITTED",
            ),
            id="436992569",
            pk="FIN#436992569",
            state=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T05:00:00+00:00",
                status="APPROVED",
            ),
            threat="Risk.",
            evidences=dict(
                exploitation=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="test",
                    url="unittesting-436992569-exploitation.png",
                ),
                evidence1=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm1",
                    url="unittesting-436992569-evidence_route_1.png",
                ),
                evidence2=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm2",
                    url="unittesting-436992569-evidence_route_2.jpg",
                ),
                evidence3=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm3",
                    url="unittesting-436992569-evidence_route_3.png",
                ),
                evidence4=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm4",
                    url="unittesting-436992569-evidence_route_4.png",
                ),
                evidence5=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="Comm5",
                    url="unittesting-436992569-evidence_route_5.png",
                ),
            ),
            animation=dict(
                modified_date="2019-04-08T05:00:00+00:00",
                description="Test description.",
                url="unittesting-436992569-animation.png",
            ),
            min_time_to_remediate=Decimal("18"),
            sorts="NO",
            attack_vector_description="This is an attack vector",
            creation=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T00:43:18+00:00",
                status="CREATED",
            ),
            verification=dict(
                modified_by="integrateshacker@fluidattacks.com",
                vulnerability_ids=["15375781-31f2-4953-ac77-f31134225747"],
                comment_id="1558048727111",
                modified_date="2020-02-21T15:41:04+00:00",
                status="VERIFIED",
            ),
        ),
        dict(
            severity=dict(
                attack_complexity=Decimal("0.77"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1"),
                modified_confidentiality_impact=Decimal("0"),
                modified_user_interaction=Decimal("0.85"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0"),
                report_confidence=Decimal("0.92"),
                modified_integrity_impact=Decimal("0.22"),
                attack_vector=Decimal("0.62"),
                modified_attack_complexity=Decimal("0.77"),
                privileges_required=Decimal("0.62"),
                availability_impact=Decimal("0"),
                modified_privileges_required=Decimal("0.62"),
                confidentiality_requirement=Decimal("1"),
                modified_attack_vector=Decimal("0.62"),
                user_interaction=Decimal("0.85"),
                confidentiality_impact=Decimal("0"),
                exploitability=Decimal("0.91"),
                remediation_level=Decimal("0.97"),
                severity_scope=Decimal("0"),
                availability_requirement=Decimal("1"),
            ),
            requirements="R359. Avoid using generic exceptions.",
            group_name="unittesting",
            approval=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-07-09T05:00:00+00:00",
                status="APPROVED",
            ),
            description="""he source code uses generic exceptions to handle
                unexpected errors. Catching generic exceptions obscures the
                problem that caused the error and promotes a generic way to
                handle different categories or sources of error. This may
                cause security vulnerabilities to materialize, as some special
                flows go unnoticed.""",
            recommendation="""Implement password politicies with the best
                practicies for strong passwords.""",
            unreliable_indicators=dict(
                unreliable_where="test/data/lib_path/f060/csharp.cs",
                unreliable_newest_vulnerability_report_date=(
                    "2020-01-03T17:46:10+00:00"
                ),
                unreliable_verification_summary=dict(
                    verified=Decimal("0"),
                    requested=Decimal("0"),
                    on_hold=Decimal("0"),
                ),
                unreliable_open_vulnerabilities=Decimal("1"),
                unreliable_treatment_summary=dict(
                    accepted=Decimal("0"),
                    untreated=Decimal("0"),
                    in_progress=Decimal("1"),
                    accepted_undefined=Decimal("0"),
                ),
                unreliable_oldest_vulnerability_report_date=(
                    "2020-01-03T17:46:10+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    "2020-01-03T17:46:10+00:00"
                ),
                unreliable_closed_vulnerabilities=Decimal("0"),
                unreliable_status="OPEN",
            ),
            title="060. Insecure service configuration - Host verification",
            analyst_email="unittest@fluidattacks.com",
            cvss_version="3.1",
            sk="GROUP#unittesting",
            submission=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-04-08T00:45:11+00:00",
                status="SUBMITTED",
            ),
            id="422286126",
            pk="FIN#422286126",
            state=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-07-09T05:00:00+00:00",
                status="APPROVED",
            ),
            threat="""A attack can get passwords  of users and
                He can impersonate them or used the credentials
                for practices maliciosus.""",
            evidences=dict(
                exploitation=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="test",
                    url="unittesting-422286126-exploitation.png",
                ),
                records=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="test",
                    url="unittesting-422286126-evidence_file.csv",
                ),
                evidence1=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description='this is a test description"',
                    url="unittesting-422286126-evidence_route_1.png",
                ),
                evidence2=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="exception",
                    url="unittesting-422286126-evidence_route_2.jpg",
                ),
                evidence3=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="update testing",
                    url="unittesting-422286126-evidence_route_3.png",
                ),
                evidence4=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="changed for testing purposesese",
                    url="unittesting-422286126-evidence_route_4.png",
                ),
                evidence5=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="Test description.",
                    url="unittesting-422286126-evidence_route_5.png",
                ),
            ),
            animation=dict(
                modified_date="2018-07-09T05:00:00+00:00",
                description="Test description.",
                url="unittesting-422286126-animation.gif",
            ),
            min_time_to_remediate=Decimal("18"),
            sorts="NO",
            attack_vector_description="This is an attack vector",
            creation=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-04-08T00:43:18+00:00",
                status="CREATED",
            ),
            verification=dict(
                modified_by="integrateshacker@fluidattacks.com",
                vulnerability_ids=["15375781-31f2-4953-ac77-f31134225747"],
                comment_id="1558048727111",
                modified_date="2020-02-21T15:41:04+00:00",
                status="VERIFIED",
            ),
        ),
        dict(
            severity=dict(
                attack_complexity=Decimal("0.77"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1"),
                modified_confidentiality_impact=Decimal("0"),
                modified_user_interaction=Decimal("0.85"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0"),
                report_confidence=Decimal("0.96"),
                modified_integrity_impact=Decimal("0"),
                attack_vector=Decimal("0.85"),
                modified_attack_complexity=Decimal("0.77"),
                privileges_required=Decimal("0.85"),
                availability_impact=Decimal("0.22"),
                modified_privileges_required=Decimal("0.62"),
                confidentiality_requirement=Decimal("1.5"),
                modified_attack_vector=Decimal("0.55"),
                user_interaction=Decimal("0.85"),
                confidentiality_impact=Decimal("0.22"),
                exploitability=Decimal("0.94"),
                remediation_level=Decimal("0.95"),
                severity_scope=Decimal("0"),
                availability_requirement=Decimal("0.5"),
            ),
            requirements="""REQ.0266. La organización debe deshabilitar las
                funciones inseguras de un sistema. (hardening de sistemas)""",
            group_name="unittesting",
            approval=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T00:45:15+00:00",
                status="APPROVED",
            ),
            description="Funcionalidad insegura description",
            recommendation="Recomendacion de prueba.",
            unreliable_indicators=dict(
                unreliable_where="192.168.1.19",
                unreliable_newest_vulnerability_report_date=(
                    "2019-04-08T00:45:15+00:00"
                ),
                unreliable_verification_summary=dict(
                    verified=Decimal("0"),
                    requested=Decimal("0"),
                    on_hold=Decimal("0"),
                ),
                unreliable_open_vulnerabilities=Decimal("1"),
                unreliable_treatment_summary=dict(
                    accepted=Decimal("0"),
                    untreated=Decimal("0"),
                    in_progress=Decimal("0"),
                    accepted_undefined=Decimal("1"),
                ),
                unreliable_oldest_vulnerability_report_date=(
                    "2019-04-08T00:45:15+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    "2019-04-08T00:45:15+00:00"
                ),
                unreliable_closed_vulnerabilities=Decimal("1"),
                unreliable_status="OPEN",
            ),
            title="014. Insecure functionality",
            analyst_email="integratesmanager@gmail.com",
            cvss_version="3.1",
            sk="GROUP#unittesting",
            submission=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T00:45:11+00:00",
                status="SUBMITTED",
            ),
            id="988493279",
            pk="FIN#988493279",
            state=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T05:00:00+00:00",
                status="APPROVED",
            ),
            threat="Risk.",
            evidences=dict(
                exploitation=dict(
                    modified_date="2019-04-08T05:00:00+00:00",
                    description="test",
                    url="unittesting-988493279-exploitation.png",
                ),
            ),
            min_time_to_remediate=Decimal("20"),
            sorts="NO",
            attack_vector_description="This is an attack vector",
            creation=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2019-04-08T00:43:18+00:00",
                status="CREATED",
            ),
        ),
        dict(
            pk="VULN#15375781-31f2-4953-ac77-f31134225747",
            sk="STATE#2019-09-13T13:17:41+00:00",
            status="OPEN",
            modified_date="2019-09-13T13:17:41+00:00",
            modified_by="unittest@fluidattacks.com",
            source="ASM",
            specific="333",
            tool=dict(
                name="tool-2",
                impact="INDIRECT",
            ),
            where="192.168.100.101",
        ),
        dict(
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            sk="STATE#2020-01-03T17:46:10+00:00",
            status="OPEN",
            modified_date="2020-01-03T17:46:10+00:00",
            modified_by="unittest@fluidattacks.com",
            source="ASM",
            specific="12",
            tool=dict(
                name="tool-2",
                impact="INDIRECT",
            ),
            where="test/data/lib_path/f060/csharp.cs",
        ),
        dict(
            pk="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            sk="STATE#2019-04-08T00:45:15+00:00",
            status="OPEN",
            modified_date="2019-04-08T00:45:15+00:00",
            modified_by="unittest@fluidattacks.com",
            source="ASM",
            specific="8888",
            tool=dict(
                name="tool-1",
                impact="INDIRECT",
            ),
            where="192.168.1.19",
        ),
        dict(
            treatment=dict(
                modified_date="2019-09-13T13:17:41+00:00",
                status="NEW",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#436992569",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=1,
                unreliable_source="ASM",
                unreliable_last_reattack_date="2020-02-19T15:41:04+00:00",
                unreliable_last_reattack_requester="integratesuser@gmail.com",
                unreliable_last_requested_reattack_date=(
                    "2020-02-18T15:41:04+00:00"
                ),
                unreliable_efficacy=0,
                unreliable_treatment_changes=0,
            ),
            specific="333",
            type="PORTS",
            created_by="unittest@fluidattacks.com",
            sk="FIN#436992569",
            sk_3="VULN#15375781-31f2-4953-ac77-f31134225747",
            pk_2="ROOT",
            where="192.168.100.101",
            created_date="2019-09-13T13:17:41+00:00",
            pk="VULN#15375781-31f2-4953-ac77-f31134225747",
            pk_3="USER",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#verified",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2019-09-13T13:17:41+00:00",
                specific="333",
                status="OPEN",
                tool=dict(
                    name="tool-2",
                    impact="INDIRECT",
                ),
                where="192.168.100.101",
            ),
            sk_2="VULN#15375781-31f2-4953-ac77-f31134225747",
            verification=dict(
                modified_date="2020-02-19T15:41:04+00:00",
                status="VERIFIED",
            ),
        ),
        dict(
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                assigned="integratesuser2@gmail.com",
                justification="test justification",
                modified_date="2020-01-03T17:46:10+00:00",
                status="IN_PROGRESS",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#422286126",
            commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=0,
            ),
            specific="12",
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#422286126",
            sk_3="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_2="ROOT",
            where="test/data/lib_path/f060/csharp.cs",
            created_date="2020-01-03T17:46:10+00:00",
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2020-01-03T17:46:10+00:00",
                specific="12",
                status="OPEN",
                tool=dict(
                    name="tool-2",
                    impact="INDIRECT",
                ),
                where="test/data/lib_path/f060/csharp.cs",
            ),
            sk_2="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
        ),
        dict(
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                assigned="integratesuser@gmail.com",
                justification="Observations about permanently accepted",
                modified_date="2020-10-08T00:59:06+00:00",
                acceptance_status="APPROVED",
                status="ACCEPTED_UNDEFINED",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#988493279",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=2,
            ),
            specific="8888",
            type="PORTS",
            created_by="unittest@fluidattacks.com",
            sk="FIN#988493279",
            sk_3="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            pk_2="ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            where="192.168.1.19",
            created_date="2019-04-08T00:45:15+00:00",
            pk="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2019-04-08T00:45:15+00:00",
                specific="8888",
                status="OPEN",
                tool=dict(
                    name="tool-1",
                    impact="INDIRECT",
                ),
                where="192.168.1.19",
            ),
            sk_2="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
        ),
        dict(
            pk="VULN#15375781-31f2-4953-ac77-f31134225747",
            sk="TREATMENT#2019-09-13T13:17:41+00:00",
            status="NEW",
            modified_date="2019-09-13T13:17:41+00:00",
        ),
        dict(
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            sk="TREATMENT#2020-01-03T17:46:10+00:00",
            status="IN_PROGRESS",
            modified_date="2020-01-03T17:46:10+00:00",
            modified_by="integratesuser@gmail.com",
            assigned="integratesuser2@gmail.com",
            justification="test justification",
        ),
        dict(
            pk="VULN#47ce0fb0-4108-49b0-93cc-160dce8168a6",
            sk="TREATMENT#2019-04-08T00:59:06+00:00",
            status="ACCEPTED_UNDEFINED",
            modified_date="2019-04-08T00:59:06+00:00",
            modified_by="integratesuser@gmail.com",
            assigned="integratesuser2@gmail.com",
            justification="test justification permanently accepted",
            acceptance_status="SUBMITTED",
        ),
    ],
)


@pytest.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> AsyncGenerator[ServiceResource, None]:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module", autouse=True)
def create_tables(dynamo_resource: ServiceResource) -> None:
    for table in tables_names:
        dynamo_resource.create_table(
            TableName=table,
            KeySchema=key_schemas[table],  # type: ignore
            AttributeDefinitions=attribute_definitions[table],  # type: ignore
            GlobalSecondaryIndexes=global_secondary_indexes[table],
        )
        for item in data[table]:
            dynamo_resource.Table(table).put_item(Item=item)
