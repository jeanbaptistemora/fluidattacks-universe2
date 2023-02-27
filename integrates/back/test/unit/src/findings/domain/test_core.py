from back.test.unit.src.utils import (  # pylint: disable=import-error
    create_dummy_info,
    create_dummy_session,
    get_mock_response,
    get_mocked_path,
    set_mocks_return_values,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
    FindingCommentsRequest,
)
from db_model.findings.enums import (
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerificationSummary,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    add_comment,
    get_last_closed_vulnerability_info,
    get_max_open_severity,
    get_oldest_no_treatment,
    get_pending_verification_findings,
    get_tracking_vulnerabilities,
    get_treatment_summary,
    has_access_to_finding,
    mask_finding,
    verify_vulnerabilities,
)
from findings.types import (
    Tracking,
)
from freezegun import (
    freeze_time,
)
import json
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from newutils.datetime import (
    get_utc_now,
)
import pytest
from pytz import (
    timezone,
)
from settings import (
    TIME_ZONE,
)
import time
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.types import (
    Treatments,
)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    get_mocked_path("finding_vulns_loader.load_many_chained"),
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_last_closed_vulnerability(
    mock_load_many_chained: AsyncMock,
    findings: list,
    findings_data: dict[str, tuple[Finding, ...]],
) -> None:

    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    mock_load_many_chained.return_value = get_mock_response(
        get_mocked_path("finding_vulns_loader.load_many_chained"),
        findings_as_keys,
    )
    loaders = get_new_context()
    (
        vuln_closed_days,
        last_closed_vuln,
    ) = await get_last_closed_vulnerability_info(loaders, findings_loader)
    tzn = timezone(TIME_ZONE)
    actual_date = datetime.now(tz=tzn).date()
    initial_date = datetime(2019, 1, 15).date()
    assert vuln_closed_days == (actual_date - initial_date).days
    expected_id = "242f848c-148a-4028-8e36-c7d995502590"
    assert last_closed_vuln
    assert last_closed_vuln.id == expected_id
    assert last_closed_vuln.finding_id == "463558592"


@patch(get_mocked_path("get_open_vulnerabilities"), new_callable=AsyncMock)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_max_open_severity(
    mock_get_open_vulnerabilities: AsyncMock,
    findings: list,
    findings_data: dict[str, tuple[Finding, ...]],
) -> None:
    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    loaders = get_new_context()
    mock_get_open_vulnerabilities.return_value = get_mock_response(
        get_mocked_path("get_open_vulnerabilities"), findings_as_keys
    )
    test_data = await get_max_open_severity(loaders, findings_loader)
    assert test_data[0] == Decimal(4.3).quantize(Decimal("0.1"))
    result_finding = test_data[1]
    assert result_finding
    assert result_finding.id == "463558592"


async def test_get_pending_verification_findings() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    findings: tuple[Finding, ...] = await get_pending_verification_findings(
        loaders, group_name
    )
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"


@pytest.mark.mymark
async def test_get_tracking_vulnerabilities() -> None:
    loaders = get_new_context()
    finding_vulns_loader = loaders.finding_vulnerabilities_released_nzr
    historic_state_loader = loaders.vulnerability_historic_state
    historic_treatment_loader = loaders.vulnerability_historic_treatment

    finding_id = "436992569"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        Tracking(
            cycle=0,
            open=1,
            closed=0,
            date="2019-08-30",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=1,
            open=15,
            closed=0,
            date="2019-09-12",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=15,
        ),
        Tracking(
            cycle=2,
            open=6,
            closed=0,
            date="2019-09-13",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=6,
        ),
        Tracking(
            cycle=3,
            open=0,
            closed=4,
            date="2019-09-13",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=4,
            vulnerable=0,
        ),
        Tracking(
            cycle=4,
            open=2,
            closed=0,
            date="2019-09-16",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=2,
        ),
    ]
    assert test_data == expected_output

    finding_id = "463461507"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        Tracking(
            cycle=0,
            open=1,
            closed=0,
            date="2019-09-12",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=1,
            open=1,
            closed=0,
            date="2019-09-13",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=2,
            open=0,
            closed=0,
            date="2019-09-13",
            accepted=1,
            accepted_undefined=0,
            assigned="integratesuser@gmail.com",
            justification="accepted justification",
            safe=0,
            vulnerable=0,
        ),
    ]
    assert test_data == expected_output

    finding_id = "422286126"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        Tracking(
            cycle=0,
            open=1,
            closed=0,
            date="2020-01-03",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
    ]
    assert test_data == expected_output

    finding_id = "463558592"
    vulns = await finding_vulns_loader.load(finding_id)
    vulns_state = await historic_state_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    vulns_treatment = await historic_treatment_loader.load_many(
        [vuln.id for vuln in vulns]
    )
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        Tracking(
            cycle=0,
            open=1,
            closed=0,
            date="2019-01-15",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=1,
            open=0,
            closed=1,
            date="2019-01-15",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=1,
            vulnerable=0,
        ),
        Tracking(
            cycle=2,
            open=0,
            closed=0,
            date="2019-01-15",
            accepted=1,
            accepted_undefined=0,
            safe=0,
            vulnerable=0,
            assigned="integratesuser@gmail.com",
            justification="This is a treatment justification test",
        ),
    ]
    assert test_data == expected_output


