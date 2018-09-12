""" GraphQL Entity for Formstack Events """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import urlparse
from .. import util
from app.api.formstack import FormstackAPI
from app.dto.eventuality import EventualityDTO
from graphene import String, ObjectType, Boolean
from ..services import has_access_to_finding

class Events(ObjectType):
    """ Formstack Events Class """
    id = String()
    analyst = String()
    client = String()
    fluidProject = String()
    clientProject = String()
    detail = String()
    evidence = String()
    type = String()
    date = String()
    status = String()
    affectation = String()
    access = Boolean()

    def __init__(self, info, identifier):
        """ Class constructor """
        self.access = False
        self.id = ""
        self.analyst, self.client = "", ""
        self.fluidProject, self.clientProject = "", ""
        self.type, self.date = "", ""
        self.detail, self.affectation = "", ""
        self.status, self.evidence = "", ""

        event_id = str(identifier)
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_finding(
                info.context.session['access'],
                event_id,
                info.context.session['role'])):
            self.access = True
            resp = FormstackAPI().get_submission(event_id)
            if resp:
                evt_dto = EventualityDTO()
                evt_set = evt_dto.parse(event_id, resp)
                self.id = event_id
                if "analyst" in evt_set:
                    self.analyst = evt_set['analyst']
                if "client" in evt_set:
                    self.client = evt_set['client']
                if "fluidProject" in evt_set:
                    self.fluidProject = evt_set["fluidProject"]
                if "clientProject" in evt_set:
                    self.clientProject = evt_set["clientProject"]
                if "type" in evt_set:
                    self.type = evt_set["type"]
                if "detalle" in evt_set:
                    self.detail = evt_set["detalle"]
                if "fecha" in evt_set:
                    self.date = evt_set["fecha"]
                if "estado" in evt_set:
                    self.status = evt_set["estado"]
                if "evidence" in evt_set  and ".png" in evt_set['evidence']:
                    parsed_url = urlparse.urlparse(evt_set['evidence'])
                    self.evidence = urlparse.parse_qs(parsed_url.query)['id'][0]
                if "affectation" in evt_set:
                    self.affectation = evt_set["affectation"]
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve event info without permission')


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

    def resolve_projectByFluid(self, info):
        """ Resolve fluidProject attribute """
        del info
        return self.fluidProject

    def resolve_projectByCustomer(self, info):
        """ Resolve clientProject attribute """
        del info
        return self.clientProject

    def resolve_type(self, info):
        """ Resolve type attribute """
        del info
        return self.type

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
        """ Resolve status attribute """
        del info
        return self.affectation

    def resolve_access(self, info):
        """ Resolve access attribute """
        del info
        return self.access
