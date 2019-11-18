"""Domain functions for events."""
import random
import threading
from datetime import datetime

import pytz
from django.conf import settings

import rollbar

from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PRODUCTION, FI_MAIL_PROJECTS, FI_MAIL_REPLYERS
)
from app import util
from app.dal import integrates_dal, event as event_dal, project as project_dal
from app.dal.helpers.formstack import FormstackAPI
from app.domain import comment as comment_domain
from app.dto.eventuality import EventDTO, migrate_event
from app.exceptions import EventNotFound, InvalidFileSize, InvalidFileType
from app.mailer import send_mail_comment, send_mail_new_event


def update_event(event_id, affectation, info):
    """Update an event associated to a project."""
    request = info.context
    event_data = {}
    has_error = False
    updated = False
    if affectation.isdigit():
        if int(affectation) >= 0:
            event_data['event_status'] = 'SOLVED'
        else:
            rollbar.report_message(
                'Error: Affectation can not be a negative number', 'error',
                request)
            has_error = True
    else:
        rollbar.report_message(
            'Error: Affectation must be a number', 'error', request)
        has_error = True
    if has_error:
        # Couldn't update the eventuality because it has error
        pass
    else:
        event_data['affectation'] = affectation
        primary_keys = ['event_id', event_id]
        table_name = 'fi_events'
        closer = util.get_jwt_content(info.context)['user_email']
        event_data['closer'] = closer
        event_migrated = integrates_dal.add_multiple_attributes_dynamo(
            table_name, primary_keys, event_data)
        if event_migrated:
            updated = True
        else:
            rollbar.report_message(
                'Error: An error ocurred updating event', 'error', request)
            has_error = True
    if has_error and not updated:
        resp = False
    else:
        resp = True
    return resp


def get_event_project_name(event_id):
    """Get the name of the project of a finding."""
    project = integrates_dal.get_event_project(event_id)
    if not project:
        api = FormstackAPI()
        evt_dto = EventDTO()
        event_data = evt_dto.parse(event_id, api.get_submission(event_id))
        project = event_data.get('projectName', '')
    else:
        # Project exist in dynamo
        pass
    return project


def update_evidence(event_id, evidence_type, file):
    success = False

    if evidence_type == 'IMAGE':
        allowed_mimes = ['image/gif', 'image/png']
        attribute = 'evidence'
    else:
        allowed_mimes = [
            'application/pdf', 'application/zip', 'text/csv', 'text/plain']
        attribute = 'evidence_file'

    if util.assert_uploaded_file_mime(file, allowed_mimes):
        mib = 1048576

        if file.size < 10 * mib:
            event = get_event(event_id)
            project_name = event.get('project_name')
            file_name = file.name.replace(' ', '_').replace('-', '_')
            evidence_id = f'{project_name}-{event_id}-{file_name}'
            full_name = f'{project_name}/{event_id}/{evidence_id}'

            if event_dal.save_evidence(file, full_name):
                success = event_dal.update(event_id, {attribute: evidence_id})
        else:
            raise InvalidFileSize()
    else:
        raise InvalidFileType()

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
    last_fs_id = 550000000
    event_id = str(random.randint(last_fs_id, 1000000000))

    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    project = integrates_dal.get_project_attributes_dynamo(
        project_name, ['companies', 'type'])
    subscription = project.get('type', '')

    event_attrs = kwargs.copy()
    event_attrs.update({
        'accessibility': ' '.join(list(set(event_attrs['accessibility']))),
        'affectation': 0,
        'analyst': analyst_email,
        'client': project.get('companies', [''])[0],
        'event_date': event_attrs['event_date'].strftime('%Y-%m-%d %H:%M:%S'),
        'event_status': 'UNSOLVED',
        'report_date': today,
        'subscription': subscription.upper()
    })
    if 'affected_components' in event_attrs:
        event_attrs['affected_components'] = '\n'.join(
            list(set(event_attrs['affected_components'])))

    success = event_dal.create(event_id, project_name, event_attrs)
    if success:
        if file:
            update_evidence(event_id, 'FILE', file)
        if image:
            update_evidence(event_id, 'IMAGE', image)

        _send_new_event_mail(
            analyst_email, event_id, project_name, subscription,
            event_attrs['event_type'])

    return success


def get_event(event_id):
    event = event_dal.get_event(event_id)
    if not event:
        api = FormstackAPI()
        fs_event = api.get_submission(event_id)
        if 'error' not in fs_event:
            ev_dto = EventDTO()
            migrate_event(ev_dto.parse(event_id, fs_event))
            event = event_dal.get_event(event_id)
        else:
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