async def test_has_access_to_finding(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    loaders = get_new_context()
    wrong_data = ["unittest@fluidattacks.com", "000000000"]
    right_data = ["unittest@fluidattacks.com", "422286126"]
    with patch(
        "dynamodb.operations.get_table_resource", new_callable=AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query

        with pytest.raises(FindingNotFound):
            await has_access_to_finding(loaders, wrong_data[0], wrong_data[1])
        with patch(
            "dynamodb.operations.get_resource", new_callable=AsyncMock
        ) as mock_resource:
            mock_resource.return_value.batch_get_item.side_effect = (
                mock_batch_get_item
            )
            assert await has_access_to_finding(
                loaders, right_data[0], right_data[1]
            )


@pytest.mark.changes_db
async def test_add_comment() -> None:
    loaders = get_new_context()
    finding_id = "463461507"
    current_time = get_utc_now()
    comment_id = str(round(time.time() * 1000))
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.COMMENT,
        id=comment_id,
        content="Test comment",
        creation_date=current_time,
        full_name="unittesting",
        parent_id="0",
        email="unittest@fluidattacks.com",
    )
    await add_comment(
        loaders=loaders,
        user_email="unittest@fluidattacks.com",
        comment_data=comment_data,
        finding_id=finding_id,
        group_name="unittesting",
    )
    loaders = get_new_context()
    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_comments[-1].content == "Test comment"
    assert finding_comments[-1].full_name == "unittesting"

    current_time = get_utc_now()
    new_comment_data = comment_data._replace(
        id=str(round(time.time() * 1000)),
        creation_date=current_time,
        parent_id=str(comment_id),
    )
    await add_comment(
        loaders=loaders,
        user_email="unittest@fluidattacks.com",
        comment_data=new_comment_data,
        finding_id=finding_id,
        group_name="unittesting",
    )
    new_loaders = get_new_context()
    new_finding_comments = await new_loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    )
    assert new_finding_comments[-1].content == "Test comment"
    assert new_finding_comments[-1].parent_id == str(comment_id)


