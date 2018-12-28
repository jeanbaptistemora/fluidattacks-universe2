""" GraphQL Entity for Formstack Projects """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from __future__ import absolute_import
import pytz
import time
from datetime import datetime, timedelta

import jwt
from graphene import String, ObjectType, List, Int, Boolean, Mutation
from graphene.types.generic import GenericScalar

from __init__ import FI_ORGANIZATION_SECRET, FI_DASHBOARD, FI_ORGANIZATION
from ..dao import integrates_dao
from .finding import Finding
from app import util
from app.decorators import require_role, require_login, require_project_access_gql

class Project(ObjectType):
    """Formstack Project Class."""

    name = String()
    findings = List(Finding)
    open_vulnerabilities = Int()
    subscription = String()
    charts_key = String()
    comments = List(GenericScalar)
    tags = List(String)

    def __init__(self, info, project_name):
        """Class constructor."""
        self.name = project_name.lower()
        self.subscription = ''
        self.charts_key = ''
        self.comments = []
        self.tags = []
        finreqset = integrates_dao.get_findings_dynamo(self.name, 'finding_id')

        if finreqset:
            findings = [Finding(info, i['finding_id']) for i in finreqset]
            self.findings = [fin for fin in findings
                             if validate_release_date(fin.release_date)]
            open_vulnerabilities = [i.open_vulnerabilities for i in self.findings
                                    if i.open_vulnerabilities > 0]
            self.open_vulnerabilities = sum(open_vulnerabilities)
            project_info = integrates_dao.get_project_dynamo(self.name)
            if project_info:
                self.subscription = project_info[0].get('type')
            else:
                self.subscription = ''

    def resolve_name(self, info):
        """Resolve name attribute."""
        del info
        return self.name

    def resolve_findings(self, info):
        """Resolve findings attribute."""
        del info
        return self.findings

    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        del info
        return self.open_vulnerabilities

    def resolve_subscription(self, info):
        """Resolve subscription attribute."""
        del info
        return self.subscription

    def resolve_charts_key(self, info):
        """ Resolve chartio token """
        del info

        charts_token = jwt.encode(
            {
              'organization': int(FI_ORGANIZATION),
              'dashboard': int(FI_DASHBOARD),
              'exp': datetime.utcnow() + timedelta(seconds=30),
              'env': {'PROJECT': self.name}
            },
            FI_ORGANIZATION_SECRET,
            algorithm='HS256'
        )
        self.charts_key = '%s/%s' % (FI_DASHBOARD, charts_token)

        return self.charts_key

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_comments(self, info):
        comments = integrates_dao.get_project_comments_dynamo(self.name)

        for comment in comments:
            comment_data = {
                'content': comment['content'],
                'created': comment['created'],
                'created_by_current_user': comment['email'] == util.get_jwt_content(info.context)["user_email"],
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

        project_data = integrates_dao.get_project_attributes_dynamo(project_name=self.name, data_attributes=['tag'])
        self.tags = project_data['tag'] if project_data and 'tag' in project_data else []

        return self.tags

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
        util.invalidate_cache(project_name)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'user_id': comment_id,
            'content': parameters.get('content'),
            'created': current_time,
            'fullname': str.join(' ', [info.context.session['first_name'], info.context.session['last_name']]),
            'modified': current_time,
            'parent': int(parameters.get('parent'))
        }
        success = integrates_dao.add_project_comment_dynamo(project_name, email, comment_data)

        return AddProjectComment(success=success, comment_id=comment_id)
