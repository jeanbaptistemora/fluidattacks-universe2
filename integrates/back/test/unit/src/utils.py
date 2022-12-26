from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.enums import (
    Source,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessState,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderSessionToken,
    StakeholderState,
    StakeholderTours,
    StateSessionType,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from graphql import (
    GraphQLResolveInfo,
)
import json
from requests import (
    Request,
)
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from settings import (
    JWT_COOKIE_NAME,
    SESSION_COOKIE_AGE,
)
from typing import (
    Any,
    Dict,
    Optional,
)
import uuid

mocked_paths: Dict[str, str] = {
    "authz.validate_handle_comment_scope": "authz.validate_handle_comment_scope",  # noqa: E501
    "dynamodb_ops.delete_item": "dynamodb.operations_legacy.delete_item",
    "dynamodb_ops.query": "dynamodb.operations_legacy.query",
    "findings_storage.download_evidence": "findings.storage.download_evidence",  # noqa: E501
    "findings_storage.search_evidence": "findings.storage.search_evidence",
    "finding_vulns_loader.load_many_chained": "db_model.vulnerabilities.get.FindingVulnerabilitiesNonZeroRiskLoader.load_many_chained",  # noqa: E501
    "get_open_vulnerabilities": "findings.domain.core.get_open_vulnerabilities",  # noqa: E501
    "group_access_model.update_metadata": "db_model.group_access.update_metadata",  # noqa: E501
    "group_comments_model.add": "db_model.group_comments.add",
    "loaders.group_access.load": "db_model.group_access.get.GroupAccessLoader.load",  # noqa: E501
    "get_user_level_role": "authz.policy.get_user_level_role",
    "loaders.stakeholder.load": "db_model.stakeholders.get.StakeholderLoader.load",  # noqa: E501
    "loaders.stakeholder_with_fallback.load": "db_model.stakeholders.get.StakeholderWithFallbackLoader.load",  # noqa: E501
    "stakeholders_model.update_metadata": "db_model.stakeholders.update_metadata",  # noqa: E501
    "s3_ops.list_files": "s3.operations.list_files",
    "s3_ops.remove_file": "s3.operations.remove_file",
    "s3_ops.upload_memory_file": "s3.operations.upload_memory_file",
}

mocked_responses: Dict[str, Dict[str, Any]] = {
    "authz.policy.get_user_level_role": {
        '["integrateshacker@fluidattacks.com"]': "hacker",
        '["integratesuser@gmail.com"]': "user_manager",
        '["test_admin@gmail.com"]': "admin",
        '["test_email@gmail.com"]': "",
        '["unittest@fluidattacks.com"]': "admin",
    },
    "authz.validate_handle_comment_scope": {
        '["Test comment", "unittest@fluidattacks.com",'
        ' "unittesting", "0"]': None,
    },
    "db_model.group_access.get.GroupAccessLoader.load": {
        '["integrateshacker@fluidattacks.com", "unittesting",'
        ' "hacker"]': GroupAccess(
            email="integrateshacker@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="hacker",
        ),
        '["integratesuser@gmail.com", "unittesting",'
        ' "user_manager"]': GroupAccess(
            email="integratesuser@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user_manager",
        ),
        '["test_admin@gmail.com", "unittesting", "admin"]': GroupAccess(
            email="test_admin@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=None,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["test_email@gmail.com", "unittesting", ""]': GroupAccess(
            email="test_email@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=None,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["unittest@fluidattacks.com", "unittesting", "admin"]': GroupAccess(
            email="unittest@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="admin",
        ),
    },
    "db_model.group_access.update_metadata": {
        '["integrateshacker@fluidattacks.com", "unittesting"]': None,
        '["integratesuser@gmail.com", "unittesting"]': None,
    },
    "db_model.group_comments.add": {
        '[["unittesting", "1672083646257", "0", "2022-04-06 16:46:23+00:00",'
        ' "Test comment", "unittest@fluidattacks.com", "unittesting"]]': None,
    },
    "db_model.stakeholders.get.StakeholderWithFallbackLoader.load": {
        '["integrateshacker@fluidattacks.com"]': Stakeholder(
            email="integrateshacker@fluidattacks.com",
            access_token=None,
            first_name="Ismael",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Rivera",
            legal_remember=False,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integratesuser@gmail.com"]': Stakeholder(
            email="integratesuser@gmail.com",
            access_token=None,
            first_name="Jane",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Doe",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="30044445556",
            ),
            role="user",
            session_key=None,
            session_token=StakeholderSessionToken(
                jti="0f98c8d494be2c9eddd973e4a861483988a1d90bb26"
                "8be48dfc442d0b4cada72",
                state=StateSessionType.IS_VALID,
            ),
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
    },
    "db_model.vulnerabilities.get.FindingVulnerabilitiesNonZeroRiskLoader.load_many_chained": {  # noqa: E501
        '["463558592", "422286126"]': tuple(
            (
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98e",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file2.exe",
                        commit=None,
                        justification=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.comm",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="242f848c-148a-4028-8e36-c7d995502590",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="123456",
                        status=VulnerabilityStateStatus.SAFE,
                        where="path/to/file2.ext",
                        commit=None,
                        justification=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.NEW,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit=None,
                        justification=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            )
        )
    },
    "db_model.stakeholders.get.StakeholderLoader.load": {
        '["continuoushacking@gmail.com", "hacker"]': Stakeholder(
            email="continuoushacking@gmail.com",
            access_token=None,
            first_name="Jhon",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Hackeroy",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="continuoushacking@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integrateshacker@fluidattacks.com", "hacker"]': Stakeholder(
            email="integrateshacker@fluidattacks.com",
            access_token=None,
            first_name="Ismael",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Rivera",
            legal_remember=False,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integratesuser@gmail.com", "user"]': Stakeholder(
            email="integratesuser@gmail.com",
            access_token=None,
            first_name="Jane",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Doe",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="30044445556",
            ),
            role="user",
            session_key=None,
            session_token=StakeholderSessionToken(
                jti="0f98c8d494be2c9eddd973e4a861483988a1d90bb26"
                "8be48dfc442d0b4cada72",
                state=StateSessionType.IS_VALID,
            ),
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["unittest@fluidattacks.com", "admin"]': Stakeholder(
            email="unittest@fluidattacks.com",
            access_token=StakeholderAccessToken(
                iat=1634677195,
                jti="c8d9d5f095958cf200f7435508fc2dba37d07447ec12dcd0"
                "70808418d640e77d",
                salt="27c7f388ccdd7cc432871c84b63e78cd716739c40055253c"
                "e7ad1666a8532db6",
            ),
            first_name="Miguel",
            is_concurrent_session=False,
            is_registered=True,
            last_name="de Orellana",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3006007008",
            ),
            role="admin",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
    },
    "dynamodb.operations_legacy.delete_item": {
        '["44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f6'
        '52110"]': True,
    },
    "dynamodb.operations_legacy.query": {
        '["ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a"]': [  # noqa: E501
            dict(
                additional_info=json.dumps(
                    dict(
                        report_type="XLS",
                        treatments=["ACCEPTED", "NEW"],
                        states=["OPEN"],
                        verifications=["REQUESTED"],
                        closing_date="null",
                        finding_title="038",
                        age=1100,
                        min_severity="2.7",
                        max_severity="null",
                    )
                ),
                subject="unittesting@fluidattacks.com",
                action_name="report",
                pk="ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a",  # noqa: E501
                time="1616116348",
                entity="unittesting",
                queue="small",
            )
        ],
        '["049ee0097a137f2961578929a800a5f23f93f59806b901ee3324abf6eb5a4828"]': [],  # noqa: E501
    },
    "findings.storage.search_evidence": {
        '["unittesting", "422286126",'
        ' "unittesting-422286126-evidence_route_1.png"]': [
            {
                "ResponseMetadata": {
                    "HTTPStatusCode": 200,
                    "HTTPHeaders": {},
                    "RetryAttempts": 0,
                },
                "IsTruncated": False,
                "Contents": [
                    {
                        "Key": "evidences/unittesting/422286126/"
                        "unittesting-422286126-evidence_file.csv",
                        "LastModified": "2019-01-15T15:43:39+00:00",
                        "ETag": '"a008e27edeaaf560cc01ef094edbbd65"',
                        "Size": 132,
                        "StorageClass": "STANDARD",
                    },
                    {
                        "Key": "evidences/unittesting/422286126/"
                        "unittesting-422286126-evidence_route_1.png",
                        "LastModified": "2020-01-03T17:46:10+00:00",
                        "ETag": '"98a8fa986a52960e0ae1e990afd06510"',
                        "Size": 16629,
                        "StorageClass": "STANDARD",
                    },
                ],
                "Name": "integrates.somedeveloperatfluid",
                "Prefix": "",
                "MaxKeys": 1000,
                "KeyCount": 2,
            }
        ]
    },
    "findings.storage.download_evidence": {
        '["unittesting", "422286126",'
        ' "unittesting-422286126-evidence_route_1.png"]': None,
    },
    "findings.domain.core.get_open_vulnerabilities": {
        '["463558592", "422286126"]': 1
    },
    "db_model.stakeholders.update_metadata": {
        '["integrateshacker@fluidattacks.com"]': None,
        '["integratesuser@gmail.com"]': None,
        '["test_email@test.com", "user"]': None,
        '["test_email@test.com", "admin"]': None,
    },
    "s3.operations.list_files": {
        '["billing-test-file.png"]': ["billing-test-file.png"],
        '["unittesting-test-file.csv"]': ["unittesting-test-file.csv"],
    },
    "s3.operations.remove_file": {
        '["billing-test-file.png"]': None,
        '["unittesting-test-file.csv"]': None,
    },
    "s3.operations.upload_memory_file": {
        '["billing-test-file.png"]': None,
        '["unittesting-test-file.csv"]': None,
    },
}