@pytest.mark.parametrize(
    ("email", "finding"),
    (
        (
            "unittest@fluidattacks.com",
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="457497316",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-11-27T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="037. Technical information leak",
                approval=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-11-27T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                attack_vector_description="Test description",
                creation=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:43:18+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.CREATED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                description="Descripción de fuga de información técnica",
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=None,
                    evidence2=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Comentario",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_3.png",
                    ),
                    evidence4=None,
                    evidence5=None,
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation="Eliminar el banner de los servicios con "
                "fuga de información, Verificar que los encabezados HTTP "
                "no expongan ningún nombre o versión.",
                requirements="REQ.0077. La aplicación no debe revelar "
                "detalles del sistema interno como stack traces, "
                "fragmentos de sentencias SQL y nombres de base de datos "
                "o tablas. REQ.0176. El sistema debe restringir el acceso "
                "a objetos del sistema que tengan contenido sensible. "
                "Sólo permitirá su acceso a usuarios autorizados.",
                severity=Finding31Severity(
                    attack_complexity=Decimal("0.44"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0.22"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0.22"),
                    confidentiality_requirement=Decimal("1"),
                    exploitability=Decimal("0.94"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.44"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0.22"),
                    modified_confidentiality_impact=Decimal("0.22"),
                    modified_integrity_impact=Decimal("0.22"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.62"),
                    remediation_level=Decimal("0.96"),
                    report_confidence=Decimal("0.92"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.85"),
                ),
                sorts=FindingSorts.NO,
                submission=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.SUBMITTED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                threat="Amenaza.",
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27T19:54:08+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27T19:54:08+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27T19:54:08+00:00"
                    ),
                    unreliable_open_vulnerabilities=0,
                    unreliable_status=FindingStatus.SAFE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=0,
                        in_progress=0,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="",
                ),
                verification=None,
            ),
        ),
    ),
)
@patch(get_mocked_path("findings_model.remove"), new_callable=AsyncMock)
@patch(
    get_mocked_path("vulns_domain.mask_vulnerability"), new_callable=AsyncMock
)
@patch(
    get_mocked_path("loaders.finding_vulnerabilities_all.load"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("remove_all_evidences"), new_callable=AsyncMock)
@patch(
    get_mocked_path("comments_domain.remove_comments"), new_callable=AsyncMock
)
async def test_mask_finding(  # pylint: disable=too-many-arguments
    mock_comments_domain_remove_comments: AsyncMock,
    mock_remove_all_evidences: AsyncMock,
    mock_loaders_finding_vulnerabilities_all: AsyncMock,
    mock_vulns_domain_mask_vulnerability: AsyncMock,
    mock_findings_model_remove: AsyncMock,
    email: str,
    finding: Finding,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_comments_domain_remove_comments,
            mock_remove_all_evidences,
            mock_loaders_finding_vulnerabilities_all,
            mock_vulns_domain_mask_vulnerability,
            mock_findings_model_remove,
        ],
        [
            "comments_domain.remove_comments",
            "remove_all_evidences",
            "loaders.finding_vulnerabilities_all.load",
            "vulns_domain.mask_vulnerability",
            "findings_model.remove",
        ],
        [
            [finding.id],
            [finding.id, finding.group_name],
            [finding.id],
            [email, finding.id],
            [finding.group_name, finding.id],
        ],
    ]
    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )

    loaders = get_new_context()
    await mask_finding(loaders, finding, email)

    assert all(mock_object.called is True for mock_object in mocked_objects)


@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment(
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    group_name = "oneshottest"
    loaders = get_new_context()
    findings = await loaders.group_findings.load(group_name)
    with patch(
        "dynamodb.operations.get_table_resource", new_callable=AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        oldest_findings = await get_oldest_no_treatment(
            loaders, tuple(findings)
        )
    expected_output = {
        "oldest_name": "037. Technical information leak",
        "oldest_age": 256,
    }
    assert expected_output == oldest_findings


@freeze_time("2021-05-27")
async def test_get_treatment_summary(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders = get_new_context()
    finding_id = "475041513"
    with patch(
        "dynamodb.operations.get_table_resource", new_callable=AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        oldest_findings = await get_treatment_summary(loaders, finding_id)
    expected_output = Treatments(
        accepted=0,
        accepted_undefined=0,
        in_progress=0,
        untreated=1,
    )
    assert expected_output == oldest_findings


@pytest.mark.changes_db
async def test_verify_vulnerabilities() -> None:
    finding_id = "436992569"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    user_info = {
        "first_name": "Miguel",
        "last_name": "de Orellana",
        "user_email": "unittest@fluidattacks.com",
    }
    justification = "Vuln verified"
    open_vulns_ids = ["587c40de-09a0-4d85-a9f9-eaa46aa895d7"]
    closed_vulns_ids: list[str] = []
    await verify_vulnerabilities(
        context=info.context,
        finding_id=finding_id,
        user_info=user_info,
        justification=justification,
        open_vulns_ids=open_vulns_ids,
        closed_vulns_ids=closed_vulns_ids,
        vulns_to_close_from_file=[],
        loaders=info.context.loaders,
    )
    loaders = get_new_context()
    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_comments[-1].finding_id == finding_id
    assert finding_comments[-1].full_name == "Miguel de Orellana"
    assert finding_comments[-1].comment_type == CommentType.VERIFICATION
    assert finding_comments[-1].content[-13:] == "Vuln verified"
