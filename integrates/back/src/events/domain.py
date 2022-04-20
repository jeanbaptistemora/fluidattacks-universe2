"""Domain functions for events."""  # pylint:disable=cyclic-import

from aioextensions import (
    collect,
    schedule,
)
import authz
from comments import (
    domain as comments_domain,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventNotFound,
    InvalidCommentParent,
    InvalidDate,
    InvalidFileSize,
    InvalidFileType,
    InvalidParameter,
    NoHoldRequested,
    VulnNotFound,
)
from custom_types import (
    AddEventPayload,
    Comment as CommentType,
    Event as EventType,
)
from datetime import (
    date as date_type,
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    FindingVerification,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from events import (
    dal as events_dal,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
from mailer import (
    events as events_mail,
)
from newutils import (
    datetime as datetime_utils,
    events as events_utils,
    files as files_utils,
    token as token_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
import pytz  # type: ignore
import random
from settings import (
    LOGGING,
    TIME_ZONE,
)
from starlette.datastructures import (
    UploadFile,
)
from time import (
    time,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from users import (
    domain as users_domain,
)
from vulnerabilities import (
    domain as vulns_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    event_id: str,
    parent_comment: str,
) -> Tuple[Union[str, None], bool]:
    parent_comment = str(parent_comment)
    content = str(comment_data["content"])
    event_loader = info.context.loaders.event
    event = await event_loader.load(event_id)
    group_name = get_key_or_fallback(event)

    await authz.validate_handle_comment_scope(
        content, user_email, group_name, parent_comment, info.context.store
    )
    if parent_comment != "0":
        event_comments = [
            comment["comment_id"]
            for comment in await comments_domain.get("event", event_id)
        ]
        if parent_comment not in event_comments:
            raise InvalidCommentParent()
    user_data = await users_domain.get(user_email)
    user_data["user_email"] = user_data.pop("email")
    success = await comments_domain.add(event_id, comment_data, user_data)
    return success


async def add_event(  # pylint: disable=too-many-locals
    loaders: Any,
    hacker_email: str,
    group_name: str,
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    **kwargs: Any,
) -> AddEventPayload:
    validations.validate_fields([kwargs["detail"], kwargs["root_id"]])
    validations.validate_field_length(kwargs["detail"], 300)

    event_id = str(random.randint(10000000, 170000000))  # nosec
    tzn = pytz.timezone(TIME_ZONE)
    today = datetime_utils.get_now()

    group: Group = await loaders.group_typed.load(group_name)
    subscription = group.state.type
    org_id = await orgs_domain.get_id_by_name(group.organization_name)

    root: RootItem = await loaders.root.load((group_name, kwargs["root_id"]))
    if root.state.status != "ACTIVE":
        raise InvalidParameter()

    event_attrs = kwargs.copy()
    event_date = event_attrs.pop("event_date").astimezone(tzn)
    if event_date > today:
        raise InvalidDate()

    event_attrs.update(
        {
            "accessibility": " ".join(list(set(event_attrs["accessibility"]))),
            "analyst": hacker_email,
            "client": org_id,
            "historic_state": [
                {
                    "analyst": hacker_email,
                    "date": datetime_utils.get_as_str(event_date),
                    "state": "OPEN",
                },
                {
                    "analyst": hacker_email,
                    "date": datetime_utils.get_as_str(today),
                    "state": "CREATED",
                },
            ],
            "root_id": root.id,
            "subscription": subscription.value,
        }
    )
    if "affected_components" in event_attrs:
        event_attrs["affected_components"] = "\n".join(
            list(set(event_attrs["affected_components"]))
        )

    valid_files: bool = True
    if file:
        valid_files = valid_files and await validate_evidence(
            "evidence_file", file
        )
    if image:
        valid_files = valid_files and await validate_evidence(
            "evidence", image
        )

    success: bool = False
    if valid_files:
        success = await events_dal.create(event_id, group_name, event_attrs)

    if success:
        if file:
            await update_evidence(event_id, "evidence_file", file, event_date)
        if image:
            await update_evidence(event_id, "evidence", image, event_date)

    event_type = event_attrs["event_type"]
    description = event_attrs["detail"]
    report_date: date_type = datetime_utils.get_date_from_iso_str(
        event_attrs["historic_state"][0]["date"]
    )
    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            event_type=event_type,
            description=description,
            report_date=report_date,
        )
    )

    return AddEventPayload(event_id, success)


async def get_event(event_id: str) -> EventType:
    event = await events_dal.get_event(event_id)
    if not event:
        raise EventNotFound()
    return events_utils.format_data(event)


async def get_events(event_ids: List[str]) -> List[EventType]:
    return cast(
        List[EventType],
        await collect(get_event(event_id) for event_id in event_ids),
    )


async def get_unsolved_events(group_name: str) -> List[str]:
    events_list = await list_group_events(group_name)
    events = await get_events(events_list)
    unsolved: List[EventType] = [
        event
        for event in events
        if event["historic_state"][-1]["state"] == "CREATED"
    ]
    return unsolved


async def get_evidence_link(event_id: str, file_name: str) -> str:
    event = await get_event(event_id)
    group_name = get_key_or_fallback(event)
    file_url = f"{group_name}/{event_id}/{file_name}"
    return await events_dal.sign_url(file_url)


async def has_access_to_event(email: str, event_id: str) -> bool:
    """Verify if the user has access to a event submission."""
    event = await get_event(event_id)
    group = cast(str, get_key_or_fallback(event, fallback=""))
    return bool(await authz.has_access_to_group(email, group))


async def list_group_events(group_name: str) -> List[str]:
    return await events_dal.list_group_events(group_name)


async def mask(event_id: str) -> bool:
    event = await events_dal.get_event(event_id)
    attrs_to_mask = [
        "client",
        "detail",
        "evidence",
        "evidence_date",
        "evidence_file",
        "evidence_file_date",
    ]

    mask_events_coroutines = [
        events_dal.update(event_id, {attr: "Masked" for attr in attrs_to_mask})
    ]

    list_comments = await comments_domain.get("event", event_id)
    mask_events_coroutines.extend(
        [
            comments_domain.delete(str(comment["comment_id"]), event_id)
            for comment in list_comments
        ]
    )

    group_name = str(get_key_or_fallback(event, fallback=""))
    evidence_prefix = f"{group_name}/{event_id}"
    list_evidences = await events_dal.search_evidence(evidence_prefix)
    # These coroutines return none instead of bool
    mask_events_coroutines_none = [
        events_dal.remove_evidence(file_name) for file_name in list_evidences
    ]

    await collect(mask_events_coroutines_none)
    return all(await collect(mask_events_coroutines))


async def remove_evidence(evidence_type: str, event_id: str) -> bool:
    event = await get_event(event_id)
    group_name = get_key_or_fallback(event)

    full_name = f"{group_name}/{event_id}/{event[evidence_type]}"
    await events_dal.remove_evidence(full_name)
    return await events_dal.update(
        event_id, {evidence_type: None, f"{evidence_type}_date": None}
    )


async def solve_event(  # pylint: disable=too-many-locals
    info: GraphQLResolveInfo,
    event_id: str,
    affectation: str,
    hacker_email: str,
    date: datetime,
) -> bool:
    event = await get_event(event_id)
    success = False
    loaders = info.context.loaders
    group_name = str(get_key_or_fallback(event, fallback=""))

    if (
        cast(List[Dict[str, str]], event.get("historic_state", []))[-1].get(
            "state"
        )
        == "SOLVED"
    ):
        raise EventAlreadyClosed()

    affected_reattacks: Tuple[
        Vulnerability, ...
    ] = await loaders.event_vulnerabilities_loader.load((event_id))
    if len(affected_reattacks) > 0:
        user_info = await token_utils.get_jwt_content(info.context)
        reattacks_dict: Dict[str, Set[str]] = {}
        for vuln in affected_reattacks:
            reattacks_dict.setdefault(vuln.finding_id, set()).add(vuln.id)

        for finding_id, hold_ids in reattacks_dict.items():
            await findings_domain.request_vulnerabilities_verification(
                loaders=loaders,
                finding_id=finding_id,
                user_info=user_info,
                justification=(
                    f"Event #{event_id} was solved. The reattacks are back to "
                    "the Requested stage."
                ),
                vulnerability_ids=hold_ids,
                is_closing_event=True,
            )

    event_type = str(event["event_type"])
    description = str(event["detail"])
    report_date: date_type = datetime_utils.get_date_from_iso_str(
        event["historic_state"][0]["date"]
    )
    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            event_type=event_type,
            description=description,
            is_closed=True,
            report_date=report_date,
        )
    )

    today = datetime_utils.get_now()
    history = cast(List[Dict[str, str]], event.get("historic_state", []))
    history += [
        {
            "analyst": hacker_email,
            "date": datetime_utils.get_as_str(date),
            "state": "CLOSED",
        },
        {
            "affectation": affectation,
            "analyst": hacker_email,
            "date": datetime_utils.get_as_str(today),
            "state": "SOLVED",
        },
    ]
    success = await events_dal.update(event_id, {"historic_state": history})
    return success