def create_dummy_simple_session(
    username: str = "unittest",
) -> Request:
    request = Request("GET", "/")
    request = apply_context_attrs(request)  # type: ignore
    setattr(
        request,
        "session",
        dict(username=username, session_key=str(uuid.uuid4())),
    )
    setattr(request, "cookies", {})

    return request


async def create_dummy_session(
    username: str = "unittest", session_jwt: Optional[str] = None
) -> Request:
    request = create_dummy_simple_session(username)
    jti = sessions_utils.calculate_hash_token()["jti"]
    expiration_time = int(
        (datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)).timestamp()
    )
    payload = {
        "user_email": username,
        "first_name": "unit",
        "last_name": "test",
        "jti": jti,
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    if session_jwt:
        request.headers["Authorization"] = f"Bearer {session_jwt}"
    else:
        request.cookies[JWT_COOKIE_NAME] = token
        # do not use me query to validate if an stakeholder
        # has been removed because update_metadata will create that user
        await stakeholders_model.update_metadata(
            email=username,
            metadata=StakeholderMetadataToUpdate(
                session_token=StakeholderSessionToken(
                    jti=jti, state=StateSessionType.IS_VALID
                )
            ),
        )
    return request


def create_dummy_info(request: Request) -> GraphQLResolveInfo:
    return GraphQLResolveInfo(
        field_name=None,  # type: ignore
        field_nodes=None,  # type: ignore
        return_type=None,  # type: ignore
        parent_type=None,  # type: ignore
        path=None,  # type: ignore
        schema=None,  # type: ignore
        fragments=None,  # type: ignore
        root_value=None,
        operation=None,  # type: ignore
        variable_values=None,  # type: ignore
        context=request,
        is_awaitable=None,  # type: ignore
    )


def get_mock_response(used_mock: str, parameters: str) -> Any:
    return mocked_responses[used_mock][parameters]


def get_mocked_path(mocked_object: str) -> str:
    return mocked_paths[mocked_object]
