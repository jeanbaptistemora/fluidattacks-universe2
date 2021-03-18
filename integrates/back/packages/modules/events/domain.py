"""Domain functions for events."""  # pylint:disable=cyclic-import
# Standard Libraries
import random
from datetime import datetime
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

# Third-party Libraries
import pytz
from aioextensions import (
    collect,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local Libraries
from back import settings
from backend import authz, mailer, util
from backend.dal import project as project_dal
from backend.domain import organization as org_domain
from backend.exceptions import (
    EventAlreadyClosed,
    EventNotFound,
    InvalidCommentParent,
    InvalidDate,
    InvalidFileSize,
    InvalidFileType
)
from backend.typing import (
    Comment as CommentType,
    Event as EventType,
    MailContent as MailContentType,
)
from comments import domain as comments_domain
from events import dal as events_dal
from newutils import (
    comments as comments_utils,
    datetime as datetime_utils,
    events as events_utils,
    validations,
)
from users import domain as users_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PRODUCTION,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS
)


async def solve_event(
        event_id: str,
        affectation: str,
        analyst_email: str,
        date: datetime) -> bool:
    event = await get_event(event_id)
    success = False

    if cast(
        List[Dict[str, str]],
        event.get('historic_state', [])
    )[-1].get('state') == 'SOLVED':
        raise EventAlreadyClosed()

    today = datetime_utils.get_now()
    history = cast(List[Dict[str, str]], event.get('historic_state', []))
    history += [
        {
            'analyst': analyst_email,
            'date': datetime_utils.get_as_str(date),
            'state': 'CLOSED'
        },
        {
            'affectation': affectation,
            'analyst': analyst_email,
            'date': datetime_utils.get_as_str(today),
            'state': 'SOLVED'
        }
    ]

    success = await events_dal.update(event_id, {'historic_state': history})

    return success


async def update_evidence(
    event_id: str,
    evidence_type: str,
    file: UploadFile,
    update_date: datetime,
) -> bool:
    event = await get_event(event_id)
    success = False

    if cast(
        List[Dict[str, str]],
        event.get('historic_state', [])
    )[-1].get('state') == 'SOLVED':
        raise EventAlreadyClosed()

    project_name = str(event.get('project_name', ''))
    extension = {
        'image/gif': '.gif',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/pdf': '.pdf',
        'application/zip': '.zip',
        'text/csv': '.csv',
        'text/plain': '.txt'
    }.get(file.content_type, '')
    evidence_id = f'{project_name}-{event_id}-{evidence_type}{extension}'
    full_name = f'{project_name}/{event_id}/{evidence_id}'

    if await events_dal.save_evidence(file, full_name):
        success = await events_dal.update(
            event_id,
            {
                evidence_type: evidence_id,
                f'{evidence_type}_date': datetime_utils.get_as_str(update_date)
            }
        )

    return success


async def validate_evidence(
        evidence_type: str,
        file: UploadFile) -> bool:
    mib = 1048576
    success = False

    if evidence_type == 'evidence':
        allowed_mimes = ['image/gif', 'image/jpeg', 'image/png']
        if not await util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_IMAGE')
    else:
        allowed_mimes = [
            'application/pdf',
            'application/zip',
            'text/csv',
            'text/plain'
        ]
        if not await util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_FILE')

    if await util.get_file_size(file) < 10 * mib:
        success = True
    else:
        raise InvalidFileSize()

    return success


async def _send_new_event_mail(  # pylint: disable=too-many-arguments
    org_id: str,
    analyst: str,
    event_id: str,
    group_name: str,
    subscription: str,
    event_type: str
) -> None:
    recipients = await project_dal.list_project_managers(group_name)
    recipients.append(analyst)
    org_name = await org_domain.get_name_by_id(org_id)
    if subscription == 'oneshot':
        recipients.append(FI_MAIL_PROJECTS)
    elif subscription == 'continuous':
        recipients += [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
    if event_type in ['CLIENT_APPROVES_CHANGE_TOE']:
        recipients.append(FI_MAIL_PRODUCTION)
        recipients += FI_MAIL_REVIEWERS.split(',')

    email_context: MailContentType = {
        'analyst_email': analyst,
        'event_id': event_id,
        'event_url': f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                     f'/events/{event_id}',
        'project': group_name,
        'organization': org_name
    }

    recipients_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient, group_name) == 'customeradmin'
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient, group_name) != 'customeradmin'
    ]
    email_context_customers = email_context.copy()
    email_context_customers['analyst_email'] = 'Hacker at FluidIntegrates'

    schedule(
        mailer.send_mail_new_event(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
        )
    )


