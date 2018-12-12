""" GraphQL Entity for Formstack Events """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

from graphene import String, ObjectType

from app.api.formstack import FormstackAPI
from app.dto import eventuality

class Events(ObjectType):
    """ Formstack Events Class """
    id = String()
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

    def __init__(self, identifier):
        """ Class constructor """
        self.id = str(identifier)
        self.analyst, self.client = '', ''
        self.projectName, self.clientProject = '', ''
        self.eventType, self.date = '', ''
        self.detail, self.affectation = '', ''
        self.status, self.evidence = '', ''
        self.accessibility, self.affectedComponents = '', ''

        resp = FormstackAPI().get_submission(self.id)

        if resp:
            evt_set = eventuality.parse(self.id, resp)
            if 'analyst' in evt_set:
                self.analyst = evt_set['analyst']
            if 'client' in evt_set:
                self.client = evt_set['client']
            if 'projectName' in evt_set:
                self.projectName = evt_set['projectName']
            if 'clientProject' in evt_set:
                self.clientProject = evt_set['clientProject']
            if 'eventType' in evt_set:
                self.eventType = evt_set['eventType']
            if 'detail' in evt_set:
                self.detail = evt_set['detail']
            if 'date' in evt_set:
                self.date = evt_set['date']
            if 'status' in evt_set:
                self.status = evt_set['status']
            if 'evidence' in evt_set  and '.png' in evt_set['evidence']:
                parsed_url = urlparse(evt_set['evidence'])
                self.evidence = parse_qs(parsed_url.query)['id'][0]
            if 'affectation' in evt_set:
                self.affectation = evt_set['affectation']
            if 'accessibility' in evt_set:
                self.accessibility = evt_set['accessibility']
            if 'affectedComponents' in evt_set:
                self.affectedComponents = evt_set['affectedComponents']

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
