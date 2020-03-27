""" GraphQL Entity for Findings """
# pylint: disable=no-self-use
from collections import namedtuple
from time import time

import rollbar
from graphql import GraphQLError
from graphene import (
    Argument, Boolean, Enum, Field, Float, Int, JSONString, List, Mutation,
    ObjectType, String
)
from graphene.types.generic import GenericScalar
from graphene_file_upload.scalars import Upload
from backend import util
from backend.decorators import (
    get_entity_cache, require_finding_access, require_login,
    require_project_access, enforce_authz
)
from backend.domain import (
    user as user_domain,
    comment as comment_domain, finding as finding_domain,
    project as project_domain, vulnerability as vuln_domain
)
from backend.entity.comment import Comment
from backend.entity.vulnerability import Vulnerability
from backend.utils import findings as finding_utils


class Finding(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """Finding Class."""

    actor = String()
    affected_systems = String()
    age = Int()
    analyst = String()
    attack_vector_desc = String()
    bts_url = String()
    closed_vulnerabilities = Int()
    comments = List(Comment)
    compromised_attributes = String()
    compromised_records = Int()
    current_state = String()
    cvss_version = String()
    cwe_url = String()
    description = String()
    evidence = GenericScalar()
    exploit = String()
    id = String()  # noqa pylint: disable=invalid-name
    is_exploitable = Boolean()
    last_vulnerability = Int()
    observations = List(Comment)
    open_vulnerabilities = Int()
    project_name = String()
    recommendation = String()
    records = JSONString()
    release_date = String()
    new_remediated = Boolean()
    remediated = Boolean()
    verified = Boolean()
    report_date = String()
    requirements = String()
    risk = String()
    scenario = String()
    severity = GenericScalar()
    severity_score = Float()
    state = String()
    historic_state = List(GenericScalar)
    historic_treatment = List(GenericScalar)
    threat = String()
    title = String()
    tracking = List(GenericScalar)
    type = String()
    vulnerabilities = List(Vulnerability, vuln_type=String(), state=String(),
                           approval_status=String())

    def __str__(self):
        return self.id + '_finding'

    def resolve_id(self, info):
        """Resolve id attribute."""
        del info
        return self.id

    def resolve_project_name(self, info):
        """Resolve project_name attribute."""
        del info
        return self.project_name

    @get_entity_cache
    def resolve_vulnerabilities(self, info,
                                vuln_type='', state='', approval_status=''):
        """Resolve vulnerabilities attribute."""
        vulns_loader = info.context.loaders['vulnerability']
        vuln_filtered = vulns_loader.load(self.id)

        if vuln_type:
            vuln_filtered = vuln_filtered.then(lambda vulns: [
                vuln for vuln in vulns if vuln.vuln_type == vuln_type and
                (vuln.current_approval_status != 'PENDING' or
                 vuln.last_approved_status)])
        if state:
            vuln_filtered = vuln_filtered.then(lambda vulns: [
                vuln for vuln in vulns
                if vuln_domain.get_current_state(vuln) == state and
                (vuln.current_approval_status != 'PENDING' or
                 vuln.last_approved_status)])
        if approval_status:
            vuln_filtered = vuln_filtered.then(lambda vulns: [
                vuln for vuln in vulns
                if vuln.current_approval_status == approval_status])

        return vuln_filtered

    @get_entity_cache
    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        vulns_loader = info.context.loaders['vulnerability']
        vulns = vulns_loader.load(self.id)

        self.open_vulnerabilities = vulns.then(lambda vulns: len([
            vuln for vuln in vulns
            if vuln_domain.get_current_state(vuln) == 'open' and
            (vuln.current_approval_status != 'PENDING' or
             vuln.last_approved_status)]))

        return self.open_vulnerabilities

    def resolve_release_date(self, info):
        """Resolve release date attribute."""
        draft_allowed_roles = ['admin', 'analyst']

        if not self.release_date:
            data = util.get_jwt_content(info.context)
            email = data['user_email']
            role = user_domain.get_group_level_role(email, self.project_name)

            if role not in draft_allowed_roles:
                raise GraphQLError('Access denied')
        return self.release_date

    @get_entity_cache
    def resolve_closed_vulnerabilities(self, info):
        """Resolve closed vulnerabilities attribute."""
        vulns_loader = info.context.loaders['vulnerability']
        vulns = vulns_loader.load(self.id)

        self.closed_vulnerabilities = vulns.then(lambda vulns: len([
            vuln for vuln in vulns
            if vuln_domain.get_current_state(vuln) == 'closed' and
            (vuln.current_approval_status != 'PENDING' or
             vuln.last_approved_status)]))

        return self.closed_vulnerabilities

    @get_entity_cache
    def resolve_tracking(self, info):
        """Resolve tracking attribute."""
        if self.release_date:
            vulns_loader = info.context.loaders['vulnerability']
            vulns = vulns_loader.load(self.id).then(lambda vulns: vulns).get()
            self.tracking = finding_domain.get_tracking_vulnerabilities(vulns)
        else:
            self.tracking = []
        return self.tracking

    @get_entity_cache
    def resolve_records(self, info):
        """ Resolve compromised records attribute """
        del info
        if self.records['url']:
            self.records = finding_utils.get_records_from_file(
                self.project_name, self.id, self.records['url'])
        else:
            self.records = []
        return self.records

    def resolve_severity(self, info):
        """ Resolve severity values from Formstack """
        del info

        return self.severity

    def resolve_cvss_version(self, info):
        """ Resolve cvss version value from Formstack """
        del info

        return self.cvss_version

    @get_entity_cache
    def resolve_exploit(self, info):
        """ Resolve exploit attribute """
        del info
        if self.exploit['url']:
            self.exploit = finding_utils.get_exploit_from_file(
                self.project_name, self.id, self.exploit['url'])
        else:
            self.exploit = ''
        return self.exploit

    @get_entity_cache
    def resolve_evidence(self, info):
        """ Resolve evidence attribute """
        del info
        return self.evidence

    def resolve_comments(self, info):
        """ Resolve comments attribute """
        user_data = util.get_jwt_content(info.context)
        user_email = user_data['user_email']
        curr_user_role = \
            user_domain.get_group_level_role(user_email, self.project_name)
        self.comments = [Comment(**comment)
                         for comment in comment_domain.get_comments(
                             self.id, curr_user_role)]
        return self.comments

    @enforce_authz
    @get_entity_cache
    def resolve_historic_state(self, info):
        """ Resolve submission history of a draft """
        del info
        return self.historic_state

    @enforce_authz
    def resolve_observations(self, info):
        """ Resolve observations attribute """
        user_data = util.get_jwt_content(info.context)
        user_email = user_data['user_email']
        curr_user_role = \
            user_domain.get_group_level_role(user_email, self.project_name)
        self.observations = [Comment(**obs)
                             for obs in comment_domain.get_observations(
                                 self.id, curr_user_role)]
        return self.observations

    def resolve_title(self, info):
        """ Resolve title attribute """
        del info
        return self.title

    def resolve_scenario(self, info):
        """ Resolve scenario attribute """
        del info
        return self.scenario

    def resolve_actor(self, info):
        """ Resolve actor attribute """
        del info
        return self.actor

    def resolve_description(self, info):
        """ Resolve description attribute """
        del info
        return self.description

    def resolve_requirements(self, info):
        """ Resolve requirements attribute """
        del info
        return self.requirements

    def resolve_attack_vector_desc(self, info):
        """ Resolve attack vector description attribute """
        del info
        return self.attack_vector_desc

    def resolve_threat(self, info):
        """ Resolve threat attribute """
        del info
        return self.threat

    def resolve_recommendation(self, info):
        """ Resolve recommendation attribute """
        del info
        return self.recommendation

    def resolve_affected_systems(self, info):
        """ Resolve affected_systems attribute """
        del info
        return self.affected_systems

    def resolve_compromised_attributes(self, info):
        """ Resolve compromised_attributes attribute """
        del info
        return self.compromised_attributes

    def resolve_compromised_records(self, info):
        """ Resolve compromised_records attribute """
        del info
        return self.compromised_records

    def resolve_cwe_url(self, info):
        """ Resolve cwe_url attribute """
        del info

        return self.cwe_url

    def resolve_bts_url(self, info):
        """ Resolve bts_url attribute """
        del info
        return self.bts_url

    def resolve_risk(self, info):
        """ Resolve risk attribute """
        del info
        return self.risk

    @get_entity_cache
    def resolve_state(self, info):
        """ Resolve state attribute """
        vulns_loader = info.context.loaders['vulnerability']
        vulns = vulns_loader.load(self.id)

        self.state = vulns.then(lambda vulns: 'open' if [
            vuln for vuln in vulns
            if vuln_domain.get_last_approved_status(vuln) == 'open']
            else 'closed')

        return self.state

    def resolve_remediated(self, info):
        """ Resolve remediated attribute """
        del info
        return self.remediated

    def resolve_type(self, info):
        """ Resolve type attribute """
        del info
        return self.type

    def resolve_age(self, info):
        """ Resolve age attribute """
        del info
        return self.age

    def resolve_last_vulnerability(self, info):
        """ Resolve days since last report """
        del info
        last_vuln_date = util.calculate_datediff_since(self.last_vulnerability)
        self.last_vulnerability = last_vuln_date.days
        return self.last_vulnerability

    def resolve_is_exploitable(self, info):
        """ Resolve is_exploitable attribute """
        del info
        return self.is_exploitable

    def resolve_severity_score(self, info):
        """ Resolve precalculated severity score """
        del info
        return self.severity_score

    def resolve_report_date(self, info):
        """ Resolve report date """
        del info
        return self.report_date

    @enforce_authz
    def resolve_analyst(self, info):
        """ Resolve analyst attribute """
        del info
        return self.analyst

    def resolve_historic_treatment(self, info):
        del info
        return self.historic_treatment

    def resolve_current_state(self, info):
        """Resolve vulnerabilities attribute."""
        del info
        return self.current_state

    def resolve_new_remediated(self, info):
        """ Resolve new_remediated attribute """
        del info
        return self.new_remediated

    def resolve_verified(self, info):
        """ Resolve verified attribute """
        del info
        return self.verified


EVIDENCE_TYPE = Enum('EvidenceType', [
    ('ANIMATION', 'animation'),
    ('EVIDENCE1', 'evidence_route_1'),
    ('EVIDENCE2', 'evidence_route_2'),
    ('EVIDENCE3', 'evidence_route_3'),
    ('EVIDENCE4', 'evidence_route_4'),
    ('EVIDENCE5', 'evidence_route_5'),
    ('EXPLOIT', 'exploit'),
    ('EXPLOITATION', 'exploitation'),
    ('RECORDS', 'fileRecords')
])


class RemoveEvidence(Mutation):
    """ Remove evidence files """

    class Arguments():
        finding_id = String(required=True)
        evidence_id = Argument(EVIDENCE_TYPE, required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, evidence_id, finding_id):
        success = finding_domain.remove_evidence(evidence_id, finding_id)

        if success:
            util.cloudwatch_log(
                info.context,
                f'Security: Removed evidence in finding {finding_id}')
            util.invalidate_cache(finding_id)
        findings_loader = info.context.loaders['finding']
        ret = RemoveEvidence(
            finding=findings_loader.load(finding_id), success=success)
        return ret


class UpdateEvidence(Mutation):
    """ Update evidence files """

    class Arguments():
        file = Upload(required=True)
        finding_id = String(required=True)
        evidence_id = Argument(EVIDENCE_TYPE, required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, evidence_id, finding_id, file):
        success = False

        if finding_domain.validate_evidence(evidence_id, file):
            success = finding_domain.update_evidence(
                finding_id, evidence_id, file)
        if success:
            util.invalidate_cache(finding_id)
            util.cloudwatch_log(info.context,
                                'Security: Updated evidence in finding '
                                f'{finding_id} succesfully')
        else:
            util.cloudwatch_log(info.context,
                                'Security: Attempted to update evidence in '
                                f'finding {finding_id}')

        return UpdateEvidence(success=success)


class UpdateEvidenceDescription(Mutation):
    """ Update evidence description """

    class Arguments():
        description = String(required=True)
        evidence_id = Argument(
            Enum('EvidenceDescriptionType', [
                ('EVIDENCE1', 'evidence_route_1'),
                ('EVIDENCE2', 'evidence_route_2'),
                ('EVIDENCE3', 'evidence_route_3'),
                ('EVIDENCE4', 'evidence_route_4'),
                ('EVIDENCE5', 'evidence_route_5')
            ]), required=True)
        finding_id = String(required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id, evidence_id, description):
        success = False
        try:
            success = finding_domain.update_evidence_description(
                finding_id, evidence_id, description)
            if success:
                util.invalidate_cache(finding_id)
                util.cloudwatch_log(info.context, 'Security: Evidence description \
                    succesfully updated in finding ' + finding_id)
            else:
                util.cloudwatch_log(info.context, 'Security: Attempted to update \
                    evidence description in ' + finding_id)
        except KeyError:
            rollbar.report_message('Error: \
An error occurred updating evidence description', 'error', info.context)

        return UpdateEvidenceDescription(success=success)


class UpdateSeverity(Mutation):
    class Arguments():
        finding_id = String(required=True)
        data = GenericScalar(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, **parameters):
        finding_id = parameters.get('finding_id')
        project = finding_domain.get_project(finding_id)
        success = False
        success = finding_domain.save_severity(parameters.get('data'))
        findings_loader = info.context.loaders['finding']
        ret = UpdateSeverity(
            finding=findings_loader.load(finding_id), success=success)
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project)
            util.cloudwatch_log(info.context, 'Security: Updated severity in\
                finding {id} succesfully'.format(id=parameters.get('finding_id')))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to update \
                severity in finding {id}'.format(id=parameters.get('finding_id')))
        return ret