async def create_event(  # pylint: disable=too-many-locals
    loaders: Any,
    analyst_email: str,
    group_name: str,
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    **kwargs: Any
) -> bool:
    group_loader = loaders.group_all
    validations.validate_fields([kwargs['detail']])
    validations.validate_field_length(kwargs['detail'], 300)
    event_id = str(random.randint(10000000, 170000000))

    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime_utils.get_now()

    group = await group_loader.load(group_name)
    subscription = group['subscription']
    org_id = group['organization']

    event_attrs = kwargs.copy()
    event_date = (
        event_attrs['event_date']
        .astimezone(tzn)
    )
    del event_attrs['event_date']
    if event_date > today:
        raise InvalidDate()

    event_attrs.update({
        'accessibility': ' '.join(list(set(event_attrs['accessibility']))),
        'analyst': analyst_email,
        'client': org_id,
        'historic_state': [
            {
                'analyst': analyst_email,
                'date': datetime_utils.get_as_str(event_date),
                'state': 'OPEN'
            },
            {
                'analyst': analyst_email,
                'date': datetime_utils.get_as_str(today),
                'state': 'CREATED'
            }
        ],
        'subscription': subscription.upper()
    })
    if 'affected_components' in event_attrs:
        event_attrs['affected_components'] = '\n'.join(
            list(set(event_attrs['affected_components'])))

    if any([file, image]):
        if file and image:
            valid = (
                validate_evidence('evidence_file', file) and
                validate_evidence('evidence', image)
            )
        elif file:
            valid = validate_evidence('evidence_file', file)
        elif image:
            valid = validate_evidence('evidence', image)

        if (valid and
                await events_dal.create(event_id, group_name, event_attrs)):
            if file:
                await update_evidence(
                    event_id, 'evidence_file', file, event_date
                )
            if image:
                await update_evidence(event_id, 'evidence', image, event_date)
            success = True
            await _send_new_event_mail(
                org_id,
                analyst_email,
                event_id,
                group_name,
                subscription,
                event_attrs['event_type']
            )

    else:
        success = await events_dal.create(event_id, group_name, event_attrs)
        await _send_new_event_mail(
            org_id,
            analyst_email,
            event_id,
            group_name,
            subscription,
            event_attrs['event_type']
        )

    return success


async def get_event(event_id: str) -> EventType:
    event = await events_dal.get_event(event_id)
    if not event:
        raise EventNotFound()

    return events_utils.format_data(event)


async def get_events(event_ids: List[str]) -> List[EventType]:
    return cast(
        List[EventType],
        await collect(
            get_event(event_id)
            for event_id in event_ids
        )
    )


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    event_id: str,
    parent: str,
) -> Tuple[Union[int, None], bool]:
    parent = str(parent)
    content = str(comment_data['content'])
    event_loader = info.context.loaders.event
    event = await event_loader.load(event_id)
    project_name = event['project_name']

    await comments_utils.validate_handle_comment_scope(
        content,
        user_email,
        project_name,
        parent,
        info.context.store
    )

    if parent != '0':
        event_comments = [
            str(comment.get('user_id'))
            for comment in await comments_domain.get('event', int(event_id))
        ]
        if parent not in event_comments:
            raise InvalidCommentParent()
    user_data = await users_domain.get(user_email)
    user_data['user_email'] = user_data.pop('email')
    success = await comments_domain.create(event_id, comment_data, user_data)
    del comment_data['user_id']

    return cast(
        Tuple[Optional[int], bool],
        success
    )


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    event: EventType
) -> None:
    schedule(
        mailer.send_comment_mail(
            comment_data,
            'event',
            user_email,
            'event',
            event
        )
    )


async def get_evidence_link(event_id: str, file_name: str) -> str:
    event = await get_event(event_id)
    project_name = event['project_name']
    file_url = f'{project_name}/{event_id}/{file_name}'

    return await events_dal.sign_url(file_url)


async def remove_evidence(evidence_type: str, event_id: str) -> bool:
    event = await get_event(event_id)
    project_name = event['project_name']
    success = False

    full_name = f'{project_name}/{event_id}/{event[evidence_type]}'
    if await events_dal.remove_evidence(full_name):
        success = await events_dal.update(
            event_id,
            {evidence_type: None, f'{evidence_type}_date': None}
        )

    return success


async def mask(event_id: str) -> bool:
    event = await events_dal.get_event(event_id)
    attrs_to_mask = [
        'client',
        'detail',
        'evidence',
        'evidence_date',
        'evidence_file',
        'evidence_file_date'
    ]
    mask_events_coroutines = []

    mask_events_coroutines.append(
        events_dal.update(
            event_id,
            {attr: 'Masked' for attr in attrs_to_mask}
        )
    )

    project_name = str(event.get('project_name', ''))
    evidence_prefix = f'{project_name}/{event_id}'
    list_evidences = await events_dal.search_evidence(evidence_prefix)
    mask_events_coroutines.extend([
        events_dal.remove_evidence(file_name)
        for file_name in list_evidences
    ])

    list_comments = await comments_domain.get('event', int(event_id))
    mask_events_coroutines.extend([
        comments_domain.delete(int(event_id), int(comment['user_id']))
        for comment in list_comments
    ])
    success = all(await collect(mask_events_coroutines))
    return success
