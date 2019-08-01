"""Domain functions for events."""

import rollbar
from app.dao import integrates_dao
from app import util
from app.dao.helpers.formstack import FormstackAPI
from app.dto.eventuality import EventDTO


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
        event_migrated = integrates_dao.add_multiple_attributes_dynamo(
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
    project = integrates_dao.get_event_project(event_id)
    if not project:
        api = FormstackAPI()
        evt_dto = EventDTO()
        event_data = evt_dto.parse(event_id, api.get_submission(event_id))
        project = event_data.get('projectName', '')
    else:
        # Project exist in dynamo
        pass
    return project