class AddFindingComment(Mutation):
    """ Add comment to finding """
    class Arguments():
        content = String(required=True)
        finding_id = String(required=True)
        parent = String(required=True)
        type = Argument(
            Enum('FindingCommentType', [
                ('COMMENT', 'comment'),
                ('OBSERVATION', 'observation')
            ]), required=True)
    success = Boolean()
    comment_id = String()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, **parameters):
        if parameters.get('type') in ['comment', 'observation']:
            user_data = util.get_jwt_content(info.context)
            user_email = user_data['user_email']
            finding_id = parameters.get('finding_id')
            group = finding_domain.get_finding(finding_id).get('projectName')
            role = \
                user_domain.get_group_level_role(user_email, group)
            if parameters.get('type') == 'observation' and \
               role not in ['analyst', 'admin']:
                util.cloudwatch_log(info.context, 'Security: \
                    Unauthorized role attempted to add observation')
                raise GraphQLError('Access denied')

            user_email = user_data['user_email']
            comment_id = int(round(time() * 1000))
            comment_data = {
                'user_id': comment_id,
                'comment_type': parameters.get('type'),
                'content': parameters.get('content'),
                'fullname': str.join(' ', [user_data['first_name'],
                                     user_data['last_name']]),
                'parent': parameters.get('parent'),
            }
            success = finding_domain.add_comment(
                user_email=user_email,
                comment_data=comment_data,
                finding_id=finding_id,
                is_remediation_comment=False
            )
        else:
            raise GraphQLError('Invalid comment type')
        if success:
            util.invalidate_cache(parameters.get('finding_id'))
            util.cloudwatch_log(info.context, 'Security: Added comment in\
                finding {id} succesfully'.format(id=parameters.get('finding_id')))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to add \
                comment in finding {id}'.format(id=parameters.get('finding_id')))
        ret = AddFindingComment(success=success, comment_id=comment_id)
        return ret


