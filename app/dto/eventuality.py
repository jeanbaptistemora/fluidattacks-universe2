""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level

import rollbar
from django.conf import settings

from ..dao import integrates_dao
from ..api.formstack import FormstackAPI
from ..utils import forms
from .. import util


class EventDTO(object):
    """Class to create an object with the attributes of an event."""

    FIELDS_EVENT = settings.FIELDS_EVENT
    ANALYST = FIELDS_EVENT['ANALYST']
    CLIENT = FIELDS_EVENT['CLIENT']
    PROJECT_NAME = FIELDS_EVENT['PROJECT_NAME']
    CLIENT_PROJECT = FIELDS_EVENT['CLIENT_PROJECT']
    EVENT_TYPE = FIELDS_EVENT['EVENT_TYPE']
    DETAIL = FIELDS_EVENT['DETAIL']
    EVENT_DATE = FIELDS_EVENT['EVENT_DATE']
    EVENT_STATUS = FIELDS_EVENT['EVENT_STATUS']
    AFFECTATION = FIELDS_EVENT['AFFECTATION']
    EVIDENCE = FIELDS_EVENT['EVIDENCE']
    ACCESSIBILITY = FIELDS_EVENT['ACCESSIBILITY']
    AFFECTED_COMPONENTS = FIELDS_EVENT['AFFECTED_COMPONENTS']
    SUBSCRIPTION = FIELDS_EVENT['SUBSCRIPTION']
    CONTEXT = FIELDS_EVENT['CONTEXT']
    CLIENT_RESPONSIBLE = FIELDS_EVENT['CLIENT_RESPONSIBLE']
    HOURS_BEFORE_BLOCKING = FIELDS_EVENT['HOURS_BEFORE_BLOCKING']
    ACTION_BEFORE_BLOCKING = FIELDS_EVENT['ACTION_BEFORE_BLOCKING']
    ACTION_AFTER_BLOCKING = FIELDS_EVENT['ACTION_AFTER_BLOCKING']
    CLOSER = FIELDS_EVENT['CLOSER']

    def __init__(self):
        """Class constructor."""
        self.request_id = None
        self.data = dict()

    def parse(self, submission_id, request_arr):
        """Parse event data."""
        self.data = dict()
        self.data['id'] = submission_id
        report_title = 'report_date'
        report_date = integrates_dao.get_event_attributes_dynamo(
            str(submission_id),
            report_title)
        if report_date:
            self.data['reportDate'] = report_date.get('report_date')
        else:
            self.data['reportDate'] = request_arr['timestamp']
        self.data = forms.dict_concatenation(self.data, self.parse_event(request_arr))
        return self.data

    def parse_event(self, request_arr):
        """Convert the data of an event into a formstack."""
        initial_dict = forms.create_dict(request_arr)
        event_fields = {
            self.ANALYST: 'analyst',
            self.CLIENT: 'client',
            self.PROJECT_NAME: 'projectName',
            self.CLIENT_PROJECT: 'clientProject',
            self.EVENT_TYPE: 'eventType',
            self.DETAIL: 'detail',
            self.EVENT_DATE: 'eventDate',
            self.EVENT_STATUS: 'eventStatus',
            self.AFFECTATION: 'affectation',
            self.EVIDENCE: 'evidence',
            self.ACCESSIBILITY: 'accessibility',
            self.AFFECTED_COMPONENTS: 'affectedComponents',
            self.SUBSCRIPTION: 'subscription',
            self.CONTEXT: 'context',
            self.CLIENT_RESPONSIBLE: 'clientResponsible',
            self.HOURS_BEFORE_BLOCKING: 'hoursBeforeBlocking',
            self.ACTION_BEFORE_BLOCKING: 'actionBeforeBlocking',
            self.ACTION_AFTER_BLOCKING: 'actionAfterBlocking',
            self.CLOSER: 'closer'
        }
        parsed_dict = {v: initial_dict[k]
                       for (k, v) in event_fields.items()
                       if k in initial_dict.keys()}
        if parsed_dict.get('evidence'):
            parsed_dict['evidence'] = forms.drive_url_filter(parsed_dict['evidence'])
        else:
            # Event does not have evidences
            pass
        return parsed_dict

    def to_formstack(self, data):
        new_data = dict()
        for key, value in data.items():
            new_data["field_" + str(key)] = value
        return new_data


def parse_event_dynamo(submission_id):
    event_headers = [
        'analyst', 'client', 'project_name', 'client_project', 'report_date',
        'event_type', 'detail', 'event_date', 'event_status', 'affectation',
        'evidence', 'accessibility', 'affected_components', 'subscription',
        'context', 'client_responsible', 'hours_before_blocking', 'event_id',
        'action_before_blocking', 'action_after_blocking', 'closer']
    event_title = ','.join(event_headers)
    event = integrates_dao.get_event_attributes_dynamo(
        submission_id,
        event_title)
    parsed_dict = {}
    if event:
        event_fields = {k: util.snakecase_to_camelcase(k)
                        for k in event_headers}
        parsed_dict = {v: event[k]
                       for (k, v) in event_fields.items()
                       if k in event.keys()}
        parsed_dict['id'] = event.get('event_id')
    else:
        util.cloudwatch_log_plain(
            'Event {submission_id} does not have data in dynamo'.format(
                submission_id=submission_id)
        )
    return parsed_dict


def event_data(submission_id):
    event = []
    event_title = 'event_date'
    event = integrates_dao.get_event_attributes_dynamo(
        submission_id,
        event_title)
    if event:
        event_parsed = parse_event_dynamo(submission_id)
    else:
        ev_dto = EventDTO()
        api = FormstackAPI()
        if str(submission_id).isdigit() is True:
            event_parsed = ev_dto.parse(
                submission_id,
                api.get_submission(submission_id)
            )
            migrate_event(event_parsed)
        else:
            rollbar.report_message('Error: An error occurred catching event', 'error')
    return event_parsed


def migrate_event(event):
    primary_keys = ['event_id', str(event['id'])]
    if event.get('projectName'):
        event['projectName'] = event['projectName'].lower()
    else:
        # Event does not have project name
        pass
    event_fields = [
        'analyst', 'client', 'project_name', 'client_project', 'report_date',
        'event_type', 'detail', 'event_date', 'event_status', 'affectation',
        'evidence', 'accessibility', 'affected_components', 'subscription',
        'context', 'client_responsible', 'hours_before_blocking',
        'action_before_blocking', 'action_after_blocking', 'closer']
    event_data = {k: event.get(util.snakecase_to_camelcase(k))
                  for k in event_fields
                  if event.get(util.snakecase_to_camelcase(k))}
    response = integrates_dao.add_multiple_attributes_dynamo('fi_events', primary_keys, event_data)
    return response
