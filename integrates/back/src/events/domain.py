# pylint:disable=cyclic-import
from . import (
    validations as events_validations,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from collections import (
    defaultdict,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventHasNotBeenSolved,
    EventVerificationAlreadyRequested,
    EventVerificationNotRequested,
    InvalidCommentParent,
    InvalidDate,
    InvalidEventSolvingReason,
    InvalidFileSize,
    InvalidFileType,
    InvalidParameter,
    RequiredFieldToBeUpdate,
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    events as events_model,
    findings as findings_model,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.enums import (
    EventEvidenceId,
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventMetadataToUpdate,
    EventState,
    GroupEventsRequest,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
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
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.types import (
    Root,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from event_comments import (
    domain as event_comments_domain,
)
from events.constants import (
    FILE_EVIDENCE_IDS,
    IMAGE_EVIDENCE_IDS,
    SOLUTION_REASON_BY_EVENT_TYPE,
)
from events.types import (
    EventAttributesToUpdate,
)
from finding_comments import (
    domain as finding_comments_domain,
)
from findings import (
    domain as findings_domain,
)
from findings.domain.evidence import (
    validate_evidencename,
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
    files as files_utils,
    validations,
    vulnerabilities as vulns_utils,
)
import pytz
import random
from s3 import (
    operations as s3_ops,
)
from sessions import (
    domain as sessions_domain,
)
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
    DefaultDict,
    Optional,
    Union,
)
from vulnerabilities import (
    domain as vulns_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def save_evidence(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"evidences/{file_name}",
    )


async def search_evidence(file_name: str) -> list[str]:
    return await s3_ops.list_files(f"evidences/{file_name}")


async def remove_file_evidence(file_name: str) -> None:
    await s3_ops.remove_file(file_name)


async def add_comment(
    loaders: Dataloaders,
    comment_data: EventComment,
    email: str,
    event_id: str,
    parent_comment: str,
) -> None:
    parent_comment = str(parent_comment)
    content = comment_data.content
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name

    validations.validate_field_length(content, 20000)
    await authz.validate_handle_comment_scope(
        loaders, content, email, group_name, parent_comment
    )
    if parent_comment != "0":
        event_comments: tuple[
            EventComment, ...
        ] = await loaders.event_comments.load(event_id)
        event_comments_ids = [comment.id for comment in event_comments]
        if parent_comment not in event_comments_ids:
            raise InvalidCommentParent()
    await event_comments_domain.add(loaders, comment_data, group_name)


async def add_event(
    loaders: Dataloaders,
    hacker_email: str,
    group_name: str,
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    **kwargs: Any,
) -> str:
    validations.validate_fields([kwargs["detail"], kwargs["root_id"]])
    validations.validate_field_length(kwargs["detail"], 300)
    events_validations.validate_type(EventType[kwargs["event_type"]])
    root_id: Optional[str] = kwargs.get("root_id")
    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    if root_id:
        root: Root = await loaders.root.load((group_name, root_id))
        root_id = root.id
        if root.state.status != "ACTIVE":
            raise InvalidParameter(field="rootId")
    if file:
        await validate_evidence(
            group_name=group.name.lower(),
            organization_name=organization.name.lower(),
            evidence_id=EventEvidenceId.FILE_1,
            file=file,
        )
    if image:
        await validate_evidence(
            group_name=group.name.lower(),
            organization_name=organization.name.lower(),
            evidence_id=EventEvidenceId.IMAGE_1,
            file=image,
        )

    tzn = pytz.timezone(TIME_ZONE)
    event_date: datetime = kwargs["event_date"].astimezone(tzn)
    if event_date > datetime_utils.get_now():
        raise InvalidDate()

    created_date = datetime_utils.get_utc_now()
    event = Event(
        client=group.organization_id,
        created_by=hacker_email,
        created_date=created_date,
        description=kwargs["detail"],
        event_date=event_date,
        evidences=EventEvidences(),
        group_name=group_name,
        hacker=hacker_email,
        id=str(random.randint(10000000, 170000000)),  # nosec
        root_id=root_id,
        state=EventState(
            modified_by=hacker_email,
            modified_date=event_date,
            status=EventStateStatus.OPEN,
        ),
        type=EventType[kwargs["event_type"]],
    )
    await events_model.add(event=event)
    await events_model.update_state(
        current_value=event,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=created_date,
            status=EventStateStatus.CREATED,
        ),
    )

    if file:
        await update_evidence(
            loaders, event.id, EventEvidenceId.FILE_1, file, event_date
        )
    if image:
        await update_evidence(
            loaders, event.id, EventEvidenceId.IMAGE_1, image, event_date
        )

    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event.id,
            event_type=event.type,
            description=event.description,
            root_id=event.root_id,
            report_date=event.event_date.date(),
        )
    )

    return event.id


async def get_unsolved_events(
    loaders: Dataloaders, group_name: str
) -> list[Event]:
    events: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    unsolved: list[Event] = [
        event
        for event in events
        if event.state.status == EventStateStatus.CREATED
    ]
    return unsolved


async def get_evidence_link(
    loaders: Dataloaders, event_id: str, file_name: str
) -> str:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    file_url = f"evidences/{group_name}/{event_id}/{file_name}"
    return await s3_ops.sign_url(file_url, 10)


async def get_solving_state(
    loaders: Dataloaders, event_id: str
) -> Optional[EventState]:
    historic_states: tuple[
        EventState, ...
    ] = await loaders.event_historic_state.load(event_id)
    for state in sorted(
        historic_states,
        key=lambda state: state.modified_date,
    ):
        if state.status == EventStateStatus.SOLVED:
            return state

    return None


async def get_solving_date(
    loaders: Dataloaders, event_id: str
) -> Optional[datetime]:
    """Returns the date of the last closing state."""
    last_closing_state = await get_solving_state(loaders, event_id)

    return last_closing_state.modified_date if last_closing_state else None


async def has_access_to_event(
    loaders: Dataloaders, email: str, event_id: str
) -> bool:
    """Verify if the user has access to a event submission."""
    event: Event = await loaders.event.load(event_id)
    return await authz.has_access_to_group(loaders, email, event.group_name)


async def remove_event(event_id: str, group_name: str) -> None:
    evidence_prefix = f"{group_name}/{event_id}"
    list_evidences = await search_evidence(evidence_prefix)
    await collect(
        [
            *[remove_file_evidence(file_name) for file_name in list_evidences],
            event_comments_domain.remove_comments(event_id),
        ]
    )
    await events_model.remove(event_id=event_id)


async def remove_evidence(
    loaders: Dataloaders, evidence_id: EventEvidenceId, event_id: str
) -> None:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name

    if (
        evidence := getattr(
            event.evidences, str(evidence_id.value).lower(), None
        )
    ) and isinstance(evidence, EventEvidence):
        full_name = f"evidences/{group_name}/{event_id}/{evidence.file_name}"
        await s3_ops.remove_file(full_name)
        await events_model.update_evidence(
            event_id=event_id,
            group_name=group_name,
            evidence_info=None,
            evidence_id=evidence_id,
        )


async def solve_event(  # pylint: disable=too-many-locals
    info: GraphQLResolveInfo,
    event_id: str,
    hacker_email: str,
    reason: EventSolutionReason,
    other: Optional[str],
) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    """Solves an Event, can either return two empty dicts or
    the `reattacks_dict[finding_id, set_of_respective_vuln_ids]`
    and the `verifications_dict[finding_id, list_of_respective_vuln_ids]`"""
    loaders: Dataloaders = info.context.loaders
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    other_reason: str = other if other else ""

    if event.state.status == EventStateStatus.SOLVED:
        raise EventAlreadyClosed()

    if reason not in SOLUTION_REASON_BY_EVENT_TYPE[event.type]:
        raise InvalidEventSolvingReason()

    affected_reattacks: tuple[
        Vulnerability, ...
    ] = await loaders.event_vulnerabilities_loader.load((event_id))
    has_reattacks: bool = len(affected_reattacks) > 0
    if has_reattacks:
        user_info = await sessions_domain.get_jwt_content(info.context)
        # For open vulns on hold
        reattacks_dict: dict[str, set[str]] = {}
        # For closed vulns on hold (yes, that can happen)
        verifications_dict: dict[str, list[str]] = {}
        for vuln in affected_reattacks:
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE:
                reattacks_dict.setdefault(vuln.finding_id, set()).add(vuln.id)
            elif vuln.state.status == VulnerabilityStateStatus.SAFE:
                verifications_dict.setdefault(vuln.finding_id, []).append(
                    vuln.id
                )

        for finding_id, reattack_ids in reattacks_dict.items():
            await findings_domain.request_vulnerabilities_verification(
                loaders=loaders,
                finding_id=finding_id,
                user_info=user_info,
                justification=(
                    f"Event #{event_id} was solved. The reattacks are back to "
                    "the Requested stage."
                ),
                vulnerability_ids=reattack_ids,
                is_closing_event=True,
            )
        for finding_id, verification_ids in verifications_dict.items():
            # Mark all closed vulns as verified
            await findings_domain.verify_vulnerabilities(
                context=info.context,
                finding_id=finding_id,
                user_info=user_info,
                justification=(
                    f"Event #{event_id} was solved. As these vulnerabilities "
                    "were closed, the reattacks are set to Verified."
                ),
                open_vulns_ids=[],
                closed_vulns_ids=verification_ids,
                vulns_to_close_from_file=[],
                is_closing_event=True,
                loaders=info.context.loaders,
            )

    await events_model.update_state(
        current_value=event,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=datetime_utils.get_utc_now(),
            other=other_reason,
            reason=reason,
            status=EventStateStatus.SOLVED,
        ),
    )

    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            event_type=event.type.value,
            description=event.description,
            root_id=event.root_id,
            reason=reason.value,
            other=other,
            is_closed=True,
            report_date=event.event_date.date(),
        )
    )

    if has_reattacks:
        return (reattacks_dict, verifications_dict)
    return ({}, {})