class VerifyFinding(Mutation):
    """ Verify a finding """
    class Arguments():
        finding_id = String(required=True)
        justification = String(required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id, justification):
        project_name = project_domain.get_finding_project_name(finding_id)
        user_info = util.get_jwt_content(info.context)
        success = finding_domain.verify_finding(
            finding_id, user_info['user_email'],
            justification, str.join(' ', [user_info['first_name'], user_info['last_name']])
        )
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Verified the '
                                f'finding_id: {finding_id}')
        ret = VerifyFinding(success=success)
        return ret


class HandleAcceptation(Mutation):
    """ Approve or reject acceptation request """
    class Arguments():
        finding_id = String(required=True)
        observations = String(required=True)
        project_name = String(required=True)
        response = String(required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, **parameters):
        user_info = util.get_jwt_content(info.context)
        user_mail = user_info['user_email']
        finding_id = parameters.get('finding_id')
        historic_treatment = finding_domain.get_finding(finding_id).get('historicTreatment')
        if historic_treatment[-1]['acceptance_status'] != 'SUBMITTED':
            raise GraphQLError(
                'It cant be approved/rejected a finding' +
                'definite assumption without being requested')

        success = finding_domain.handle_acceptation(finding_id,
                                                    parameters.get('observations'),
                                                    user_mail,
                                                    parameters.get('response'))
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(parameters.get('project_name'))
            util.cloudwatch_log(info.context, 'Security: Verified a request '
                                f'in finding_id: {finding_id}')
        ret = HandleAcceptation(success=success)
        return ret


