"""Domain functions for events."""
from typing import Dict, List, Tuple, Union, cast
import asyncio
import random
import threading
from datetime import datetime

import pytz
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from magic import Magic

from backend import authz, mailer, util
from backend.dal import (
    comment as comment_dal,
    event as event_dal,
    project as project_dal
)
from backend.domain import (
    comment as comment_domain,
    user as user_domain
)
from backend.exceptions import (
    EventAlreadyClosed,
    EventNotFound,
    InvalidCommentParent,
    InvalidDate,
    InvalidFileSize,
    InvalidFileType
)
from backend.typing import (
    Event as EventType,
    User as UserType
)
from backend.utils import (
    events as event_utils,
    validations
)

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

    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today()
    history = cast(List[Dict[str, str]], event.get('historic_state', []))
    history += [
        {
            'analyst': analyst_email,
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'CLOSED'
        },
        {
            'affectation': affectation,
            'analyst': analyst_email,
            'date': today.strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'SOLVED'
        }
    ]

    success = await event_dal.update(event_id, {'historic_state': history})

    return success


async def update_evidence(event_id: str, evidence_type: str, file) -> bool:
    event = await get_event(event_id)
    success = False

    if cast(
        List[Dict[str, str]],
        event.get('historic_state', [])
    )[-1].get('state') == 'SOLVED':
        raise EventAlreadyClosed()

    project_name = str(event.get('project_name', ''))
    try:
        mime = Magic(mime=True).from_buffer(file.file.getvalue())
        extension = {
            'image/gif': '.gif',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'application/pdf': '.pdf',
            'application/zip': '.zip',
            'text/csv': '.csv',
            'text/plain': '.txt'
        }[mime]
    except AttributeError:
        extension = ''
    evidence_id = f'{project_name}-{event_id}-{evidence_type}{extension}'
    full_name = f'{project_name}/{event_id}/{evidence_id}'

    if await event_dal.save_evidence(file, full_name):
        success = await event_dal.update(
            event_id, {evidence_type: evidence_id})

    return success


def validate_evidence(evidence_type: str, file) -> bool:
    success = False

    if evidence_type == 'evidence':
        allowed_mimes = ['image/gif', 'image/jpeg', 'image/png']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_IMAGE')
    else:
        allowed_mimes = [
            'application/pdf',
            'application/zip',
            'text/csv',
            'text/plain'
        ]
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_FILE')

    mib = 1048576
    if file.size < 10 * mib:
        success = True
    else:
        raise InvalidFileSize()

    return success


