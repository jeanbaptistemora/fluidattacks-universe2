""" GraphQL Entity for Formstack Projects """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# pylint: disable=super-init-not-called
# pylint: disable=no-self-use
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from __future__ import absolute_import
from datetime import datetime
import time
import pytz
import rollbar
from app import util
from app.decorators import require_role, require_login, require_project_access_gql
from app.domain.project import (
    add_comment, validate_tags, validate_project, get_vulnerabilities,
    get_pending_closing_check, get_last_closing_vuln, get_total_treatment,
    get_max_severity, get_max_open_severity, get_mean_remediate,
    get_project_info
)
from graphene import String, ObjectType, List, Int, Float, Boolean, Mutation, Field, JSONString
from graphene.types.generic import GenericScalar

from ..dao import integrates_dao, project as redshift_dao
from .finding import Finding
from .user import User


class Project(ObjectType): # noqa pylint: disable=too-many-instance-attributes
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
    has_complete_docs = Boolean()

    def __init__(self, project_name):
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

        findings = integrates_dao.get_findings_released_dynamo(
            self.name, 'finding_id, treatment, cvss_temporal')
        self.findings_aux = findings

    def resolve_name(self, info):
        """Resolve name attribute."""
        del info
        return self.name

    def resolve_findings(self, info):
        """Resolve findings attribute."""
        self.findings = [Finding(info, i['finding_id']) for i in self.findings_aux]
        return self.findings

    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        del info
        self.open_vulnerabilities = get_vulnerabilities(
            self.findings_aux, 'openVulnerabilities')
        return self.open_vulnerabilities

    def resolve_closed_vulnerabilities(self, info):
        """Resolve closed vulnerabilities attribute."""
        del info
        self.closed_vulnerabilities = get_vulnerabilities(
            self.findings_aux, 'closedVulnerabilities')
        return self.closed_vulnerabilities

    def resolve_pending_closing_check(self, info):
        """Resolve pending closing check attribute."""
        del info
        self.pending_closing_check = get_pending_closing_check(self.name)
        return self.pending_closing_check

    def resolve_last_closing_vuln(self, info):
        """Resolve days since last closing vuln attribute."""
        del info
        self.last_closing_vuln = get_last_closing_vuln(self.findings_aux)
        return self.last_closing_vuln

    def resolve_max_severity(self, info):
        """Resolve maximum severity attribute."""
        del info
        self.max_severity = get_max_severity(self.findings_aux)
        return self.max_severity

    def resolve_max_open_severity(self, info):
        """Resolve maximum severity in open vulnerability attribute."""
        del info
        self.max_open_severity = get_max_open_severity(self.findings_aux)
        return self.max_open_severity

    def resolve_mean_remediate(self, info):
        """Resolve mean to remediate a vulnerability attribute."""
        del info
        self.mean_remediate = get_mean_remediate(self.findings_aux)
        return self.mean_remediate

    def resolve_total_findings(self, info):
        """Resolve total findings attribute."""
        del info
        self.total_findings = len(self.findings_aux)
        return self.total_findings

    def resolve_total_treatment(self, info):
        """Resolve total treatment attribute."""
        del info
        self.total_treatment = get_total_treatment(self.findings_aux)
        return self.total_treatment

    def resolve_current_month_authors(self, info):
        """Resolve current month authors attribute."""
        del info
        self.current_month_authors = \
            redshift_dao.get_current_month_authors(self.name)
        return self.current_month_authors

    def resolve_current_month_commits(self, info):
        """Resolve current month commits attribute."""
        del info
        self.current_month_commits = \
            redshift_dao.get_current_month_commits(self.name)
        return self.current_month_commits

    def resolve_subscription(self, info):
        """Resolve subscription attribute."""
        del info
        project_info = integrates_dao.get_project_dynamo(self.name)
        if project_info:
            self.subscription = project_info[0].get('type')
        else:
            self.subscription = ''
        return self.subscription

    def resolve_deletion_date(self, info):
        """Resolve deletion date attribute."""
        del info
        project_info = integrates_dao.get_project_attributes_dynamo(
            self.name, ['deletion_date'])
        if project_info:
            self.deletion_date = project_info.get('deletion_date')
        else:
            self.deletion_date = ''
        return self.deletion_date

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_comments(self, info):
        comments = integrates_dao.get_project_comments_dynamo(self.name)

        for comment in comments:
            comment_data = {
                'content': comment['content'],
                'created': comment['created'],
                'created_by_current_user':
                    comment['email'] == util.get_jwt_content(info.context)["user_email"],
                'email': comment['email'],
                'fullname': comment['fullname'],
                'id': int(comment['user_id']),
                'modified': comment['modified'],
                'parent': int(comment['parent'])
            }
            self.comments.append(comment_data)

        return self.comments

    def resolve_tags(self, info):
        """ Resolve project tags """
        del info

        project_data = \
            integrates_dao.get_project_attributes_dynamo(project_name=self.name,
                                                         data_attributes=['tag'])
        self.tags = project_data['tag'] if project_data and 'tag' in project_data else []

        return self.tags

    @require_role(['admin', 'customer'])
    def resolve_users(self, info):
        """ Resolve project users """

        init_emails = integrates_dao.get_project_users(self.name)
        init_email_list = [user[0] for user in init_emails if user[1] == 1]
        user_email_list = util.user_email_filter(init_email_list,
                                                 util.get_jwt_content(info.context)['user_email'])
        self.users = [User(self.name, user_email) for user_email in user_email_list]

        return self.users

    def resolve_has_complete_docs(self, info):
        """ Whether executive report is available or not """
        del info

        self.has_complete_docs = get_project_info(self.name) != []

        return self.has_complete_docs


def validate_release_date(release_date=''):
    """Validate if a finding has a valid relese date."""
    if release_date:
        tzn = pytz.timezone('America/Bogota')
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
    @require_project_access_gql
    def mutate(self, info, **parameters):
        project_name = parameters.get('project_name').lower()
        email = util.get_jwt_content(info.context)["user_email"]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'user_id': comment_id,
            'content': parameters.get('content'),
            'created': current_time,
            'fullname':
                str.join(' ', [info.context.session['first_name'],
                         info.context.session['last_name']]),
            'modified': current_time,
            'parent': int(parameters.get('parent'))
        }
        success = add_comment(project_name, email, comment_data)

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
    @require_project_access_gql
    def mutate(self, info, project_name, tag):
        success = False
        project_name = project_name.lower()
        if validate_project(project_name):
            primary_keys = ['project_name', project_name.lower()]
            table_name = 'FI_projects'
            tag_deleted = integrates_dao.remove_set_element_dynamo(
                table_name, primary_keys, 'tag', tag)
            if tag_deleted:
                success = True
            else:
                rollbar.report_message('Error: \
An error occurred removing a tag', 'error', info.context)

        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to remove tags without the allowed validations')

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
    @require_project_access_gql
    def mutate(self, info, project_name, tags):
        success = False
        project_name = project_name.lower()
        if validate_project(project_name):
            primary_keys = ['project_name', project_name]
            table_name = 'FI_projects'
            if validate_tags(tags):
                tags_added = integrates_dao.add_set_element_dynamo(
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
