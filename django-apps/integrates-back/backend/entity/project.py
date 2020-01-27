""" GraphQL Entity for Formstack Projects """
# pylint: disable=super-init-not-called
# pylint: disable=no-self-use
from datetime import datetime
import time

import rollbar
import simplejson as json
from graphene import (
    Argument, Boolean, Enum, Field, Float, Int, JSONString, List, Mutation,
    ObjectType, String
)
from graphene.types.generic import GenericScalar

from backend.decorators import (
    get_entity_cache, require_login, require_project_access, require_role
)
from backend.domain import (
    finding as finding_domain, project as project_domain,
    vulnerability as vuln_domain
)
from backend.entity.comment import Comment
from backend.entity.event import Event
from backend.entity.finding import Finding
from backend.services import get_user_role
from backend.entity.user import User

from backend import util
from backend.dal import integrates_dal, project as redshift_dal


class Project(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """Formstack Project Class."""

    name = String()
    findings = List(Finding)
    open_vulnerabilities = Int()
    closed_vulnerabilities = Int()
    current_month_authors = Int()
    current_month_commits = Int()
    subscription = String()
    comments = List(Comment)
    tags = List(String)
    deletion_date = String()
    pending_closing_check = Int()
    last_closing_vuln = Int()
    max_severity = Float()
    max_open_severity = Float()
    mean_remediate = Int()
    total_findings = Int()
    users = List(User)
    total_treatment = GenericScalar()
    drafts = List(Finding)
    description = String()
    remediated_over_time = String()
    events = List(Event)

    def __init__(self, project_name, description=''):
        """Class constructor."""
        self.name = project_name
        self.subscription = ''
        self.comments = []
        self.tags = []
        self.deletion_date = ''
        self.open_vulnerabilities = 0
        self.closed_vulnerabilities = 0
        self.current_month_authors = 0
        self.current_month_commits = 0
        self.pending_closing_check = 0
        self.last_closing_vuln = 0
        self.max_severity = 0.0
        self.max_open_severity = 0.0
        self.mean_remediate = 0
        self.total_findings = 0
        self.total_treatment = {}
        self.description = description
        self.remediated_over_time = []

    def __str__(self):
        """String representation of entity."""
        return self.name

    def resolve_name(self, info):
        """Resolve name attribute."""
        del info
        return self.name

    @get_entity_cache
    def resolve_remediated_over_time(self, info):
        "Resolve remediated over time"
        del info
        remediated_over_time = integrates_dal.get_project_attributes_dynamo(
            self.name, ['remediated_over_time'])
        remediate_over_time_decimal = remediated_over_time.get('remediated_over_time', {})
        remediated_twelve_weeks = [lst_rem[-12:] for lst_rem in remediate_over_time_decimal]
        self.remediated_over_time = json.dumps(
            remediated_twelve_weeks, use_decimal=True)
        return self.remediated_over_time

    @get_entity_cache
    def resolve_findings(self, info):
        """Resolve findings attribute."""
        util.cloudwatch_log(info.context, 'Security: Access to {project} '
                            'findings'.format(project=self.name))
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_findings(self.name))
        findings_loader = info.context.loaders['finding']
        self.findings = findings_loader.load_many(finding_ids).then(
            lambda findings: [finding for finding in findings
                              if finding.current_state != 'DELETED'])

        return self.findings

    @get_entity_cache
    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_findings(self.name))
        vulns_loader = info.context.loaders['vulnerability']

        self.open_vulnerabilities = vulns_loader.load_many(finding_ids).then(
            lambda findings: sum([
                len([vuln for vuln in vulns
                     if vuln_domain.get_current_state(vuln) == 'open' and
                     (vuln.current_approval_status != 'PENDING' or
                      vuln.last_approved_status)])
                for vulns in findings
            ]))

        return self.open_vulnerabilities

    @get_entity_cache
    def resolve_closed_vulnerabilities(self, info):
        """Resolve closed vulnerabilities attribute."""
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_findings(self.name))
        vulns_loader = info.context.loaders['vulnerability']

        self.closed_vulnerabilities = vulns_loader.load_many(finding_ids).then(
            lambda findings: sum([
                len([vuln for vuln in vulns
                     if vuln_domain.get_current_state(vuln) == 'closed' and
                     (vuln.current_approval_status != 'PENDING' or
                      vuln.last_approved_status)])
                for vulns in findings
            ]))

        return self.closed_vulnerabilities

    @get_entity_cache
    def resolve_pending_closing_check(self, info):
        """Resolve pending closing check attribute."""
        del info
        self.pending_closing_check = project_domain.get_pending_closing_check(
            self.name)
        return self.pending_closing_check

    @get_entity_cache
    def resolve_last_closing_vuln(self, info):
        """Resolve days since last closing vuln attribute."""
        del info
        last_closing_vuln = integrates_dal.get_project_attributes_dynamo(
            self.name, ['last_closing_date'])
        self.last_closing_vuln = last_closing_vuln.get('last_closing_date', 0)
        return self.last_closing_vuln

    @get_entity_cache
    def resolve_max_severity(self, info):
        """Resolve maximum severity attribute."""
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_findings(self.name))
        findings_loader = info.context.loaders['finding']

        self.max_severity = findings_loader.load_many(finding_ids).then(
            lambda findings: max([
                finding.severity_score for finding in findings
                if finding.current_state != 'DELETED'])
            if findings else 0)

        return self.max_severity

    @get_entity_cache
    def resolve_max_open_severity(self, info):
        """Resolve maximum severity in open vulnerability attribute."""
        del info
        max_open_severity = integrates_dal.get_project_attributes_dynamo(
            self.name, ['max_open_severity'])
        self.max_open_severity = max_open_severity.get('max_open_severity', 0)
        return self.max_open_severity

    @get_entity_cache
    def resolve_mean_remediate(self, info):
        """Resolve mean to remediate a vulnerability attribute."""
        del info
        mean_remediate = integrates_dal.get_project_attributes_dynamo(
            self.name, ['mean_remediate'])
        self.mean_remediate = mean_remediate.get('mean_remediate', 0)
        return self.mean_remediate

    @get_entity_cache
    def resolve_total_findings(self, info):
        """Resolve total findings attribute."""
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_findings(self.name))
        findings_loader = info.context.loaders['finding']
        findings = findings_loader.load_many(finding_ids).then(
            lambda findings: [finding for finding in findings
                              if finding.current_state != 'DELETED'])
        self.total_findings = findings.then(len)

        return self.total_findings

    @get_entity_cache
    def resolve_total_treatment(self, info):
        """Resolve total treatment attribute."""
        del info
        total_treatment = integrates_dal.get_project_attributes_dynamo(
            self.name, ['total_treatment'])
        total_treatment_decimal = total_treatment.get('total_treatment', {})
        self.total_treatment = json.dumps(
            total_treatment_decimal, use_decimal=True)
        return self.total_treatment

    @get_entity_cache
    def resolve_current_month_authors(self, info):
        """Resolve current month authors attribute."""
        del info
        self.current_month_authors = \
            redshift_dal.get_current_month_authors(self.name)
        return self.current_month_authors

    @get_entity_cache
    def resolve_current_month_commits(self, info):
        """Resolve current month commits attribute."""
        del info
        self.current_month_commits = \
            redshift_dal.get_current_month_commits(self.name)
        return self.current_month_commits

    @get_entity_cache
    def resolve_subscription(self, info):
        """Resolve subscription attribute."""
        del info
        project_info = integrates_dal.get_project_attributes_dynamo(
            self.name, ['type'])
        if project_info:
            self.subscription = project_info.get('type', '')
        else:
            self.subscription = ''
        return self.subscription

    @get_entity_cache
    def resolve_deletion_date(self, info):
        """Resolve deletion date attribute."""
        del info
        project_info = integrates_dal.get_project_attributes_dynamo(
            self.name, ['deletion_date'])
        if project_info:
            self.deletion_date = project_info.get('deletion_date')
        else:
            self.deletion_date = ''
        return self.deletion_date

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_comments(self, info):
        user_data = util.get_jwt_content(info.context)
        curr_user_role = get_user_role(user_data)
        self.comments = [
            Comment(**comment) for comment in project_domain.list_comments(
                self.name, curr_user_role)]

        return self.comments

    @get_entity_cache
    def resolve_tags(self, info):
        """ Resolve project tags """
        del info

        project_data = \
            integrates_dal.get_project_attributes_dynamo(project_name=self.name,
                                                         data_attributes=['tag'])
        self.tags = project_data['tag'] if project_data and 'tag' in project_data else []

        return self.tags

    @require_role(['admin', 'customeradmin'])
    @get_entity_cache
    def resolve_users(self, info):
        """ Resolve project users """
        init_email_list = project_domain.get_users(self.name)
        user_email_list = util.user_email_filter(
            init_email_list, util.get_jwt_content(info.context)['user_email'])
        self.users = [User(self.name, user_email)
                      for user_email in user_email_list]
        return self.users

    @require_role(['admin', 'analyst'])
    def resolve_drafts(self, info):
        """ Resolve drafts attribute """
        util.cloudwatch_log(info.context, 'Security: Access to {project} '
                            'drafts'.format(project=self.name))
        finding_ids = finding_domain.filter_deleted_findings(
            project_domain.list_drafts(self.name))
        findings_loader = info.context.loaders['finding']
        self.drafts = findings_loader.load_many(finding_ids).then(
            lambda drafts: [draft for draft in drafts
                            if draft.current_state != 'DELETED'])

        return self.drafts

    @require_role(['admin', 'analyst', 'customer'])
    def resolve_events(self, info):
        """ Resolve project events """
        util.cloudwatch_log(
            info.context, f'Security: Access to {self.name} events')
        event_ids = project_domain.list_events(self.name)
        events_loader = info.context.loaders['event']
        self.events = events_loader.load_many(event_ids)

        return self.events

    def resolve_description(self, info):
        """ Resolve project description """
        del info

        return self.description


