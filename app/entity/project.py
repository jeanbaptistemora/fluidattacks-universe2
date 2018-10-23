""" GraphQL Entity for Formstack Projects """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from .. import util
import pytz
import datetime
from app.api.formstack import FormstackAPI
from graphene import String, ObjectType, Boolean, List, Int
from ..services import has_access_to_project
from ..dao import integrates_dao
from .finding import Finding


class Project(ObjectType):
    """Formstack Project Class."""

    name = String()
    access = Boolean()
    success = Boolean()
    error_message = String()
    findings = List(Finding)
    open_vulnerabilities = Int()
    subscription = String()

    def __init__(self, info, project_name):
        """Class constructor."""
        self.access = False
        self.name = ""
        self.success = False
        self.error_message = ""
        self.subscription = ""

        if (info.context.session['role'] in ['analyst', 'admin', 'customer'] \
            and has_access_to_project(
                info.context.session['username'],
                project_name.lower(),
                info.context.session['role'])):
            self.name = project_name.lower()
            self.access = True
            api = FormstackAPI()
            finreqset = api.get_findings(self.name)['submissions']
            if finreqset:
                findings = [Finding(info, i['id']) for i in finreqset]
                self.findings = [fin for fin in findings
                                 if fin.project_name.lower() == self.name and validate_release_date(fin.release_date)]
                open_vulnerabilities = [i.open_vulnerabilities for i in self.findings
                                        if i.open_vulnerabilities > 0]
                self.open_vulnerabilities = sum(open_vulnerabilities)
                project_info = integrates_dao.get_project_dynamo(self.name)
                if project_info:
                    self.subscription = project_info[0].get('type')
                else:
                    self.subscription = ""
                self.success = True
            else:
                self.success = False
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve project info without permission')

    def resolve_name(self, info):
        """Resolve name attribute."""
        del info
        return self.name

    def resolve_access(self, info):
        """Resolve access attribute."""
        del info
        return self.access

    def resolve_success(self, info):
        """Resolve success attribute."""
        del info
        return self.success

    def resolve_error_message(self, info):
        """Resolve error_message attribute."""
        del info
        return self.error_message

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


def validate_release_date(release_date=""):
    """Validate if a finding has a valid relese date."""
    if release_date:
        tzn = pytz.timezone('America/Bogota')
        finding_last_vuln = datetime.datetime.strptime(
            release_date.split(" ")[0],
            '%Y-%m-%d'
        )
        last_vuln = finding_last_vuln.replace(tzinfo=tzn).date()
        today_day = datetime.datetime.now(tz=tzn).date()
        result = last_vuln <= today_day
    else:
        result = False
    return result
