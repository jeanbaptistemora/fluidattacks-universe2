# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
    get_mock_response,
    get_mocked_path,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
    FindingCommentsRequest,
)
from db_model.findings.types import (
    Finding,
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
    Dict,
    List,
    Tuple,
)
from unittest import (
    mock,
)
from vulnerabilities.types import (
    Treatments,
)

pytestmark = [
    pytest.mark.asyncio,
]


@mock.patch(
    get_mocked_path("finding_vulns_loader.load_many_chained"),
    new_callable=mock.AsyncMock,
)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_last_closed_vulnerability(
    mock_load_many_chained: mock.AsyncMock,
    findings: List,
    findings_data: Dict[str, Tuple[Finding, ...]],
) -> None:

    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    mock_load_many_chained.return_value = get_mock_response(
        get_mocked_path("finding_vulns_loader.load_many_chained"),
        findings_as_keys,
    )
    loaders: Dataloaders = get_new_context()
    (
        vuln_closed_days,
        last_closed_vuln,
    ) = await get_last_closed_vulnerability_info(loaders, findings_loader)
    tzn = timezone(TIME_ZONE)
    actual_date = datetime.now(tz=tzn).date()
    initial_date = datetime(2019, 1, 15).date()
    assert vuln_closed_days == (actual_date - initial_date).days
    expected_id = "242f848c-148a-4028-8e36-c7d995502590"
    assert last_closed_vuln.id == expected_id  # type: ignore
    assert last_closed_vuln.finding_id == "463558592"  # type: ignore


@mock.patch(
    get_mocked_path("get_open_vulnerabilities"), new_callable=mock.AsyncMock
)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_max_open_severity(
    mock_get_open_vulnerabilities: mock.AsyncMock,
    findings: List,
    findings_data: Dict[str, Tuple[Finding, ...]],
) -> None:
    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    loaders = get_new_context()
    mock_get_open_vulnerabilities.return_value = get_mock_response(
        get_mocked_path("get_open_vulnerabilities"), findings_as_keys
    )
    test_data = await get_max_open_severity(loaders, findings_loader)
    assert test_data[0] == Decimal(4.3).quantize(Decimal("0.1"))
    assert test_data[1].id == "463558592"  # type: ignore


async def test_get_pending_verification_findings() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await get_pending_verification_findings(
        loaders, group_name
    )
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"


@pytest.mark.mymark
async def test_get_tracking_vulnerabilities() -> None:
    loaders: Dataloaders = get_new_context()
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
            effectiveness=None,
            new=None,
            in_progress=None,
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
            effectiveness=None,
            new=None,
            in_progress=None,
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
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query

        with pytest.raises(FindingNotFound):
            await has_access_to_finding(loaders, wrong_data[0], wrong_data[1])
        with mock.patch(
            "dynamodb.operations.get_resource", new_callable=mock.AsyncMock
        ) as mock_resource:
            mock_resource.return_value.batch_get_item.side_effect = (
                mock_batch_get_item
            )
            assert await has_access_to_finding(
                loaders, right_data[0], right_data[1]
            )


@pytest.mark.changes_db
async def test_add_comment() -> None:
    loaders: Dataloaders = get_new_context()
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
        loaders,
        "unittest@fluidattacks.com",
        comment_data,
        finding_id,
        "unittesting",
    )
    loaders = get_new_context()
    finding_comments: tuple[
        FindingComment, ...
    ] = await loaders.finding_comments.load(
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
        loaders,
        "unittest@fluidattacks.com",
        new_comment_data,
        finding_id,
        "unittesting",
    )
    new_loaders = get_new_context()
    new_finding_comments: tuple[
        FindingComment, ...
    ] = await new_loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    )
    assert new_finding_comments[-1].content == "Test comment"
    assert new_finding_comments[-1].parent_id == str(comment_id)


@pytest.mark.changes_db
async def test_mask_finding() -> None:
    finding_id = "475041524"
    email = "unittest@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    await mask_finding(loaders, finding, email)
    loaders.finding.clear(finding_id)
    with pytest.raises(FindingNotFound):
        await loaders.finding.load(finding_id)


@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment(
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    group_name = "oneshottest"
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        oldest_findings = await get_oldest_no_treatment(loaders, findings)
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
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        oldest_findings = await get_treatment_summary(loaders, finding_id)
    expected_output = Treatments(
        accepted=0,
        accepted_undefined=0,
        in_progress=0,
        new=1,
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
    closed_vulns_ids: List[str] = []
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
    finding_commets: tuple[
        FindingComment, ...
    ] = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_commets[-1].finding_id == finding_id
    assert finding_commets[-1].full_name == "Miguel de Orellana"
    assert finding_commets[-1].comment_type == CommentType.VERIFICATION
    assert finding_commets[-1].content[-13:] == "Vuln verified"
