""" GraphQL Entity for Formstack Projects """
# pylint: disable=super-init-not-called
# pylint: disable=no-self-use
from __future__ import absolute_import
from datetime import datetime
import time
import pytz
import rollbar

import simplejson as json
from graphene import String, ObjectType, List, Int, Float, Boolean, Mutation, Field, JSONString
from graphene.types.generic import GenericScalar
from django.conf import settings

from app import util
from app.decorators import require_role, require_login, require_project_access
from app.domain.project import (
    add_comment, validate_tags, validate_project, get_vulnerabilities,
    get_pending_closing_check, get_max_severity, get_drafts, list_comments
)
from app.dal import integrates_dal, project as redshift_dal
from app.decorators import get_entity_cache
from app.domain import project
from app.entity.finding import Finding
from app.entity.user import User
from app.exceptions import InvalidProject


class Project(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """Formstack Project Class."""

    name = String()
    findings = List(Finding)
    findings_aux = []
    open_vulnerabilities = Int()
    closed_vulnerabilities = Int()
    current_month_authors = Int()
    current_month_commits = Int()
    subscription = String()
    comments = List(GenericScalar)
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

    def __init__(self, project_name, description=''):
        """Class constructor."""
        self.name = project_name.lower()
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

        if validate_project(self.name):
            findings = integrates_dal.get_findings_released_dynamo(
                self.name, 'finding_id, treatment, cvss_temporal')
            self.findings_aux = findings
        else:
            raise InvalidProject

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
        self.findings = [Finding(i['finding_id'], info.context)
                         for i in self.findings_aux]
        return self.findings

    @get_entity_cache
    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        del info
        self.open_vulnerabilities = get_vulnerabilities(
            self.findings_aux, 'openVulnerabilities')
        return self.open_vulnerabilities

    @get_entity_cache
    def resolve_closed_vulnerabilities(self, info):
        """Resolve closed vulnerabilities attribute."""
        del info
        self.closed_vulnerabilities = get_vulnerabilities(
            self.findings_aux, 'closedVulnerabilities')
        return self.closed_vulnerabilities

    @get_entity_cache
    def resolve_pending_closing_check(self, info):
        """Resolve pending closing check attribute."""
        del info
        self.pending_closing_check = get_pending_closing_check(self.name)
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
        del info
        self.max_severity = get_max_severity(self.findings_aux)
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
        del info
        self.total_findings = len(self.findings_aux)
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
        self.comments = list_comments(
            user_email=util.get_jwt_content(info.context)['user_email'],
            project_name=self.name)

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
    def resolve_users(self, info):
        """ Resolve project users """
        init_email_list = project.get_users_from_db(self.name)
        user_email_list = util.user_email_filter(init_email_list,
                                                 util.get_jwt_content(info.context)['user_email'])
        self.users = [User(self.name, user_email) for user_email in user_email_list]
        return self.users

    @get_entity_cache
    def resolve_users_db(self):
        """resolve a full list of users from database"""
        init_emails = integrates_dal.get_project_users(self.name)
        users_list = [user[0] for user in init_emails if user[1] == 1]
        return users_list

    @require_role(['admin', 'analyst'])
    def resolve_drafts(self, info):
        """ Resolve drafts attribute """
        self.drafts = [Finding(draft_id, info.context)
                       for draft_id in get_drafts(self.name)]
        return self.drafts

    def resolve_description(self, info):
        """ Resolve project description """
        del info

        return self.description


def validate_release_date(release_date=''):
    """Validate if a finding has a valid relese date."""
    if release_date:
        tzn = pytz.timezone(settings.TIME_ZONE)
        finding_last_vuln = datetime.strptime(
            release_date.split(' ')[0],
            '%Y-%m-%d'
        )
        last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
        today_day = datetime.now(tz=tzn).date()
        result = last_vuln <= today_day
    else:
        result = False
    return result


class AddProjectComment(Mutation):
    """ Add comment to project """

    class Arguments(object):
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
        success = add_comment(project_name, user_info['user_email'],
                              comment_data)
        if success:
            util.cloudwatch_log(info.context, 'Security: Added comment to \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to add \
                comment in {project} project'.format(project=project_name))
        ret = AddProjectComment(success=success, comment_id=comment_id)
        util.invalidate_cache(project_name)
        return ret


class RemoveTag(Mutation):
    """Remove a tag of a given project."""

    class Arguments(object):
        project_name = String(required=True)
        tag = String(required=True)
    project = Field(Project)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, project_name, tag):
        success = False
        project_name = project_name.lower()
        if validate_project(project_name):
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
            util.cloudwatch_log(info.context, 'Security: Removed tag from \
                {project} project succesfully'.format(project=project_name))
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to remove \
                tag in {project} project'.format(project=project_name))
        ret = RemoveTag(success=success, project=Project(project_name))
        util.invalidate_cache(project_name)
        return ret


class AddTags(Mutation):
    """Add a tags to a project."""

    class Arguments(object):
        project_name = String(required=True)
        tags = JSONString()
    project = Field(Project)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_project_access
    def mutate(self, info, project_name, tags):
        success = False
        project_name = project_name.lower()
        if validate_project(project_name):
            primary_keys = ['project_name', project_name]
            table_name = 'FI_projects'
            if validate_tags(tags):
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

        ret = AddTags(success=success, project=Project(project_name))
        util.invalidate_cache(project_name)
        return ret
