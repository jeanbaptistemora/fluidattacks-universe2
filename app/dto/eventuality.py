# coding=utf-8
""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level

from __future__ import absolute_import
import os
import rollbar
import boto3
from django.conf import settings
from magic import Magic
from botocore.exceptions import ClientError
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from app.dal.helpers.drive import DriveAPI
from ..dal import integrates_dal
from ..dal.helpers.formstack import FormstackAPI
from ..utils import forms
from .. import util

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

BUCKET_S3 = FI_AWS_S3_BUCKET


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
    EVIDENCE_FILE = FIELDS_EVENT['EVIDENCE_FILE']

    def __init__(self):
        """Class constructor."""
        self.request_id = None
        self.data = dict()

    def parse(self, submission_id, request_arr):
        """Parse event data."""
        self.data = dict()
        self.data['id'] = submission_id
        report_title = 'report_date'
        report_date = integrates_dal.get_event_attributes_dynamo(
            str(submission_id),
            report_title)
        if report_date:
            self.data['reportDate'] = report_date.get('report_date')
        else:
            self.data['reportDate'] = request_arr['timestamp']
        self.data = forms.dict_concatenation(
            self.data, self.parse_event(request_arr))
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
            self.CLOSER: 'closer',
            self.EVIDENCE_FILE: 'evidenceFile'
        }
        parsed_dict = {v: initial_dict[k]
                       for (k, v) in event_fields.items()
                       if k in initial_dict.keys()}
        if parsed_dict.get('evidence'):
            parsed_dict['evidence'] = \
                forms.drive_url_filter(parsed_dict['evidence'])
        else:
            # Event does not have evidences
            pass
        if parsed_dict.get('evidenceFile'):
            parsed_dict['evidenceFile'] = \
                forms.drive_url_filter(parsed_dict['evidenceFile'])
        else:
            # Event does not have evidence file
            pass
        parsed_dict = cast_event_attributes(parsed_dict)
        return parsed_dict


def cast_event_attributes(event):
    cast_event_field = {
        'Pendiente': 'UNSOLVED',
        'Tratada': 'SOLVED',
        'Puntual': 'ONESHOT',
        'Continua': 'CONTINUOUS',
        'Autorización para ataque especial':
            'AUTHORIZATION_SPECIAL_ATTACK',
        'Alcance difiere a lo aprobado':
            'TOE_DIFFERS_APPROVED',
        'Aprobación de alta disponibilidad': 'HIGH_AVAILABILITY_APPROVAL',
        'Insumos incorrectos o faltantes': 'INCORRECT_MISSING_SUPPLIES',
        'Cliente suspende explicitamente':
            'CLIENT_EXPLICITLY_SUSPENDS_PROJECT',
        'Cliente aprueba cambio de alcance':
            'CLIENT_APPROVES_CHANGE_TOE',
        'Cliente cancela el proyecto/hito':
            'CLIENT_CANCELS_PROJECT_MILESTONE',
        'Cliente detecta ataque': 'CLIENT_DETECTS_ATTACK',
        'Otro': 'OTHER',
        'FLUID': 'FLUID',
        'Cliente': 'CLIENT',
        'Tele-trabajo': 'TELECOMMUTING',
        'Planeación': 'PLANNING',
        'Probar otra parte del ToE': 'TEST_OTHER_PART_TOE',
        'Documentar el proyecto': 'DOCUMENT_PROJECT',
        'Ninguna': 'NONE',
        'Ejecutar otro proyecto del mismo cliente':
            'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
        'Ejecutar otro proyecto de otro cliente':
            'EXECUTE_OTHER_PROJECT_OTHER_CLIENT',
        'Entrenar': 'TRAINING'
    }
    list_fields = ['eventStatus', 'subscription', 'eventType', 'context',
                   'actionBeforeBlocking', 'actionAfterBlocking']
    for field in list_fields:
        if event.get(field):
            event[field] = cast_event_field.get(
                event.get(field).encode('utf-8'), '')
    return event