class UpdateDescription(Mutation):
    """ Update description of a finding """
    class Arguments():
        actor = String(required=True)
        affected_systems = String(required=True)
        attack_vector_desc = String(required=True)
        cwe = String(required=True)
        description = String(required=True)
        finding_id = String(required=True)
        recommendation = String(required=True)
        records = String()
        records_number = Int(required=True)
        requirements = String(required=True)
        risk = String()
        scenario = String(required=True)
        threat = String(required=True)
        title = String(required=True)
        finding_type = String()
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id, **parameters):
        success = finding_domain.update_description(finding_id, parameters)
        if success:
            project_name = finding_domain.get_finding(finding_id)['projectName']
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Updated description in\
                finding {id} succesfully'.format(id=finding_id))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to update \
                description in finding {id}'.format(id=finding_id))
        findings_loader = info.context.loaders['finding']
        ret = UpdateDescription(
            finding=findings_loader.load(finding_id), success=success)
        return ret


class UpdateClientDescription(Mutation):
    """ Update treatment of a finding """
    class Arguments():
        acceptance_date = String()
        bts_url = String()
        finding_id = String(required=True)
        treatment = String(
            Enum('UpdateClientDescriptionTreatment', [
                ('IN PROGRESS', 'IN PROGRESS'),
                ('ACCEPTED', 'ACCEPTED'),
                ('ACCEPTED_UNDEFINED', 'ACCEPTED_UNDEFINED')]), required=True)
        justification = String(required=True)
        acceptance_status = String()
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id, **parameters):
        project_name = finding_domain.get_finding(finding_id)['projectName']
        user_mail = util.get_jwt_content(info.context)['user_email']
        if parameters.get('acceptance_status') == '':
            del parameters['acceptance_status']
        historic_treatment = finding_domain.get_finding(finding_id)['historicTreatment']
        last_state = {
            key: value for key, value in historic_treatment[-1].items()
            if key not in ['date', 'user']}
        new_state = {
            key: value for key, value in parameters.items() if key != 'bts_url'}
        bts_changed, treatment_changed = True, True
        Status = namedtuple('Status', 'bts_changed treatment_changed')
        if not finding_domain.compare_historic_treatments(last_state, new_state):
            treatment_changed = False
        if ('externalBts' in finding_domain.get_finding(finding_id) and
           parameters.get('bts_url') == finding_domain.get_finding(finding_id)['externalBts']):
            bts_changed = False
        update = Status(bts_changed=bts_changed, treatment_changed=treatment_changed)
        if not any(list(update)):
            raise GraphQLError('It cant be updated a finding with same values it already has')
        success = finding_domain.update_client_description(
            finding_id, parameters, user_mail, update)
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Updated treatment in '
                                f'finding {finding_id} succesfully')
            util.forces_trigger_deployment(project_name)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to update '
                                f'treatment in finding {finding_id}')
        findings_loader = info.context.loaders['finding']
        return UpdateClientDescription(
            finding=findings_loader.load(finding_id), success=success)