class CreateProject(Mutation):
    """ Create project """

    class Arguments():
        companies = List(String, required=True)
        description = String(required=True)
        project_name = String(required=True)
        subscription = Argument(Enum('Subscription', [
            ('Continuous', 'continuous'), ('Oneshot', 'oneshot')]),
            required=False)
    success = Boolean()

    @require_login
    @require_role(['admin', 'customeradminfluid'])
    def mutate(self, info, **kwargs):
        user_data = util.get_jwt_content(info.context)
        user_role = get_user_role(user_data)
        success = project_domain.create_project(
            user_data['user_email'], user_role, **kwargs)
        if success:
            project = kwargs.get('project_name').lower()
            util.invalidate_cache(user_data['user_email'])
            util.cloudwatch_log(
                info.context,
                f'Security: Created project {project} succesfully')
        return CreateProject(success=success)


class RemoveProject(Mutation):
    """ Remove project """

    class Arguments():
        project_name = String(required=True)
    success = Boolean()
    findings_masked = Boolean()
    users_removed = Boolean()
    project_finished = Boolean()

    @require_login
    @require_role(['admin', 'customeradminfluid'])
    @require_project_access
    def mutate(self, info, project_name):
        user_info = util.get_jwt_content(info.context)
        result = project_domain.remove_project(project_name, user_info['user_email'])
        success = all(list(result))
        if success:
            project = project_name.lower()
            util.cloudwatch_log(
                info.context,
                f'Security: Removed project {project} succesfully')
        return RemoveProject(success=success,
                             findings_masked=result.are_findings_masked,
                             users_removed=result.are_users_removed,
                             project_finished=result.is_project_finished)