async def reject_solution(
    loaders: Dataloaders,
    event_id: str,
    comments: str,
    stakeholder_email: str,
    stakeholder_full_name: str,
) -> None:
    validations.validate_fields([comments])
    event: Event = await loaders.event.load(event_id)
    if event.state.status is not EventStateStatus.VERIFICATION_REQUESTED:
        raise EventVerificationNotRequested()

    comment_id: str = str(round(time() * 1000))
    parent_comment_id = (
        event.state.comment_id if event.state.comment_id else "0"
    )
    await add_comment(
        loaders=loaders,
        comment_data=EventComment(
            event_id=event.id,
            parent_id=parent_comment_id,
            id=comment_id,
            content=comments,
            creation_date=datetime_utils.get_utc_now(),
            email=stakeholder_email,
            full_name=stakeholder_full_name,
        ),
        email=stakeholder_email,
        event_id=event.id,
        parent_comment=parent_comment_id,
    )
    await events_model.update_state(
        current_value=event,
        group_name=event.group_name,
        state=EventState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            comment_id=comment_id,
            status=EventStateStatus.CREATED,
        ),
    )


async def request_verification(
    loaders: Dataloaders,
    event_id: str,
    comments: str,
    stakeholder_email: str,
    stakeholder_full_name: str,
) -> None:
    validations.validate_fields([comments])
    event: Event = await loaders.event.load(event_id)
    if event.state.status is EventStateStatus.SOLVED:
        raise EventAlreadyClosed()
    if event.state.status is EventStateStatus.VERIFICATION_REQUESTED:
        raise EventVerificationAlreadyRequested()

    comment_id: str = str(round(time() * 1000))
    await add_comment(
        loaders=loaders,
        comment_data=EventComment(
            event_id=event.id,
            parent_id="0",
            id=comment_id,
            content=comments,
            creation_date=datetime_utils.get_utc_now(),
            email=stakeholder_email,
            full_name=stakeholder_full_name,
        ),
        email=stakeholder_email,
        event_id=event.id,
        parent_comment="0",
    )
    await events_model.update_state(
        current_value=event,
        group_name=event.group_name,
        state=EventState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            comment_id=comment_id,
            status=EventStateStatus.VERIFICATION_REQUESTED,
        ),
    )


