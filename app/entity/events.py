""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import

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
    projectName = String()
    clientProject = String()
    detail = String()
    evidence = String()
    eventType = String()
    date = String()
    status = String()
    affectation = String()
    accessibility = String()
    affectedComponents = String()
    context = String()
    subscription = String()

    def __init__(self, identifier):
        """ Class constructor """
        self.id = ''
        self.analyst = ''
        self.client = ''
        self.projectName = ''
        self.clientProject = ''
        self.eventType = ''
        self.date = ''
        self.detail = ''
        self.affectation = ''
        self.status = ''
        self.evidence = ''
        self.accessibility = ''
        self.affectedComponents = ''
        self.context = ''
        self.subscription = ''

        event_id = str(identifier)
        resp = event_data(event_id)

        if resp:
            self.id = event_id
            self.analyst = resp.get('analyst')
            self.client = resp.get('client')
            self.projectName = resp.get('projectName')
            self.clientProject = resp.get('clientProject')
            self.eventType = resp.get('eventType')
            self.date = resp.get('date')
            self.detail = resp.get('detail')
            self.affectation = resp.get('affectation')
            self.status = resp.get('status')
            self.evidence = resp.get('evidence')
            self.accessibility = resp.get('accessibility')
            self.affectedComponents = resp.get('affectedComponents')
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

    def resolve_projectName(self, info):
        """ Resolve projectName attribute """
        del info
        return self.projectName

    def resolve_projectByCustomer(self, info):
        """ Resolve clientProject attribute """
        del info
        return self.clientProject

    def resolve_eventType(self, info):
        """ Resolve eventType attribute """
        del info
        return self.eventType

    def resolve_detail(self, info):
        """ Resolve detail attribute """
        del info
        return self.detail

    def resolve_date(self, info):
        """ Resolve date attribute """
        del info
        return self.date

    def resolve_status(self, info):
        """ Resolve status attribute """
        del info
        return self.status

    def resolve_affectation(self, info):
        """ Resolve affectation attribute """
        del info
        return self.affectation

    def resolve_accessibility(self, info):
        """ Resolve accessibility attribute """
        del info
        return self.accessibility

    def resolve_affectedComponents(self, info):
        """ Resolve affected components attribute """
        del info
        return self.affectedComponents

    def resolve_context(self, info):
        """ Resolve context attribute """
        del info
        return self.context
        
    def resolve_subscription(self, info):
        """ Resolve subscription attribute """
        del info
        return self.subscription
