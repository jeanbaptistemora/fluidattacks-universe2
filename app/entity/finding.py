""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from .. import util
from app.dto import finding
from graphene import String, ObjectType, Boolean, List
from ..services import has_access_to_finding
from ..dao import integrates_dao
from .vulnerability import Vulnerability


class Finding(ObjectType):
    """Formstack Finding Class."""

    id = String()
    access = Boolean()
    vulnerabilities = List(
        Vulnerability,
        vuln_type=String(),
        state=String())

    def __init__(self, info, identifier):
        """Class constructor."""
        self.access = False
        self.id = ""

        finding_id = str(identifier)
        if (info.context.session['role'] in ['analyst', 'admin'] \
            and has_access_to_finding(
                info.context.session['access'],
                finding_id,
                info.context.session['role'])):
            self.access = True
            resp = finding.finding_vulnerabilities(finding_id)
            if resp:
                self.id = finding_id
                vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                self.vulnerabilities = [Vulnerability(info, i) for i in vulnerabilities]
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve finding info without permission')

    def resolve_id(self, info):
        """Resolve id attribute."""
        del info
        return self.id

    def resolve_access(self, info):
        """Resolve access attribute."""
        del info
        return self.access

    def resolve_vulnerabilities(self, info, vuln_type="", state=""):
        """Resolve vulnerabilities attribute."""
        del info
        vuln_filtered = self.vulnerabilities
        if vuln_type:
            vuln_filtered = [i for i in vuln_filtered if i.vuln_type == vuln_type]
        if state:
            vuln_filtered = [i for i in vuln_filtered if i.current_state == state]
        return vuln_filtered
