""" GraphQL Entity for Events """
# pylint: disable=no-self-use
from graphene import Boolean, Field, Mutation, ObjectType, String

from app import util
from app.decorators import require_login, require_role, require_event_access
from app.domain import event as event_domain


class Event(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """ Formstack Events Class """
    id = String()  # noqa pylint: disable=invalid-name
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
    evidence_file = String()

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

    def resolve_evidence_file(self, info):
        """ Resolve evidence file attribute """
        del info
        return self.evidence_file


class UpdateEvent(Mutation):
    """Update event status."""

    class Arguments:
        event_id = String(required=True)
        affectation = String(required=True)
    success = Boolean()
    event = Field(Event)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_event_access
    def mutate(self, info, event_id, affectation):
        success = event_domain.update_event(event_id, affectation, info)
        if success:
            project_name = event_domain.get_event_project_name(event_id)
            util.invalidate_cache(event_id)
            util.invalidate_cache(project_name)
        events_loader = info.context.loaders['event']

        ret = UpdateEvent(success=success, event=events_loader.load(event_id))
        return ret
