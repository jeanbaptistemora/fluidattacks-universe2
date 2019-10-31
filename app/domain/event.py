"""Domain functions for events."""
import random
from datetime import datetime

import pytz
from django.conf import settings

import rollbar

from app import util
from app.dal import integrates_dal, event as event_dal
from app.dal.helpers.formstack import FormstackAPI
from app.dto.eventuality import EventDTO, migrate_event
from app.exceptions import EventNotFound


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


def create_event(analyst_email, project_name, **kwargs):
    last_fs_id = 550000000
    event_id = str(random.randint(last_fs_id, 1000000000))

    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    project = integrates_dal.get_project_attributes_dynamo(
        project_name, ['companies', 'type'])

    event_attrs = kwargs.copy()
    event_attrs.update({
        'accessibility': ' '.join(list(set(event_attrs['accessibility']))),
        'affectation': 0,
        'analyst': analyst_email,
        'client': project.get('companies', [''])[0],
        'event_date': event_attrs['event_date'].strftime('%Y-%m-%d %H:%M:%S'),
        'event_status': 'UNSOLVED',
        'report_date': today,
        'subscription': project.get('type', '').upper()
    })
    if 'affected_components' in event_attrs:
        event_attrs['affected_components'] = '\n'.join(
            list(set(event_attrs['affected_components'])))

    return event_dal.create(event_id, project_name, event_attrs)


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