class AddProjectComment(Mutation):
    """ Add comment to project """

    class Arguments():
        content = String(required=True)
        parent = String(required=True)
        project_name = String(required=True)
    success = Boolean()
    comment_id = String()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, **parameters):
        project_name = parameters.get('project_name').lower()
        user_info = util.get_jwt_content(info.context)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'user_id': comment_id,
            'content': parameters.get('content'),
            'created': current_time,
            'fullname':
                str.join(' ', [user_info['first_name'],
                               user_info['last_name']]),
            'modified': current_time,
            'parent': int(parameters.get('parent'))
        }
        success = project_domain.add_comment(
            project_name, user_info['user_email'], comment_data)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Added comment to \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to add \
                comment in {project} project'.format(project=project_name))
        ret = AddProjectComment(success=success, comment_id=comment_id)
        return ret


class RemoveTag(Mutation):
    """Remove a tag of a given project."""

    class Arguments():
        project_name = String(required=True)
        tag = String(required=True)
    project = Field(Project)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, project_name, tag):
        success = False
        project_name = project_name.lower()
        if project_domain.validate_project(project_name):
            primary_keys = ['project_name', project_name.lower()]
            table_name = 'FI_projects'
            tag_deleted = integrates_dal.remove_set_element_dynamo(
                table_name, primary_keys, 'tag', tag)
            if tag_deleted:
                success = True
            else:
                rollbar.report_message('Error: \
An error occurred removing a tag', 'error', info.context)
        if success:
            util.invalidate_cache(project_name)
            util.cloudwatch_log(info.context, 'Security: Removed tag from \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove \
                tag in {project} project'.format(project=project_name))
        ret = RemoveTag(success=success, project=Project(project_name))
        return ret


class AddTags(Mutation):
    """Add a tags to a project."""

    class Arguments():
        project_name = String(required=True)
        tags = JSONString()
    project = Field(Project)
    success = Boolean()

    @require_login
    @require_role(['customer'])
    @require_project_access
    def mutate(self, info, project_name, tags):
        success = False
        project_name = project_name.lower()
        if project_domain.validate_project(project_name):
            primary_keys = ['project_name', project_name]
            table_name = 'FI_projects'
            if project_domain.validate_tags(tags):
                tags_added = integrates_dal.add_set_element_dynamo(
                    table_name, primary_keys, 'tag', tags)
                if tags_added:
                    success = True
                else:
                    rollbar.report_message('Error: \
An error occurred adding tags', 'error', info.context)
            else:
                util.cloudwatch_log(info.context,
                                    'Security: \
Attempted to upload tags without the allowed structure')
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to upload tags without the allowed validations')
        if success:
            util.invalidate_cache(project_name)
        ret = AddTags(success=success, project=Project(project_name))
        return ret


class AddAllProjectAccess(Mutation):

    class Arguments():
        project_name = String(required=True)
    success = Boolean()

    @require_login
    @require_role(['admin'])
    def mutate(self, info, project_name):
        success = project_domain.add_all_access_to_project(project_name)
        if success:
            util.cloudwatch_log(
                info.context,
                f'Security: Add all project access of {project_name}')
            util.invalidate_cache(project_name)
        return AddAllProjectAccess(success=success)


class RemoveAllProjectAccess(Mutation):

    class Arguments():
        project_name = String(required=True)
    success = Boolean()

    @require_login
    @require_role(['admin'])
    def mutate(self, info, project_name):
        success = project_domain.remove_all_project_access(project_name)
        if success:
            util.cloudwatch_log(
                info.context,
                f'Security: Remove all project access of {project_name}')
            util.invalidate_cache(project_name)
        return RemoveAllProjectAccess(success=success)
