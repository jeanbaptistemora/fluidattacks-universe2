import boto3
from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from decimal import (
    Decimal,
)
from moto import (
    mock_s3,
)
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from mypy_boto3_s3 import (
    S3Client,
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

BUCKET_NAME = FI_AWS_S3_MAIN_BUCKET

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
                attack_complexity=Decimal("0.44"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1.5"),
                modified_confidentiality_impact=Decimal("0.56"),
                modified_user_interaction=Decimal("0.62"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0"),
                report_confidence=Decimal("0.96"),
                modified_integrity_impact=Decimal("0.22"),
                attack_vector=Decimal("0.62"),
                modified_attack_complexity=Decimal("0.44"),
                privileges_required=Decimal("0.62"),
                availability_impact=Decimal("0"),
                modified_privileges_required=Decimal("0.62"),
                confidentiality_requirement=Decimal("1"),
                modified_attack_vector=Decimal("0.62"),
                user_interaction=Decimal("0.62"),
                confidentiality_impact=Decimal("0.56"),
                exploitability=Decimal("0.91"),
                remediation_level=Decimal("0.95"),
                severity_scope=Decimal("0"),
                availability_requirement=Decimal("1"),
            ),
            requirements="""REQ.0174. La aplicación debe garantizar que las
                peticiones que ejecuten transacciones no sigan un patrón
                discernible.""",
            group_name="unittesting",
            approval=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-12-17T05:00:00+00:00",
                status="APPROVED",
            ),
            description="""La aplicación permite engañar a un usuario
                autenticado por medio de links manipulados para ejecutar
                acciones sobre la aplicación sin su consentimiento.""",
            recommendation="""Hacer uso de tokens en los formularios para la
                verificación de las peticiones realizadas por usuarios
                legítimos.""",
            unreliable_indicators=dict(
                unreliable_where="path/to/file2.ext",
                unreliable_newest_vulnerability_report_date=(
                    "2019-01-15T16:04:14+00:00"
                ),
                unreliable_verification_summary=dict(
                    verified=Decimal("0"),
                    requested=Decimal("0"),
                    on_hold=Decimal("0"),
                ),
                unreliable_open_vulnerabilities=Decimal("1"),
                unreliable_treatment_summary=dict(
                    accepted=Decimal("1"),
                    new=Decimal("0"),
                    in_progress=Decimal("0"),
                    accepted_undefined=Decimal("0"),
                ),
                unreliable_oldest_vulnerability_report_date=(
                    "2019-01-15T15:43:39+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    "2019-01-15T15:43:39+00:00"
                ),
                unreliable_closed_vulnerabilities=Decimal("1"),
                unreliable_status="OPEN",
            ),
            title="007. Cross-site request forgery",
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
            id="463558592",
            pk="FIN#463558592",
            state=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-12-17T05:00:00+00:00",
                status="APPROVED",
            ),
            threat="Test.",
            evidences=dict(
                evidence1=dict(
                    modified_date="2018-12-17T05:00:00+00:00",
                    description="test",
                    url="unittesting-463558592-evidence_route_1.png",
                ),
                evidence2=dict(
                    modified_date="2018-12-17T05:00:00+00:00",
                    description="Test2",
                    url="unittesting-463558592-evidence_route_2.jpg",
                ),
                evidence3=dict(
                    modified_date="2018-12-17T05:00:00+00:00",
                    description="Test3",
                    url="unittesting-463558592-evidence_route_3.png",
                ),
                evidence4=dict(
                    modified_date="2018-12-17T05:00:00+00:00",
                    description="Test4",
                    url="unittesting-463558592-evidence_route_4.png",
                ),
                evidence5=dict(
                    modified_date="2018-12-17T05:00:00+00:00",
                    description="Test5",
                    url="unittesting-463558592-evidence_route_5.png",
                ),
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
                modified_by="integratesuser@gmail.com",
                vulnerability_ids=[
                    "3bcdb384-5547-4170-a0b6-3b397a245465",
                    "74632c0c-db08-47c2-b013-c70e5b67c49f",
                ],
                comment_id="1558048727999",
                modified_date="2020-01-19T15:41:04+00:00",
                status="REQUESTED",
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
            description="""The source code uses generic exceptions to handle
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
                    new=Decimal("0"),
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
            threat="""An attacker can get passwords of users and impersonate
                them or used the credentials for practices maliciosus.""",
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
                    description="this is a test description",
                    url="unittesting-422286126-evidence_route_1.png",
                ),
                evidence2=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="exception",
                    url="unittesting-422286126-evidence_route_2.jpg",
                ),
                evidence3=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="Description",
                    url="unittesting-422286126-evidence_route_3.png",
                ),
                evidence4=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="changed for testing purposesese",
                    url="unittesting-422286126-evidence_route_4.png",
                ),
                evidence5=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="Test description",
                    url="unittesting-422286126-evidence_route_5.png",
                ),
                animation=dict(
                    modified_date="2018-07-09T05:00:00+00:00",
                    description="Test description",
                    url="unittesting-422286126-animation.gif",
                ),
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
        ),
        dict(
            severity=dict(
                attack_complexity=Decimal("0.44"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1"),
                modified_confidentiality_impact=Decimal("0.22"),
                modified_user_interaction=Decimal("0.85"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0.22"),
                report_confidence=Decimal("0.92"),
                modified_integrity_impact=Decimal("0.22"),
                attack_vector=Decimal("0.62"),
                modified_attack_complexity=Decimal("0.44"),
                privileges_required=Decimal("0.62"),
                availability_impact=Decimal("0.22"),
                modified_privileges_required=Decimal("0.62"),
                confidentiality_requirement=Decimal("1"),
                modified_attack_vector=Decimal("0.62"),
                user_interaction=Decimal("0.85"),
                confidentiality_impact=Decimal("0.22"),
                exploitability=Decimal("0.94"),
                remediation_level=Decimal("0.96"),
                severity_scope=Decimal("0"),
                availability_requirement=Decimal("1"),
            ),
            requirements="""REQ.0077. La aplicación no debe revelar detalles
                del sistema interno como stack traces, fragmentos de
                sentencias SQL y nombres de base de datos o tablas.
                REQ.0176. El sistema debe restringir el acceso a objetos del
                sistema que tengan contenido sensible. Sólo permitirá su
                acceso a usuarios autorizados.""",
            group_name="oneshottest",
            approval=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-11-29T05:00:00+00:00",
                status="APPROVED",
            ),
            description="Descripción de fuga de información técnica",
            recommendation="""Eliminar el banner de los servicios con fuga de
                información, Verificar que los encabezados HTTP no expongan
                ningún nombre o versión.""",
            unreliable_indicators=dict(
                unreliable_where="192.168.1.9",
                unreliable_newest_vulnerability_report_date=(
                    "2020-09-12T13:45:48+00:00"
                ),
                unreliable_verification_summary=dict(
                    verified=Decimal("0"),
                    requested=Decimal("0"),
                    on_hold=Decimal("0"),
                ),
                unreliable_open_vulnerabilities=Decimal("1"),
                unreliable_treatment_summary=dict(
                    accepted=Decimal("0"),
                    new=Decimal("1"),
                    in_progress=Decimal("0"),
                    accepted_undefined=Decimal("0"),
                ),
                unreliable_oldest_vulnerability_report_date=(
                    "2020-09-12T13:45:48+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    "2020-09-12T13:45:48+00:00"
                ),
                unreliable_closed_vulnerabilities=Decimal("0"),
                unreliable_status="OPEN",
            ),
            title="037. Technical information leak",
            analyst_email="unittest@fluidattacks.com",
            cvss_version="3.1",
            sk="GROUP#oneshottest",
            submission=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-04-08T00:45:11+00:00",
                status="SUBMITTED",
            ),
            id="457497318",
            pk="FIN#457497318",
            state=dict(
                modified_by="integratesmanager@gmail.com",
                justification="NO_JUSTIFICATION",
                source="ASM",
                modified_date="2018-11-29T05:00:00+00:00",
                status="APPROVED",
            ),
            threat="Amenaza.",
            evidences=dict(
                evidence1=dict(
                    modified_date="2018-11-29T05:00:00+00:00",
                    description="Comentario",
                    url="oneshottest-457497318-evidence_route_1",
                ),
                evidence2=dict(
                    modified_date="2018-11-29T05:00:00+00:00",
                    description="Descripcion de prueba",
                    url="oneshottest-457497318-evidence_route_2",
                ),
                evidence3=dict(
                    modified_date="2018-11-29T05:00:00+00:00",
                    description="Descripcion de prueba",
                    url="oneshottest-457497318-evidence_route_3",
                ),
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
        ),
        dict(
            treatment=dict(
                modified_date="2020-09-12T13:45:48+00:00",
                status="NEW",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="oneshottest",
            pk_5="FIN#457497318",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=0,
            ),
            type="PORTS",
            created_by="unittest@fluidattacks.com",
            sk="FIN#457497318",
            sk_3="VULN#afb345f6-9319-416a-b174-0201d7cd3822",
            pk_2="ROOT",
            created_date="2020-09-12T13:45:48+00:00",
            pk="VULN#afb345f6-9319-416a-b174-0201d7cd3822",
            pk_3="USER",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2020-09-12T13:45:48+00:00",
                specific="6666",
                status="OPEN",
                where="192.168.1.9",
            ),
            sk_2="VULN#afb345f6-9319-416a-b174-0201d7cd3822",
        ),
        dict(
            treatment=dict(
                modified_by="integratesuser@gmail.com",
                accepted_until="2021-01-16T17:46:10+00:00",
                assigned="integratesuser@gmail.comm",
                justification="This is a treatment justification test",
                modified_date="2019-01-15T15:43:39+00:00",
                status="ACCEPTED",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#463558592",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=1,
            ),
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#463558592",
            sk_3="VULN#0a848781-b6a4-422e-95fa-692151e6a98e",
            pk_2="ROOT",
            created_date="2019-01-15T15:43:39+00:00",
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98e",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2019-01-15T15:43:39+00:00",
                status="OPEN",
                specific="12",
                where="path/to/file2.exe",
            ),
            sk_2="VULN#0a848781-b6a4-422e-95fa-692151e6a98e",
        ),
        dict(
            treatment=dict(
                modified_date="2019-01-15T15:43:39+00:00",
                status="NEW",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            pk_5="FIN#463558592",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=0,
            ),
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#463558592",
            sk_3="VULN#242f848c-148a-4028-8e36-c7d995502590e",
            pk_2="ROOT",
            created_date="2019-01-15T16:04:14+00:00",
            pk="VULN#242f848c-148a-4028-8e36-c7d995502590",
            pk_3="USER",
            sk_5="VULN#DELETED#false#ZR#false#STATE#closed#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2019-01-15T20:59:16+00:00",
                status="CLOSED",
                specific="123456",
                where="path/to/file2.ext",
            ),
            sk_2="VULN#242f848c-148a-4028-8e36-c7d995502590",
        ),
        dict(
            treatment=dict(
                modified_date="2019-04-12T13:45:48+00:00",
                status="NEW",
            ),
            hacker_email="unittest@fluidattacks.com",
            group_name="oneshottest",
            pk_5="FIN#475041513",
            unreliable_indicators=dict(
                unreliable_reattack_cycles=0,
                unreliable_source="ASM",
                unreliable_efficacy=0,
                unreliable_treatment_changes=0,
            ),
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#475041513",
            sk_3="VULN#a8c0ff07-bb21-4cd5-bb9f-4d716fc69320",
            pk_2="ROOT",
            created_date="2019-04-12T13:45:48+00:00",
            pk="VULN#a8c0ff07-bb21-4cd5-bb9f-4d716fc69320",
            pk_3="USER",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2019-04-12T13:45:48+00:00",
                specific="564",
                where="path/to/file4.ext",
                status="OPEN",
            ),
            sk_2="VULN#a8c0ff07-bb21-4cd5-bb9f-4d716fc69320",
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
                unreliable_treatment_changes=1,
            ),
            type="LINES",
            created_by="unittest@fluidattacks.com",
            sk="FIN#422286126",
            sk_3="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_2="ROOT",
            created_date="2020-01-03T17:46:10+00:00",
            pk="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
            pk_3="USER#integratesuser@gmail.com",
            sk_5="VULN#DELETED#false#ZR#false#STATE#open#VERIF#none",
            state=dict(
                modified_by="unittest@fluidattacks.com",
                source="ASM",
                modified_date="2020-01-03T17:46:10+00:00",
                tool=dict(
                    name="tool-2",
                    impact="INDIRECT",
                ),
                specific="12",
                where="test/data/lib_path/f060/csharp.cs",
                status="OPEN",
            ),
            sk_2="VULN#0a848781-b6a4-422e-95fa-692151e6a98z",
        ),
        dict(
            pk="USER#unittest@fluidattacks.com",
            sk="GROUP#unittesting",
            role="reattacker",
            has_access=True,
            responsibility="Testes",
            group_name="unittesting",
            email="unittest@fluidattacks.com",
        ),
    ]
)


@pytest.fixture(scope="module")
def s3_mock() -> S3Client:  # type: ignore
    """Mocked S3 Fixture."""
    with mock_s3():
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        yield s3_client


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
