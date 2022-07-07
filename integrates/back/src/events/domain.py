# pylint:disable=cyclic-import
from aioextensions import (
    collect,
    schedule,
)
import authz
from comments import (
    domain as comments_domain,
)
from context import (
    FI_AWS_S3_BUCKET,
)
from custom_exceptions import (
    EventAlreadyClosed,
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
)
from datetime import (
    date as date_type,
    datetime,
)
from db_model import (
    events as events_model,
    findings as findings_model,
)
from db_model.events.enums import (
    EventAccessibility,
    EventAffectedComponents,
    EventEvidenceType,
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
    Root,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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
    files as files_utils,
    token as token_utils,
    validations,
    vulnerabilities as vulns_utils,
)
import pytz  # type: ignore
import random
from s3 import (
    operations as s3_ops,
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
        FI_AWS_S3_BUCKET,
        file_object,
        file_name,
    )


async def search_evidence(file_name: str) -> list[str]:
    return await s3_ops.list_files(FI_AWS_S3_BUCKET, file_name)


async def remove_file_evidence(file_name: str) -> None:
    await s3_ops.remove_file(FI_AWS_S3_BUCKET, file_name)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: dict[str, Any],
    event_id: str,
    parent_comment: str,
) -> tuple[Union[str, None], bool]:
    parent_comment = str(parent_comment)
    content = str(comment_data["content"])
    loaders = info.context.loaders
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name

    validations.validate_field_length(content, 20000)
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

    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    success = await comments_domain.add(event_id, comment_data, stakeholder)
    return success


async def add_event(
    loaders: Any,
    hacker_email: str,
    group_name: str,
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    **kwargs: Any,
) -> AddEventPayload:
    validations.validate_fields([kwargs["detail"], kwargs["root_id"]])
    validations.validate_field_length(kwargs["detail"], 300)
    root: Root = await loaders.root.load((group_name, kwargs["root_id"]))
    if root.state.status != "ACTIVE":
        raise InvalidParameter(field="rootId")
    if file:
        await validate_evidence(EventEvidenceType.FILE, file)
    if image:
        await validate_evidence(EventEvidenceType.IMAGE, image)

    tzn = pytz.timezone(TIME_ZONE)
    event_date: datetime = kwargs["event_date"].astimezone(tzn)
    if event_date > datetime_utils.get_now():
        raise InvalidDate()

    group: Group = await loaders.group.load(group_name)
    accessibility: Optional[set[EventAccessibility]] = None
    if "accessibility" in kwargs:
        accessibility = set(
            EventAccessibility[item]
            for item in kwargs["accessibility"]
            if item
        )
    affected_components: Optional[set[EventAffectedComponents]] = None
    if "affected_components" in kwargs:
        affected_components = set(
            EventAffectedComponents[item]
            for item in kwargs["affected_components"]
            if item
        )
    event = Event(
        accessibility=accessibility,
        affected_components=affected_components,
        client=group.organization_id,
        description=kwargs["detail"],
        event_date=datetime_utils.get_as_utc_iso_format(event_date),
        evidences=EventEvidences(),
        group_name=group_name,
        hacker=hacker_email,
        id=str(random.randint(10000000, 170000000)),  # nosec
        root_id=root.id,
        state=EventState(
            modified_by=hacker_email,
            modified_date=datetime_utils.get_as_utc_iso_format(event_date),
            status=EventStateStatus.OPEN,
        ),
        type=EventType[kwargs["event_type"]],
    )
    await events_model.add(event=event)
    await events_model.update_state(
        event_id=event.id,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=datetime_utils.get_iso_date(),
            status=EventStateStatus.CREATED,
        ),
    )

    if file:
        await update_evidence(
            loaders, event.id, EventEvidenceType.FILE, file, event_date
        )
    if image:
        await update_evidence(
            loaders, event.id, EventEvidenceType.IMAGE, image, event_date
        )

    report_date: date_type = datetime_utils.get_date_from_iso_str(
        event.event_date
    )
    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event.id,
            event_type=event.type,
            description=event.description,
            root_id=event.root_id,
            report_date=report_date,
        )
    )

    return AddEventPayload(event.id, True)


async def get_unsolved_events(loaders: Any, group_name: str) -> list[Event]:
    events: tuple[Event, ...] = await loaders.group_events.load(group_name)
    unsolved: list[Event] = [
        event
        for event in events
        if event.state.status == EventStateStatus.CREATED
    ]
    return unsolved


async def get_evidence_link(
    loaders: Any, event_id: str, file_name: str
) -> str:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    file_url = f"{group_name}/{event_id}/{file_name}"
    return await s3_ops.sign_url(file_url, 10, FI_AWS_S3_BUCKET)


async def get_solving_state(
    loaders: Any, event_id: str
) -> Optional[EventState]:
    historic_states: tuple[
        EventState, ...
    ] = await loaders.event_historic_state.load(event_id)
    for state in sorted(
        historic_states,
        key=lambda state: datetime.fromisoformat(state.modified_date),
    ):
        if state.status == EventStateStatus.SOLVED:
            return state

    return None


