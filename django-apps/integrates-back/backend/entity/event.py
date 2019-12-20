from graphene import (
    Argument, Boolean, DateTime, Enum, Int, List, Mutation, ObjectType,
    String
)
from graphene.types.generic import GenericScalar
from graphene_file_upload.scalars import Upload
from backend.domain import comment as comment_domain, event as event_domain
from backend.entity.comment import Comment
from backend.decorators import (
    get_entity_cache, require_login, require_role, require_event_access,
    require_project_access
)
from backend import util


class Event(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """ GraphQL Entity for Events """
    id = String()  # noqa pylint: disable=invalid-name
    analyst = String()
    client = String()
    comments = List(Comment)
    project_name = String()
    client_project = String()
    detail = String()
    evidence = String()
    event_type = String()
    event_date = String()
    event_status = String()
    historic_state = List(GenericScalar)
    affectation = String()
    accessibility = String()
    affected_components = String()
    context = String()
    subscription = String()
    evidence_file = String()

    def __str__(self):
        return self.id + '_event'

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

    @get_entity_cache
    def resolve_comments(self, info):
        """ Resolve comments attribute """
        self.comments = [
            Comment(**comment)
            for comment in comment_domain.get_event_comments(
                self.id, util.get_jwt_content(info.context)['user_role'])]

        return self.comments

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

    def resolve_historic_state(self, info):
        """ Resolve historic state attribute """
        del info
        return self.historic_state

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
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin'])
    @require_event_access
    def mutate(_, info, event_id, **kwargs):
        success = event_domain.update_event(event_id, **kwargs)
        if success:
            project_name = event_domain.get_event(event_id).get('project_name')
            util.invalidate_cache(event_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(
                info.context,
                f'Security: Updated event {event_id} succesfully')

        return UpdateEvent(success=success)


class SolveEvent(Mutation):
    """ Marks an event as solved """
    class Arguments():
        event_id = String(required=True)
        affectation = Int(required=True)
        date = DateTime(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['admin', 'analyst'])
    @require_event_access
    def mutate(_, info, event_id, affectation, date):
        analyst_email = util.get_jwt_content(info.context)['user_email']
        success = event_domain.solve_event(
            event_id, affectation, analyst_email, date)
        if success:
            project_name = event_domain.get_event(event_id).get('project_name')
            util.invalidate_cache(event_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(
                info.context, f'Security: Solved event {event_id} succesfully')
        else:
            util.cloudwatch_log(
                info.context, f'Security: Attempted to solve event {event_id}')

        return SolveEvent(success=success)


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
        file = Upload(required=False)
        image = Upload(required=False)
        project_name = String(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin', 'customeradminfluid'])
    @require_project_access
    def mutate(_, info, project_name, image=None, file=None, **kwargs):
        analyst_email = util.get_jwt_content(info.context)['user_email']
        success = event_domain.create_event(
            analyst_email, project_name.lower(), file, image, **kwargs)

        if success:
            util.cloudwatch_log(info.context, 'Security: Created event in '
                                f'{project_name} project succesfully')
            util.invalidate_cache(project_name)

        return CreateEvent(success=success)


class AddEventComment(Mutation):
    """ Add comment to event """

    class Arguments():
        content = String(required=True)
        event_id = String(required=True)
        parent = String(required=True)
    comment_id = String()
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(_, info, content, event_id, parent):
        user_info = util.get_jwt_content(info.context)
        comment_id, success = event_domain.add_comment(
            content, event_id, parent, user_info)

        if success:
            util.invalidate_cache(event_id)
            util.cloudwatch_log(
                info.context,
                f'Security: Added comment to event {event_id} succesfully')
        else:
            util.cloudwatch_log(
                info.context,
                f'Security: Attempted to add comment in event {event_id}')

        return AddEventComment(success=success, comment_id=comment_id)


class EventEvidenceType(Enum):
    IMAGE = 'evidence'
    FILE = 'evidence_file'


class UpdateEventEvidence(Mutation):
    """Attaches a file as the event evidence """

    class Arguments():
        event_id = String(required=True)
        evidence_type = Argument(EventEvidenceType, required=True)
        file = Upload(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin'])
    @require_event_access
    def mutate(_, info, event_id, evidence_type, file):
        success = False
        if event_domain.validate_evidence(evidence_type, file):
            success = event_domain.update_evidence(
                event_id, evidence_type, file)
        if success:
            util.invalidate_cache(event_id)
            util.cloudwatch_log(
                info.context,
                f'Security: Updated evidence in event {event_id} succesfully')
        else:
            util.cloudwatch_log(
                info.context,
                f'Security: Attempted to update evidence in event {event_id}')

        return UpdateEventEvidence(success=success)


class DownloadEventFile(Mutation):
    """ Generate url for the requested evidence file """
    class Arguments():
        event_id = String(required=True)
        file_name = String(required=True)
    success = Boolean()
    url = String()

    @staticmethod
    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_event_access
    def mutate(_, info, event_id, file_name):
        success = False
        signed_url = event_domain.get_evidence_link(event_id, file_name)

        if signed_url:
            util.cloudwatch_log(
                info.context,
                f'Security: Downloaded file in event {event_id} succesfully')
            success = True
        else:
            util.cloudwatch_log(
                info.context,
                f'Security: Attempted to download file in event {event_id}')

        return DownloadEventFile(success=success, url=signed_url)


class RemoveEventEvidence(Mutation):
    """ Remove evidence files """

    class Arguments():
        event_id = String(required=True)
        evidence_type = Argument(EventEvidenceType, required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['analyst', 'admin'])
    @require_event_access
    def mutate(_, info, event_id, evidence_type):
        success = event_domain.remove_evidence(evidence_type, event_id)
        if success:
            util.cloudwatch_log(
                info.context,
                f'Security: Removed evidence in event {event_id}')
            util.invalidate_cache(event_id)

        return RemoveEventEvidence(success=success)