async def update_event(
    loaders: Dataloaders,
    event_id: str,
    stakeholder_email: str,
    attributes: EventAttributesToUpdate,
) -> None:
    event: Event = await loaders.event.load(event_id)
    solving_reason = attributes.solving_reason or event.state.reason
    other_solving_reason = (
        attributes.other_solving_reason or event.state.other
        if solving_reason == EventSolutionReason.OTHER
        else None
    )
    event_type = attributes.event_type or event.type
    if all(attribute is None for attribute in attributes):
        raise RequiredFieldToBeUpdate()

    if attributes.event_type:
        events_validations.validate_type(attributes.event_type)

    if (
        solving_reason == EventSolutionReason.OTHER
        and not other_solving_reason
    ):
        raise InvalidParameter("otherSolvingReason")

    if (
        solving_reason is not None
        and event.state.status != EventStateStatus.SOLVED
    ):
        raise EventHasNotBeenSolved()

    if (
        event.state.status == EventStateStatus.SOLVED
        and solving_reason not in SOLUTION_REASON_BY_EVENT_TYPE[event_type]
    ):
        raise InvalidEventSolvingReason()

    if attributes.event_type:
        await events_model.update_metadata(
            event_id=event.id,
            group_name=event.group_name,
            metadata=EventMetadataToUpdate(type=attributes.event_type),
        )

    if (
        attributes.solving_reason != event.state.reason
        or attributes.other_solving_reason != event.state.other
    ):
        await events_model.update_state(
            current_value=event,
            group_name=event.group_name,
            state=EventState(
                modified_by=stakeholder_email,
                modified_date=datetime_utils.get_utc_now(),
                other=other_solving_reason,
                reason=solving_reason,
                status=event.state.status,
            ),
        )