async def get_solving_date(loaders: Any, event_id: str) -> Optional[str]:
    """Returns the date of the last closing state"""
    last_closing_state = await get_solving_state(loaders, event_id)

    return last_closing_state.modified_date if last_closing_state else None


async def has_access_to_event(loaders: Any, email: str, event_id: str) -> bool:
    """Verify if the user has access to a event submission."""
    event: Event = await loaders.event.load(event_id)
    group = event.group_name
    return bool(await authz.has_access_to_group(email, group))


async def mask(loaders: Any, event_id: str) -> bool:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name

    list_comments = await comments_domain.get("event", event_id)
    mask_events_coroutines = [
        comments_domain.delete(str(comment["comment_id"]), event_id)
        for comment in list_comments
    ]

    mask_events_coroutines_none = [
        events_model.update_metadata(
            event_id=event_id,
            group_name=group_name,
            metadata=EventMetadataToUpdate(
                client="Masked",
                description="Masked",
            ),
        )
    ]
    evidence_prefix = f"{group_name}/{event_id}"
    list_evidences = await search_evidence(evidence_prefix)
    mask_events_coroutines_none.extend(
        [remove_file_evidence(file_name) for file_name in list_evidences]
    )

    await collect(mask_events_coroutines_none)
    return all(await collect(mask_events_coroutines))


async def remove_evidence(
    loaders: Any, evidence_type: EventEvidenceType, event_id: str
) -> None:
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name

    if evidence_type == EventEvidenceType.IMAGE and event.evidences.image:
        full_name = (
            f"{group_name}/{event_id}/{event.evidences.image.file_name}"
        )
    elif event.evidences.file:
        full_name = f"{group_name}/{event_id}/{event.evidences.file.file_name}"
    await s3_ops.remove_file(FI_AWS_S3_BUCKET, full_name)
    await events_model.update_evidence(
        event_id=event_id,
        group_name=group_name,
        evidence_info=None,
        evidence_type=evidence_type,
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
    loaders = info.context.loaders
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    other_reason: str = other if other else ""

    if event.state.status == EventStateStatus.SOLVED:
        raise EventAlreadyClosed()

    affected_reattacks: tuple[
        Vulnerability, ...
    ] = await loaders.event_vulnerabilities_loader.load((event_id))
    has_reattacks: bool = len(affected_reattacks) > 0
    if has_reattacks:
        user_info = await token_utils.get_jwt_content(info.context)
        # For open vulns on hold
        reattacks_dict: dict[str, set[str]] = {}
        # For closed vulns on hold (yes, that can happen)
        verifications_dict: dict[str, list[str]] = {}
        for vuln in affected_reattacks:
            if vuln.state.status == VulnerabilityStateStatus.OPEN:
                reattacks_dict.setdefault(vuln.finding_id, set()).add(vuln.id)
            elif vuln.state.status == VulnerabilityStateStatus.CLOSED:
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
            )

    await events_model.update_state(
        event_id=event_id,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=datetime_utils.get_iso_date(),
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
            report_date=datetime_utils.get_date_from_iso_str(event.event_date),
        )
    )

    if has_reattacks:
        return (reattacks_dict, verifications_dict)
    return ({}, {})


async def update_evidence(
    loaders: Any,
    event_id: str,
    evidence_type: EventEvidenceType,
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
    }.get(file.content_type, "")
    evidence_type_str = (
        "evidence"
        if evidence_type == EventEvidenceType.IMAGE
        else "evidence_file"
    )
    group_name = event.group_name
    evidence_id = f"{group_name}-{event_id}-{evidence_type_str}{extension}"
    full_name = f"{group_name}/{event_id}/{evidence_id}"
    validations.validate_sanitized_csv_input(full_name)
    validations.validate_sanitized_csv_input(file.filename, file.content_type)

    await save_evidence(file, full_name)
    await events_model.update_evidence(
        event_id=event_id,
        group_name=group_name,
        evidence_info=EventEvidence(
            file_name=evidence_id,
            modified_date=datetime_utils.get_as_utc_iso_format(update_date),
        ),
        evidence_type=evidence_type,
    )


async def validate_evidence(
    evidence_type: EventEvidenceType, file: UploadFile
) -> None:
    mib = 1048576
    validations.validate_file_name(file.filename)
    validations.validate_fields([file.content_type])

    if evidence_type == EventEvidenceType.IMAGE:
        allowed_mimes = ["image/gif", "image/jpeg", "image/png"]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_IMAGE")
    elif evidence_type == EventEvidenceType.FILE:
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

    if not await files_utils.get_file_size(file) < 10 * mib:
        raise InvalidFileSize()


async def request_vulnerabilities_hold(
    loaders: Any,
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
    comment_data: dict[str, Any] = {
        "comment_type": "verification",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    await comments_domain.add(finding_id, comment_data, stakeholder)
    if not success:
        LOGGER.error("An error occurred requesting hold")
        raise NoHoldRequested()
