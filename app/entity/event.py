""" GraphQL Entity for Events """
from graphene import (
    Argument, Boolean, DateTime, Enum, Field, Int, List, Mutation, ObjectType,
    String
)

from app import util
from app.decorators import (
    require_login, require_role, require_event_access, require_project_access
)
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

    class Arguments():
        event_id = String(required=True)
        affectation = String(required=True)
    success = Boolean()
    event = Field(Event)

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin'])
    @require_event_access
    def mutate(_, info, event_id, affectation):
        success = event_domain.update_event(event_id, affectation, info)
        if success:
            project_name = event_domain.get_event_project_name(event_id)
            util.invalidate_cache(event_id)
            util.invalidate_cache(project_name)
        events_loader = info.context.loaders['event']

        ret = UpdateEvent(success=success, event=events_loader.load(event_id))
        return ret


class CreateEvent(Mutation):
    """Creates a new event"""

    class Arguments():
        action_after_blocking = Argument(
            Enum('ActionsAfterBlocking', [
                (
                    'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
                    'EXECUTE_OTHER_PROJECT_SAME_CLIENT'
                ),
                (
                    'EXECUTE_OTHER_PROJECT_OTHER_CLIENT',
                    'EXECUTE_OTHER_PROJECT_OTHER_CLIENT'
                ),
                ('NONE', 'NONE'),
                ('OTHER', 'OTHER'),
                ('TRAINING', 'TRAINING')
            ]), required=True)
        action_before_blocking = Argument(
            Enum('ActionsBeforeBlocking', [
                ('DOCUMENT_PROJECT', 'DOCUMENT_PROJECT'),
                ('NONE', 'NONE'),
                ('OTHER', 'OTHER'),
                ('TEST_OTHER_PART_TOE', 'TEST_OTHER_PART_TOE')
            ]), required=True)
        accessibility = Argument(
            List(Enum('EventAccessibility', [
                ('ENVIRONMENT', 'Ambiente'),
                ('REPOSITORY', 'Repositorio')
            ])), required=True)
        affected_components = Argument(
            List(Enum('AffectedComponents', [
                ('FLUID_STATION', 'Estación de pruebas de FLUID'),
                ('CLIENT_STATION', 'Estación de pruebas del Cliente'),
                ('TOE_EXCLUSSION', 'Exclusión de alcance'),
                ('DOCUMENTATION', 'Documentación del proyecto'),
                ('LOCAL_CONNECTION', 'Conectividad local (LAN, WiFi)'),
                ('INTERNET_CONNECTION', 'Conectividad a Internet'),
                ('VPN_CONNECTION', 'Conectividad VPN'),
                ('TOE_LOCATION', 'Ubicación del ToE (IP, URL)'),
                ('TOE_CREDENTIALS', 'Credenciales en el ToE'),
                ('TOE_PRIVILEGES', 'Privilegios en el ToE'),
                ('TEST_DATA', 'Datos de prueba'),
                ('TOE_UNSTABLE', 'Inestabilidad del ToE'),
                ('TOE_UNACCESSIBLE', 'Inaccesibilidad del ToE'),
                ('TOE_UNAVAILABLE', 'Indisponibilidad del ToE'),
                ('TOE_ALTERATION', 'Alteración del ToE'),
                ('SOURCE_CODE', 'Código fuente'),
                ('COMPILE_ERROR', 'Error en compilación'),
                ('OTHER', 'Otro(s)'),
            ])), required=False)
        blocking_hours = Int(required=False)
        client_responsible = String(required=True)
        context = Argument(
            Enum('EventContext', [
                ('CLIENT', 'CLIENT'),
                ('FLUID', 'FLUID'),
                ('OTHER', 'OTHER'),
                ('PLANNING', 'PLANNING'),
                ('TELECOMMUTING', 'TELECOMMUTING')
            ]), required=True)
        detail = String(required=True)
        event_date = DateTime(required=True)
        event_type = Argument(
            Enum('EventType', [
                (
                    'AUTHORIZATION_SPECIAL_ATTACK',
                    'AUTHORIZATION_SPECIAL_ATTACK'
                ),
                ('CLIENT_APPROVES_CHANGE_TOE', 'CLIENT_APPROVES_CHANGE_TOE'),
                (
                    'CLIENT_CANCELS_PROJECT_MILESTONE',
                    'CLIENT_CANCELS_PROJECT_MILESTONE'
                ),
                ('CLIENT_DETECTS_ATTACK', 'CLIENT_DETECTS_ATTACK'),
                (
                    'CLIENT_EXPLICITLY_SUSPENDS_PROJECT',
                    'CLIENT_EXPLICITLY_SUSPENDS_PROJECT'
                ),
                ('HIGH_AVAILABILITY_APPROVAL', 'HIGH_AVAILABILITY_APPROVAL'),
                ('INCORRECT_MISSING_SUPPLIES', 'INCORRECT_MISSING_SUPPLIES'),
                ('OTHER', 'OTHER'),
                ('TOE_DIFFERS_APPROVED', 'TOE_DIFFERS_APPROVED')
            ]), required=True)
        project_name = String(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin'])
    @require_project_access
    def mutate(_, info, project_name, **kwargs):
        analyst_email = util.get_jwt_content(info.context)['user_email']

        success = event_domain.create_event(
            analyst_email, project_name.lower(), **kwargs)
        if success:
            util.cloudwatch_log(info.context, f'Security: Created event in '
                                '{project_name} project succesfully')
            util.invalidate_cache(project_name)

        return CreateEvent(success=success)