def parse_event_dynamo(submission_id):
    """Parse event data."""
    event_headers = [
        'analyst', 'client', 'project_name', 'client_project', 'report_date',
        'event_type', 'detail', 'event_date', 'event_status', 'affectation',
        'evidence', 'accessibility', 'affected_components', 'subscription',
        'context', 'client_responsible', 'hours_before_blocking', 'event_id',
        'action_before_blocking', 'action_after_blocking', 'closer',
        'evidence_file']
    event_title = ','.join(event_headers)
    event = integrates_dal.get_event_attributes_dynamo(
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
    """Get event data."""
    event = []
    event_title = 'event_date'
    event = integrates_dal.get_event_attributes_dynamo(
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
            migrate_event_files(event_parsed)
        else:
            rollbar.report_message(
                'Error: An error occurred catching event', 'error')
    return event_parsed


def migrate_event(event):
    """Migrate event to dynamo."""
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
        'action_before_blocking', 'action_after_blocking', 'closer',
        'evidence_file']
    event_attributes = {k: event.get(util.snakecase_to_camelcase(k))
                        for k in event_fields
                        if event.get(util.snakecase_to_camelcase(k))}
    response = integrates_dal.add_multiple_attributes_dynamo(
        'fi_events', primary_keys, event_attributes)
    return response


def migrate_event_files(event):
    """Migrate event files to s3."""
    project_name = event.get('projectName').lower()
    event_id = event.get('id')
    evidence_id = event.get('evidence')
    evidence_file = event.get('evidenceFile')
    files = [
        {'id': evidence_id,
            'file_type': {'image/jpeg': '.jpeg',
                          'image/gif': '.gif',
                          'image/png': '.png'}},
        {'id': evidence_file,
            'file_type': {'application/zip': '.zip',
                          'text/plain': '.csv',
                          'text/csv': '.csv',
                          'application/pdf': '.pdf',
                          'application/vnd.ms-office': '.xls'}}
    ]
    for curr_file in files:
        if curr_file.get('id'):
            file_name = '{project_name}/{event_id}/{file_id}'.format(
                project_name=project_name,
                event_id=event_id,
                file_id=curr_file['id'])
            folder = util.list_s3_objects(CLIENT_S3, BUCKET_S3, file_name)
            migrate_event_files_aux(curr_file, file_name, event_id, folder)
        else:
            # Event does not have evidences
            pass


def migrate_event_files_aux(curr_file, file_name, event_id, folder):
    """Migrate event files auxiliar."""
    if folder:
        # File exist in s3
        pass
    else:
        fileroute = '/tmp/:id.tmp'.replace(':id', curr_file['id'])
        if os.path.exists(fileroute):
            send_file_to_s3(file_name, curr_file, event_id)
        else:
            drive_api = DriveAPI()
            file_download_route = drive_api.download(
                curr_file['id'])
            if file_download_route:
                send_file_to_s3(file_name, curr_file, event_id)
            else:
                rollbar.report_message(
                    'Error: An error occurred downloading \
                    file from Drive', 'error')


def send_file_to_s3(file_name, evidence, event_id):
    """Save evidence files in s2."""
    evidence_id = evidence['id']
    fileroute = '/tmp/:id.tmp'.replace(':id', evidence_id)
    evidence_type = evidence['file_type']
    is_file_saved = False
    with open(fileroute, 'r') as file_obj:
        try:
            mime = Magic(mime=True)
            mime_type = mime.from_file(fileroute)
            if evidence_type.get(mime_type):
                file_name_s3 = file_name + evidence_type.get(mime_type)
                CLIENT_S3.upload_fileobj(file_obj, BUCKET_S3, file_name_s3)
                is_file_saved = True
            else:
                util.cloudwatch_log_plain(
                    'File of event {event_id} does not have the right type'
                    .format(event_id=event_id)
                )
        except ClientError:
            rollbar.report_exc_info()
            is_file_saved = False
    os.unlink(fileroute)
    return is_file_saved
