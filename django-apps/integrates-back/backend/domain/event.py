"""Domain functions for events."""
from typing import Dict, List, Tuple, Union, cast
import random
import threading
from datetime import datetime

import pytz
from django.conf import settings
from magic import Magic

from backend import util
from backend.dal import event as event_dal, project as project_dal
from backend.domain import (
    comment as comment_domain, resources as resources_domain,
    user as user_domain
)
from backend.exceptions import (
    EventAlreadyClosed, EventNotFound, InvalidDate, InvalidFileSize,
    InvalidFileType
)
from backend.mailer import send_comment_mail, send_mail_new_event
from backend.typing import Event as EventType, User as UserType
from backend.utils import events as event_utils

from __init__ import (
    FI_CLOUDFRONT_RESOURCES_DOMAIN, FI_MAIL_CONTINUOUS,
    FI_MAIL_PRODUCTION, FI_MAIL_PROJECTS, FI_MAIL_REVIEWERS
)


def update_event(event_id: str, **kwargs) -> bool:
    """Update an event associated to a project."""
    event = get_event(event_id)
    success = False

    if cast(List[Dict[str, str]],
            event.get('historic_state', []))[-1].get('state') == 'SOLVED':
        raise EventAlreadyClosed()

    success = event_dal.update(event_id, kwargs)

    return success


def solve_event(event_id: str, affectation: str, analyst_email: str, date: datetime) -> bool:
    event = get_event(event_id)
    success = False

    if cast(List[Dict[str, str]],
            event.get('historic_state', []))[-1].get('state') == 'SOLVED':
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

    success = event_dal.update(event_id, {'historic_state': history})

    return success


def update_evidence(event_id: str, evidence_type: str, file) -> bool:
    event = get_event(event_id)
    success = False

    if cast(List[Dict[str, str]],
            event.get('historic_state', []))[-1].get('state') == 'SOLVED':
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

    if event_dal.save_evidence(file, full_name):
        success = event_dal.update(event_id, {evidence_type: evidence_id})

    return success


def validate_evidence(evidence_type: str, file) -> bool:
    success = False

    if evidence_type == 'evidence':
        allowed_mimes = ['image/gif', 'image/jpeg', 'image/png']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_IMAGE')
    else:
        allowed_mimes = [
            'application/pdf', 'application/zip', 'text/csv', 'text/plain']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType('EVENT_FILE')

    mib = 1048576
    if file.size < 10 * mib:
        success = True
    else:
        raise InvalidFileSize()

    return success


def _send_new_event_mail(
        analyst: str, event_id: str, project: str, subscription: str, event_type: str):
    recipients = project_dal.list_project_managers(project)
    recipients.append(analyst)
    if subscription == 'oneshot':
        recipients.append(FI_MAIL_PROJECTS)
    elif subscription == 'continuous':
        recipients += [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
    if event_type in ['CLIENT_APPROVES_CHANGE_TOE',
                      'CLIENT_CANCELS_PROJECT_MILESTONE',
                      'CLIENT_EXPLICITLY_SUSPENDS_PROJECT']:
        recipients.append(FI_MAIL_PRODUCTION)
        recipients += FI_MAIL_REVIEWERS.split(',')

    email_context = {
        'analyst_email': analyst,
        'event_id': event_id,
        'event_url': (
            'https://fluidattacks.com/integrates/dashboard#!/'
            f'project/{project}/events/{event_id}'),
        'project': project
    }

    recipients_customers = [
        recipient for recipient in recipients
        if user_domain.get_data(recipient, 'role') == 'customeradmin']
    recipients_not_customers = [
        recipient for recipient in recipients
        if user_domain.get_data(recipient, 'role') != 'customeradmin']
    email_context_customers = email_context.copy()
    email_context_customers['analyst_email'] = \
        'Hacker at ' + str(user_domain.get_data(analyst, 'company')).capitalize()

    email_send_thread = threading.Thread(
        name='New event email thread',
        target=send_mail_new_event,
        args=([recipients_not_customers, recipients_customers],
              [email_context, email_context_customers]))
    email_send_thread.start()


def create_event(analyst_email: str, project_name: str, file = None,
                 image = None, **kwargs) -> bool:
    event_id = str(random.randint(10000000, 170000000))

    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today()

    project = project_dal.get_attributes(project_name, ['companies', 'type'])
    subscription = str(project.get('type'))

    event_attrs = kwargs.copy()
    event_date = event_attrs['event_date'].astimezone(
        tzn).replace(tzinfo=None)
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
            valid = validate_evidence('evidence_file', file) \
                and validate_evidence('evidence', image)
        elif file:
            valid = validate_evidence('evidence_file', file)
        elif image:
            valid = validate_evidence('evidence', image)

        if valid and event_dal.create(event_id, project_name, event_attrs):
            if file:
                update_evidence(event_id, 'evidence_file', file)
            if image:
                update_evidence(event_id, 'evidence', image)
            success = True
            _send_new_event_mail(
                analyst_email, event_id, project_name, subscription,
                event_attrs['event_type'])

    else:
        success = event_dal.create(event_id, project_name, event_attrs)
        _send_new_event_mail(
            analyst_email, event_id, project_name, subscription,
            event_attrs['event_type'])

    return success


def get_event(event_id: str) -> EventType:
    event = event_dal.get_event(event_id)
    if not event:
        raise EventNotFound()

    return event


def get_events(event_ids: List[str]) -> List[EventType]:
    events = [event_utils.format_data(get_event(event_id)) for event_id in event_ids]

    return events


def add_comment(
        content: str, event_id: str, parent: str, user_info: UserType) -> Tuple[Union[int, None], bool]:
    success = comment_domain.create(
        'event', content, event_id, parent, user_info)
    comment_data = {'parent': int(parent), 'content': content}
    if success:
        send_comment_mail(
            comment_data, 'event', str(user_info['user_email']), 'event', get_event(event_id))

    return success


def get_evidence_link(event_id: str, file_name: str) -> str:
    project_name = get_event(event_id).get('project_name')
    file_url = f'{project_name}/{event_id}/{file_name}'
    minutes_until_expire = 1.0 / 6

    return resources_domain.sign_url(
        FI_CLOUDFRONT_RESOURCES_DOMAIN, file_url, minutes_until_expire)


def remove_evidence(evidence_type: str, event_id: str) -> bool:
    finding = get_event(event_id)
    project_name = finding['project_name']
    success = False

    full_name = f'{project_name}/{event_id}/{finding[evidence_type]}'
    if event_dal.remove_evidence(full_name):
        success = event_dal.update(event_id, {evidence_type: None})

    return success