class RejectDraft(Mutation):
    class Arguments():
        finding_id = String(required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id):
        reviewer_email = util.get_jwt_content(info.context)['user_email']
        project_name = finding_domain.get_finding(finding_id)['projectName']

        success = finding_domain.reject_draft(finding_id, reviewer_email)
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(
                info.context,
                'Security: Draft {} rejected succesfully'.format(finding_id))
        else:
            util.cloudwatch_log(
                info.context,
                'Security: Attempted to reject draft {}'.format(finding_id))
        return RejectDraft(success=success)


class DeleteFinding(Mutation):
    class Arguments():
        finding_id = String(required=True)
        justification = Argument(
            Enum('DeleteFindingJustification', [
                ('DUPLICATED', 'DUPLICATED'),
                ('FALSE_POSITIVE', 'FALSE_POSITIVE'),
                ('NOT_REQUIRED', 'NOT_REQUIRED')]), required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id, justification):
        project_name = finding_domain.get_finding(finding_id)['projectName']

        success = finding_domain.delete_finding(
            finding_id, project_name, justification, info.context)
        if success:
            util.invalidate_cache(finding_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(
                info.context,
                f'Security: Deleted finding: {finding_id} succesfully')
        else:
            util.cloudwatch_log(
                info.context,
                f'Security: Attempted to delete finding: {finding_id}')
        return DeleteFinding(success=success)


class ApproveDraft(Mutation):
    class Arguments():
        draft_id = String(required=True)
    release_date = String()
    success = Boolean()

    @require_login
    @enforce_authz
    def mutate(self, info, draft_id):
        reviewer_email = util.get_jwt_content(info.context)['user_email']
        project_name = finding_domain.get_finding(draft_id)['projectName']

        has_vulns = [vuln for vuln in vuln_domain.list_vulnerabilities([draft_id])
                     if vuln['historic_state'][-1].get('state') != 'DELETED']
        if not has_vulns:
            raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
        success, release_date = finding_domain.approve_draft(
            draft_id, reviewer_email)
        if success:
            util.invalidate_cache(draft_id)
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Approved draft in\
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to approve \
                draft in {project} project'.format(project=project_name))
        return ApproveDraft(release_date, success)


class CreateDraft(Mutation):
    """ Creates a new draft """
    class Arguments():
        cwe = String(required=False)
        description = String(required=False)
        origin = String(required=False)
        project_name = String(required=True)
        recommendation = String(required=False)
        requirements = String(required=False)
        risk = String(required=False)
        threat = String(required=False)
        title = String(required=True)
        type = Argument(Enum('FindingType', [
            ('SECURITY', 'SECURITY'), ('HYGIENE', 'HYGIENE')]), required=False)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_project_access
    def mutate(self, info, project_name, title, **kwargs):
        success = finding_domain.create_draft(
            info, project_name, title, **kwargs)

        if success:
            util.cloudwatch_log(info.context, 'Security: Created draft in '
                                '{} project succesfully'.format(project_name))
        return CreateDraft(success=success)


class SubmitDraft(Mutation):
    """ Submits a draft for review """
    class Arguments():
        finding_id = String(required=True)
    success = Boolean()

    @require_login
    @enforce_authz
    @require_finding_access
    def mutate(self, info, finding_id):
        analyst_email = util.get_jwt_content(info.context)['user_email']
        success = finding_domain.submit_draft(finding_id, analyst_email)

        if success:
            util.invalidate_cache(finding_id)
            util.cloudwatch_log(info.context, 'Security: Submitted draft '
                                '{} succesfully'.format(finding_id))
        return SubmitDraft(success=success)