def _send_new_event_mail(
        analyst: str,
        event_id: str,
        project: str,
        subscription: str,
        event_type: str):
    recipients = project_dal.list_project_managers(project)
    recipients.append(analyst)
    if subscription == 'oneshot':
        recipients.append(FI_MAIL_PROJECTS)
    elif subscription == 'continuous':
        recipients += [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
    if event_type in ['CLIENT_APPROVES_CHANGE_TOE']:
        recipients.append(FI_MAIL_PRODUCTION)
        recipients += FI_MAIL_REVIEWERS.split(',')

    email_context = {
        'analyst_email': analyst,
        'event_id': event_id,
        'event_url': f'{BASE_URL}/groups/{project}/events/{event_id}',
        'project': project
    }

    recipients_customers = [
        recipient
        for recipient in recipients
        if authz.get_group_level_role(recipient, project) == 'customeradmin'
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if authz.get_group_level_role(recipient, project) != 'customeradmin'
    ]
    email_context_customers = email_context.copy()
    company = str(user_domain.get_data(analyst, 'company')).capitalize()
    email_context_customers['analyst_email'] = f'Hacker at {company}'

    email_send_thread = threading.Thread(
        name='New event email thread',
        target=mailer.send_mail_new_event,
        args=(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
        )
    )
    email_send_thread.start()


async def create_event(
        analyst_email: str,
        project_name: str,
        file=None,
        image=None,
        **kwargs) -> bool:
    validations.validate_fields([kwargs['detail']])
    validations.validate_field_length(kwargs['detail'], 300)
    event_id = str(random.randint(10000000, 170000000))

    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today()

    project = project_dal.get_attributes(project_name, ['companies', 'type'])
    subscription = str(project.get('type'))

    event_attrs = kwargs.copy()
    event_date = (
        event_attrs['event_date']
        .astimezone(tzn)
        .replace(tzinfo=None)
    )
    del event_attrs['event_date']
    if event_date > today:
        raise InvalidDate()

    event_attrs.update({
        'accessibility': ' '.join(list(set(event_attrs['accessibility']))),
        'analyst': analyst_email,
        'client': project.get('companies', [''])[0],
        'historic_state': [
            {
                'analyst': analyst_email,
                'date': event_date.strftime('%Y-%m-%d %H:%M:%S'),
                'state': 'OPEN'
            },
            {
                'analyst': analyst_email,
                'date': today.strftime('%Y-%m-%d %H:%M:%S'),
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
                await event_dal.create(event_id, project_name, event_attrs)):
            if file:
                await update_evidence(event_id, 'evidence_file', file)
            if image:
                await update_evidence(event_id, 'evidence', image)
            success = True
            _send_new_event_mail(
                analyst_email, event_id, project_name, subscription,
                event_attrs['event_type']
            )

    else:
        success = await event_dal.create(event_id, project_name, event_attrs)
        _send_new_event_mail(
            analyst_email, event_id, project_name, subscription,
            event_attrs['event_type']
        )

    return success


async def get_event(event_id: str) -> EventType:
    event = await event_dal.get_event(event_id)
    if not event:
        raise EventNotFound()

    return event_utils.format_data(event)


async def get_events(event_ids: List[str]) -> List[EventType]:
    events_tasks = [
        asyncio.create_task(
            get_event(event_id)
        )
        for event_id in event_ids
    ]
    events = await asyncio.gather(*events_tasks)
    return events


async def add_comment(
        comment_id: int, content: str, event_id: str, parent: str,
        user_info: UserType) -> Tuple[Union[int, None], bool]:
    parent = str(parent)
    if parent != '0':
        event_comments = [
            str(comment.get('user_id'))
            for comment in await comment_dal.get_comments(
                'event',
                int(event_id)
            )
        ]
        if parent not in event_comments:
            raise InvalidCommentParent()
    comment_data = {
        'comment_type': 'event',
        'parent': parent,
        'content': content,
        'user_id': comment_id
    }
    success = await comment_domain.create(event_id, comment_data, user_info)
    del comment_data['user_id']
    if success:
        await sync_to_async(mailer.send_comment_mail)(
            comment_data,
            'event',
            str(user_info['user_email']),
            'event', await get_event(event_id)
        )

    return success


async def get_evidence_link(event_id: str, file_name: str) -> str:
    event = await get_event(event_id)
    project_name = event['project_name']
    file_url = f'{project_name}/{event_id}/{file_name}'

    return await event_dal.sign_url(file_url)


async def remove_evidence(evidence_type: str, event_id: str) -> bool:
    event = await get_event(event_id)
    project_name = event['project_name']
    success = False

    full_name = f'{project_name}/{event_id}/{event[evidence_type]}'
    if await event_dal.remove_evidence(full_name):
        success = await event_dal.update(event_id, {evidence_type: None})

    return success


def mask(event_id: str) -> bool:
    event = async_to_sync(event_dal.get_event)(event_id)

    attrs_to_mask = ['client', 'detail', 'evidence', 'evidence_file']
    event_result = async_to_sync(event_dal.update)(
        event_id,
        {attr: 'Masked' for attr in attrs_to_mask}
    )

    project_name = str(event.get('project_name', ''))
    evidence_prefix = f'{project_name}/{event_id}'
    evidence_result = all([
        async_to_sync(event_dal.remove_evidence)(file_name)
        for file_name in async_to_sync(event_dal.search_evidence)(
            evidence_prefix)
    ])

    comments_result = all([
        comment_dal.delete(comment['finding_id'], comment['user_id'])
        for comment in async_to_sync(comment_dal.get_comments)(
            'event',
            int(event_id)
        )
    ])

    success = all([event_result, evidence_result, comments_result])
    util.invalidate_cache(event_id)

    return success
