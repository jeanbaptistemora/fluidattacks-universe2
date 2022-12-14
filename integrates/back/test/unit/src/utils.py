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
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
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
    "finding_vulns_loader.load_many_chained": "db_model.vulnerabilities.get.FindingVulnerabilitiesNonZeroRiskLoader.load_many_chained",  # noqa: E501
    "get_open_vulnerabilities": "findings.domain.core.get_open_vulnerabilities",  # noqa: E501
}

mocked_responses: Dict[str, Dict[str, Any]] = {
    "db_model.vulnerabilities.get.FindingVulnerabilitiesNonZeroRiskLoader.load_many_chained": {  # noqa: E501
        '["463558592", "422286126"]': tuple(
            (
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date="2019-01-15T15:43:39+00:00",
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98e",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2019-01-15T15:43:39+00:00",
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.OPEN,
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
                        modified_date="2019-01-15T15:43:39+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until="2021-01-16T17:46:10+00:00",
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
                    created_date="2019-01-15T16:04:14+00:00",
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="242f848c-148a-4028-8e36-c7d995502590",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2019-01-15T20:59:16+00:00",
                        source=Source.ASM,
                        specific="123456",
                        status=VulnerabilityStateStatus.CLOSED,
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
                        modified_date="2019-01-15T15:43:39+00:00",
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
                    created_date="2020-01-03T17:46:10+00:00",
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date="2020-01-03T17:46:10+00:00",
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.OPEN,
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
                        modified_date="2020-01-03T17:46:10+00:00",
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
    "findings.domain.core.get_open_vulnerabilities": {
        '["463558592", "422286126"]': 1
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
