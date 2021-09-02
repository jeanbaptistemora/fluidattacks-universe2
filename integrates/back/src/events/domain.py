"""Domain functions for events."""  # pylint:disable=cyclic-import

from aioextensions import (
    collect,
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
)
from custom_types import (
    Comment as CommentType,
    Event as EventType,
)
from datetime import (
    datetime,
)
from events import (
    dal as events_dal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
    events as events_utils,
    files as files_utils,
    validations,
)
from newutils.utils import (
    get_key_or_fallback,
)
import pytz  # type: ignore
import random
from settings import (
    TIME_ZONE,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from users import (
    domain as users_domain,
)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    event_id: str,
    parent: str,
) -> Tuple[Union[str, None], bool]:
    parent = str(parent)
    content = str(comment_data["content"])
    event_loader = info.context.loaders.event
    event = await event_loader.load(event_id)
    group_name = get_key_or_fallback(event)

    await authz.validate_handle_comment_scope(
        content, user_email, group_name, parent, info.context.store
    )
    if parent != "0":
        event_comments = [
            comment["comment_id"]
            for comment in await comments_domain.get("event", event_id)
        ]
        if parent not in event_comments:
            raise InvalidCommentParent()
    user_data = await users_domain.get(user_email)
    user_data["user_email"] = user_data.pop("email")
    success = await comments_domain.add(event_id, comment_data, user_data)
    return cast(Tuple[Optional[str], bool], success)


async def add_event(  # pylint: disable=too-many-locals
    loaders: Any,
    analyst_email: str,
    group_name: str,
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    **kwargs: Any,
) -> bool:
    validations.validate_fields([kwargs["detail"]])
    validations.validate_field_length(kwargs["detail"], 300)

    event_id = str(random.randint(10000000, 170000000))  # nosec
    tzn = pytz.timezone(TIME_ZONE)
    today = datetime_utils.get_now()

    group_loader = loaders.group
    group = await group_loader.load(group_name)
    subscription = group["subscription"]
    org_id = group["organization"]

    event_attrs = kwargs.copy()
    event_date = event_attrs.pop("event_date").astimezone(tzn)
    if event_date > today:
        raise InvalidDate()

    event_attrs.update(
        {
            "accessibility": " ".join(list(set(event_attrs["accessibility"]))),
            "analyst": analyst_email,
            "client": org_id,
            "historic_state": [
                {
                    "analyst": analyst_email,
                    "date": datetime_utils.get_as_str(event_date),
                    "state": "OPEN",
                },
                {
                    "analyst": analyst_email,
                    "date": datetime_utils.get_as_str(today),
                    "state": "CREATED",
                },
            ],
            "subscription": subscription.upper(),
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
    return success


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
    unsolved = [
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
            comments_domain.delete(comment["comment_id"], event_id)
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


async def solve_event(
    event_id: str, affectation: str, analyst_email: str, date: datetime
) -> bool:
    event = await get_event(event_id)
    success = False

    if (
        cast(List[Dict[str, str]], event.get("historic_state", []))[-1].get(
            "state"
        )
        == "SOLVED"
    ):
        raise EventAlreadyClosed()

    today = datetime_utils.get_now()
    history = cast(List[Dict[str, str]], event.get("historic_state", []))
    history += [
        {
            "analyst": analyst_email,
            "date": datetime_utils.get_as_str(date),
            "state": "CLOSED",
        },
        {
            "affectation": affectation,
            "analyst": analyst_email,
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
    success = False

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

    if await events_dal.save_evidence(file, full_name):
        success = await events_dal.update(
            event_id,
            {
                evidence_type: evidence_id,
                f"{evidence_type}_date": datetime_utils.get_as_str(
                    update_date
                ),
            },
        )
    return success


async def validate_evidence(evidence_type: str, file: UploadFile) -> bool:
    mib = 1048576
    success = False

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
