""" GraphQL Entity for Formstack Eventuality """
# pylint: disable=F0401
from app.api.formstack import FormstackAPI
from app.dto.eventuality import EventualityDTO
from graphene import String, ObjectType


class Eventuality(ObjectType):
    """ Formstack Eventuality Class """
    id = String()
    analyst = String()
    customer = String()
    projectByFluid = String()
    projectByCustomer = String()
    detail = String()
    type = String()
    date = String()
    status = String()
    affectation = String()

    def __init__(self, submit_id):
        """ Class constructor """
        self.id = submit_id
        self.analyst, self.customer = "", ""
        self.projectByFluid, self.projectByCustomer = "", ""
        self.type, self.date = "", ""
        self.detail, self.affectation = "", ""
        self.status = ""
        event_id = str(submit_id)
        resp = FormstackAPI().get_submission(event_id)
        if resp:
            evt_dto = EventualityDTO()
            evt_set = evt_dto.parse(event_id, resp)
            if "analyst" in evt_set:
                self.analyst = evt_set['analyst']
            if "client" in evt_set:
                self.customer = evt_set['client']
            if "fluidProject" in evt_set:
                self.projectByFluid = evt_set["fluidProject"]
            if "clientProject" in evt_set:
                self.projectByCustomer = evt_set["clientProject"]
            if "type" in evt_set:
                self.type = evt_set["type"]
            if "detalle" in evt_set:
                self.detail = evt_set["detalle"]
            if "fecha" in evt_set:
                self.date = evt_set["fecha"]
            if "estado" in evt_set:
                self.status = evt_set["estado"]
            if "affectation" in evt_set:
                self.affectation = evt_set["affectation"]

    def resolve_id(self, info):
        """ Resolve id attribute """
        del info
        return self.id

    def resolve_analyst(self, info):
        """ Resolve analyst attribute """
        del info
        return self.analyst

    def resolve_customer(self, info):
        """ Resolve customer attribute """
        del info
        return self.customer

    def resolve_projectByFluid(self, info):
        """ Resolve projectByFluid attribute """
        del info
        return self.projectByFluid

    def resolve_projectByCustomer(self, info):
        """ Resolve projectByCustomer attribute """
        del info
        return self.projectByCustomer

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
