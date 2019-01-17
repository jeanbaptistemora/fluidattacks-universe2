""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

import boto3
from graphene import String, ObjectType, Boolean

from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from app.dto.eventuality import event_data

client_s3 = boto3.client('s3',
                            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = FI_AWS_S3_BUCKET

class Events(ObjectType):
    """ Formstack Events Class """
    id = String()
    success = Boolean()
    error_message = String()
    analyst = String()
    client = String()
    project_name = String()
    client_project = String()
    detail = String()
    evidence = String()
    event_type = String()
    event_date = String()
    event_status = String()
    affectation = String()
    accessibility = String()
    affected_components = String()
    context = String()
    subscription = String()

    def __init__(self, identifier):
        """ Class constructor """
        self.id = ''
        self.analyst = ''
        self.client = ''
        self.project_name = ''
        self.client_project = ''
        self.event_type = ''
        self.event_date = ''
        self.detail = ''
        self.affectation = ''
        self.event_status = ''
        self.evidence = ''
        self.accessibility = ''
        self.affected_components = ''
        self.context = ''
        self.subscription = ''

        event_id = str(identifier)
        resp = event_data(event_id)

        if resp:
            self.id = event_id
            self.analyst = resp.get('analyst')
            self.client = resp.get('client')
            self.project_name = resp.get('projectName')
            self.client_project = resp.get('clientProject')
            self.event_type = resp.get('eventType')
            self.event_date = resp.get('eventDate')
            self.detail = resp.get('detail')
            self.affectation = resp.get('affectation')
            self.event_status = resp.get('eventStatus')
            if resp.get('evidence'):
                parsedUrl = urlparse(resp.get('evidence'))
                self.evidence = parse_qs(parsedUrl.query)['id'][0]
            self.accessibility = resp.get('accessibility')
            self.affected_components = resp.get('affectedComponents')
            self.context = resp.get('context')
            self.subscription = resp.get('subscription')
        else:
            self.success = False
            self.error_message = 'Finding does not exist'
        self.success = True

    def resolve_id(self, info):
        """ Resolve id attribute """
        del info
        return self.id

    def resolve_analyst(self, info):
        """ Resolve analyst attribute """
        del info
        return self.analyst

    def resolve_client(self, info):
        """ Resolve client attribute """
        del info
        return self.client

    def resolve_evidence(self, info):
        """ Resolve evidence attribute """
        del info
        return self.evidence

    def resolve_project_name(self, info):
        """ Resolve project_name attribute """
        del info
        return self.project_name

    def resolve_client_project(self, info):
        """ Resolve client_project attribute """
        del info
        return self.client_project

    def resolve_event_type(self, info):
        """ Resolve event_type attribute """
        del info
        return self.event_type

    def resolve_detail(self, info):
        """ Resolve detail attribute """
        del info
        return self.detail

    def resolve_event_date(self, info):
        """ Resolve date attribute """
        del info
        return self.event_date

    def resolve_event_status(self, info):
        """ Resolve status attribute """
        del info
        return self.event_status

    def resolve_affectation(self, info):
        """ Resolve affectation attribute """
        del info
        return self.affectation

    def resolve_accessibility(self, info):
        """ Resolve accessibility attribute """
        del info
        return self.accessibility

    def resolve_affected_components(self, info):
        """ Resolve affected components attribute """
        del info
        return self.affected_components

    def resolve_context(self, info):
        """ Resolve context attribute """
        del info
        return self.context
        
    def resolve_subscription(self, info):
        """ Resolve subscription attribute """
        del info
        return self.subscription