async def update_evidence(
    loaders: Dataloaders,
    event_id: str,
    evidence_id: EventEvidenceId,
    file: UploadFile,
    update_date: datetime,
) -> None:
    validations.validate_sanitized_csv_input(event_id)
    event: Event = await loaders.event.load(event_id)
    if event.state.status == EventStateStatus.SOLVED:
        raise EventAlreadyClosed()

    extension = {
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
        "video/webm": ".webm",
    }.get(file.content_type, "")
    group_name = event.group_name
    file_name = (
        f"{group_name}_{event_id}_evidence_"
        f"{str(evidence_id.value).lower()}{extension}"
    )
    full_name = f"{group_name}/{event_id}/{file_name}"
    validations.validate_sanitized_csv_input(
        file.filename, file.content_type, full_name
    )

    await save_evidence(file, full_name)
    await events_model.update_evidence(
        event_id=event_id,
        group_name=group_name,
        evidence_info=EventEvidence(
            file_name=file_name,
            modified_date=update_date,
        ),
        evidence_id=evidence_id,
    )


async def update_solving_reason(
    loaders: Dataloaders,
    event_id: str,
    stakeholder_email: str,
    reason: EventSolutionReason,
    other: Optional[str],
) -> None:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    if reason == EventSolutionReason.OTHER and not other:
        raise InvalidParameter("other")
    other_reason: Optional[str] = (
        other if reason == EventSolutionReason.OTHER else None
    )

    if event.state.status != EventStateStatus.SOLVED:
        raise EventHasNotBeenSolved()

    if reason not in SOLUTION_REASON_BY_EVENT_TYPE[event.type]:
        raise InvalidEventSolvingReason()

    await events_model.update_state(
        current_value=event,
        group_name=group_name,
        state=EventState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            other=other_reason,
            reason=reason,
            status=event.state.status,
        ),
    )


async def validate_evidence(
    *,
    group_name: str,
    organization_name: str,
    evidence_id: EventEvidenceId,
    file: UploadFile,
) -> None:
    mib = 1048576
    validations.validate_file_name(file.filename)
    validations.validate_fields([file.content_type])

    if evidence_id in IMAGE_EVIDENCE_IDS:
        allowed_mimes = ["image/gif", "image/jpeg", "image/png", "video/webm"]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_IMAGE")
    elif evidence_id in FILE_EVIDENCE_IDS:
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
    else:
        raise InvalidFileType("EVENT")

    if await files_utils.get_file_size(file) > 10 * mib:
        raise InvalidFileSize()

    validate_evidencename(
        organization_name=organization_name.lower(),
        group_name=group_name.lower(),
        filename=file.filename.lower(),
    )


async def request_vulnerabilities_hold(
    loaders: Dataloaders,
    finding_id: str,
    event_id: str,
    user_info: dict[str, str],
    vulnerability_ids: set[str],
) -> None:
    vulnerabilities: Union[tuple[Vulnerability, ...], list[Vulnerability]]
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
        modified_date=datetime_utils.get_utc_now(),
        status=FindingVerificationStatus.ON_HOLD,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    await collect(
        vulns_domain.request_hold(event_id, vuln) for vuln in vulnerabilities
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        creation_date=datetime_utils.get_utc_now(),
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
    )
    await finding_comments_domain.add(loaders, comment_data)


async def get_unsolved_events_by_root(
    loaders: Dataloaders, group_name: str
) -> dict[str, tuple[Event, ...]]:
    unsolved_events_by_root: DefaultDict[
        Optional[str], list[Event]
    ] = defaultdict(list[Event])
    unsolved_events: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name, is_solved=False)
    )
    for event in unsolved_events:
        unsolved_events_by_root[event.root_id].append(event)
    return {
        root_id: tuple(events)
        for root_id, events in unsolved_events_by_root.items()
        if root_id
    }
