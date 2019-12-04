"""Domain functions for events."""
import random
import threading
from datetime import datetime

import pytz
from django.conf import settings

from __init__ import (
    FI_CLOUDFRONT_RESOURCES_DOMAIN, FI_MAIL_CONTINUOUS, FI_MAIL_PRODUCTION,
    FI_MAIL_PROJECTS, FI_MAIL_REPLYERS
)
from app import util
from app.dal import integrates_dal, event as event_dal, project as project_dal
from app.domain import comment as comment_domain, resources as resources_domain
from app.exceptions import (
    EventAlreadyClosed, EventNotFound, InvalidDate, InvalidFileSize,
    InvalidFileType
)
from app.mailer import send_mail_comment, send_mail_new_event


def update_event(event_id, **kwargs):
    """Update an event associated to a project."""
    event = get_event(event_id)
    success = False

    if event.get('historic_state')[-1].get('state') == 'CLOSED':
        raise EventAlreadyClosed()

    success = event_dal.update(event_id, kwargs)

    return success


def solve_event(event_id, affectation, analyst_email, date):
    event = get_event(event_id)
    success = False

    if event.get('historic_state')[-1].get('state') == 'CLOSED':
        raise EventAlreadyClosed()

    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today()
    history = event.get('historic_state')
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


def update_evidence(event_id, evidence_type, file):
    event = get_event(event_id)
    success = False

    if event.get('historic_state')[-1].get('state') == 'CLOSED':
        raise EventAlreadyClosed()

    project_name = event.get('project_name')
    file_name = file.name.replace(' ', '_').replace('-', '_')
    evidence_id = f'{project_name}-{event_id}-{file_name}'
    full_name = f'{project_name}/{event_id}/{evidence_id}'

    if event_dal.save_evidence(file, full_name):
        success = event_dal.update(event_id, {evidence_type: evidence_id})

    return success


def validate_evidence(evidence_type, file):
    success = False

    if evidence_type == 'evidence':
        allowed_mimes = ['image/gif', 'image/png']
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


def _send_new_event_mail(analyst, event_id, project, subscription, event_type):
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

    email_context = {
        'analyst_email': analyst,
        'event_id': event_id,
        'event_url': (
            'https://fluidattacks.com/integrates/dashboard#!/'
            f'project/{project}/events/{event_id}'),
        'project_name': project
    }
    email_send_thread = threading.Thread(
        name='New event email thread',
        target=send_mail_new_event,
        args=(recipients, email_context))
    email_send_thread.start()


def create_event(analyst_email, project_name, file=None, image=None, **kwargs):
    event_id = str(random.randint(10000000, 170000000))

    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today()

    project = integrates_dal.get_project_attributes_dynamo(
        project_name, ['companies', 'type'])
    subscription = project.get('type', '')

    event_attrs = kwargs.copy()
    if event_attrs['event_date'].astimezone(tzn).replace(tzinfo=None) > today:
        raise InvalidDate()

    event_attrs.update({
        'accessibility': ' '.join(list(set(event_attrs['accessibility']))),
        'analyst': analyst_email,
        'client': project.get('companies', [''])[0],
        'historic_state': [
            {
                'analyst': analyst_email,
                'date': event_attrs['event_date'].strftime(
                    '%Y-%m-%d %H:%M:%S'),
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
    del event_attrs['event_date']
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


def get_event(event_id):
    event = event_dal.get_event(event_id)
    if not event:
        raise EventNotFound()

    return event


def get_events(event_ids):
    events = [get_event(event_id) for event_id in event_ids]

    return events


def _send_comment_email(content, event_id, parent, user_info):
    event = get_event(event_id)
    project_name = event.get('project_name')
    recipients = [user for user in project_dal.get_users(project_name, True)]
    recipients += FI_MAIL_REPLYERS.split(',')

    email_context = {
        'comment': content.replace('\n', ' '),
        'comment_type': 'event',
        'comment_url': (
            'https://fluidattacks.com/integrates/dashboard#!/'
            f'project/{project_name}/events/{event_id}/comments'),
        'finding_id': event_id,
        'finding_name': f'Event #{event_id}',
        'parent': parent,
        'project': project_name,
        'user_email': user_info['user_email']
    }

    email_send_thread = threading.Thread(
        name='Event comment email thread',
        target=send_mail_comment,
        args=(recipients, email_context))
    email_send_thread.start()


def add_comment(content, event_id, parent, user_info):
    success = comment_domain.create(
        'event', content, event_id, parent, user_info)

    if success:
        _send_comment_email(content, event_id, parent, user_info)

    return success


def get_evidence_link(event_id, file_name):
    project_name = get_event(event_id).get('project_name')
    file_url = f'{project_name}/{event_id}/{file_name}'
    minutes_until_expire = 1.0 / 6

    return resources_domain.sign_url(
        FI_CLOUDFRONT_RESOURCES_DOMAIN, file_url, minutes_until_expire)