async def update_evidence(
    event_id: str,
    evidence_type: str,
    file: UploadFile,
    update_date: datetime,
) -> bool:
    event = await get_event(event_id)
    if (
        cast(List[Dict[str, str]], event.get("historic_state", []))[-1].get(
            "state"
        )
        == "SOLVED"
    ):
        raise EventAlreadyClosed()

    group_name = str(get_key_or_fallback(event, fallback=""))
    extension = {
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
    }.get(file.content_type, "")
    evidence_id = f"{group_name}-{event_id}-{evidence_type}{extension}"
    full_name = f"{group_name}/{event_id}/{evidence_id}"

    await events_dal.save_evidence(file, full_name)
    return await events_dal.update(
        event_id,
        {
            evidence_type: evidence_id,
            f"{evidence_type}_date": datetime_utils.get_as_str(update_date),
        },
    )


async def validate_evidence(evidence_type: str, file: UploadFile) -> bool:
    mib = 1048576
    success = False
    validations.validate_file_name(file.filename)
    validations.validate_fields([file.content_type])

    if evidence_type == "evidence":
        allowed_mimes = ["image/gif", "image/jpeg", "image/png"]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_IMAGE")
    else:
        allowed_mimes = [
            "application/csv",
            "application/pdf",
            "application/zip",
            "text/csv",
            "text/plain",
        ]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_FILE")

    if await files_utils.get_file_size(file) < 10 * mib:
        success = True
    else:
        raise InvalidFileSize()
    return success


async def request_vulnerabilities_hold(
    loaders: Any,
    finding_id: str,
    event_id: str,
    user_info: Dict[str, str],
    vulnerability_ids: Set[str],
) -> None:
    justification: str = (
        f"These reattacks have been put on hold because of Event #{event_id}"
    )
    finding: Finding = await loaders.finding.load(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    vulnerabilities = [
        vulns_utils.validate_requested_hold(vuln) for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    user_email = str(user_info["user_email"])
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        status=FindingVerificationStatus.ON_HOLD,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    success = all(
        await collect(
            vulns_domain.request_hold(event_id, vuln)
            for vuln in vulnerabilities
        )
    )
    comment_data: CommentType = {
        "comment_type": "verification",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    await comments_domain.add(finding_id, comment_data, user_info)
    if not success:
        LOGGER.error("An error occurred requesting hold")
        raise NoHoldRequested()
