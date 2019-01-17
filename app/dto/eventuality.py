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
    """ Class to create an object with the attributes of an event. """
    FIELDS_EVENT = settings.FIELDS_EVENT
    #Atributos evento
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
        """ Class constructor """
        self.request_id = None
        self.data = dict()

    def parse(self, submission_id, request_arr):
        self.data = dict()
        self.data['id'] = submission_id
        self.data['timestamp'] = request_arr['timestamp']
        self.data = forms.dict_concatenation(self.data, self.parse_event(submission_id, request_arr))
        return self.data

    def parse_event(self, submission_id, request_arr):
        """ Converts the data of an event into a formstack """
        initial_dict = forms.create_dict(request_arr)
        event = integrates_dao.get_event_dynamo(submission_id)
        if event:
            event_title = ['analyst', 'client',
                           'projectName', 'clientProject',
                           'eventType', 'detail',
                           'date', 'status',
                           'affectation', 'evidence',
                           'accessibility', 'affectedComponents',
                           'subscription', 'context']
            event_fields = {util.camelcase_to_snakecase(k): k
                               for k in event_title}
            parsed_dict = {v: event[k]
                           for (k, v) in event_fields.items()
                           if k in event.keys()}
        else:
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
            parsed_dict = {v: initial_dict[k] \
                           for (k, v) in event_fields.items() \
                           if k in initial_dict.keys()}
            return parsed_dict

    def to_formstack(self, data):
        new_data = dict()
        for key, value in data.items():
            new_data["field_"+ str(key)] = value
        return new_data
    
def event_data(submission_id):
    event = []
    ev_dto = EventDTO()
    api = FormstackAPI()
    if str(submission_id).isdigit() is True:
        event = ev_dto.parse(
            submission_id,
            api.get_submission(submission_id)
        )
    else:
        rollbar.report_message('Error: An error occurred catching event', 'error')
        return None
    return event
