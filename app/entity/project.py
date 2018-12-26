""" GraphQL Entity for Formstack Projects """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
from __future__ import absolute_import
import pytz
from datetime import datetime, timedelta

import jwt
from graphene import String, ObjectType, List, Int

from __init__ import FI_ORGANIZATION_SECRET, FI_DASHBOARD, FI_ORGANIZATION
from app.api.formstack import FormstackAPI
from ..dao import integrates_dao
from .finding import Finding

class Project(ObjectType):
    """Formstack Project Class."""

    name = String()
    findings = List(Finding)
    open_vulnerabilities = Int()
    subscription = String()
    charts_key = String()

    def __init__(self, info, project_name):
        """Class constructor."""
        self.name = project_name.lower()
        self.subscription = ''
        self.charts_key = ''
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
