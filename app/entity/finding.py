""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from .. import util
from app.dto import finding
from graphene import String, ObjectType, Boolean, List, Int
from ..services import has_access_to_finding
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file


class Finding(ObjectType):
    """Formstack Finding Class."""

    id = String()
    access = Boolean()
    success = Boolean()
    error_message = String()
    vulnerabilities = List(
        Vulnerability,
        vuln_type=String(),
        state=String())
    open_vulnerabilities = Int()
    project_name = String()
    release_date = String()

    def __init__(self, info, identifier):
        """Class constructor."""
        self.access = False
        self.id = ""
        self.vulnerabilities = []
        self.success = False
        self.error_message = ""
        self.open_vulnerabilities = 0
        self.project_name = ""
        self.release_date = ""

        finding_id = str(identifier)
        if (info.context.session['role'] in ['analyst', 'admin', 'customer'] \
            and has_access_to_finding(
                info.context.session['access'],
                finding_id,
                info.context.session['role'])):
            self.access = True
            resp = finding.finding_vulnerabilities(finding_id)
            if resp:
                self.id = finding_id
                self.project_name = resp.get('fluidProject')
                if resp.get('releaseDate'):
                    self.release_date = resp.get('releaseDate')
                else:
                    self.release_date = ""
                vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                if vulnerabilities:
                    self.vulnerabilities = [Vulnerability(info, i) for i in vulnerabilities]
                    open_vulnerabilities = [i for i in self.vulnerabilities if i.current_state == "open"]
                    self.open_vulnerabilities = len(open_vulnerabilities)
                elif resp.get("vulnerabilities"):
                    is_file_valid = validate_formstack_file(resp.get("vulnerabilities"), finding_id, info)
                    if is_file_valid:
                        vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                        self.vulnerabilities = [Vulnerability(info, i) for i in vulnerabilities]
                    else:
                        self.success = False
                        self.error_message = "Error in file"
                else:
                    vuln_info = {"finding_id": self.id, "vuln_type": "old", "where": resp.get("where")}
                    self.vulnerabilities = [Vulnerability(info, vuln_info)]
            else:
                self.success = False
                self.error_message = "Finding does not exist"
            self.success = True
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to retrieve finding info without permission')

    def resolve_id(self, info):
        """Resolve id attribute."""
        del info
        return self.id

    def resolve_project_name(self, info):
        """Resolve project_name attribute."""
        del info
        return self.project_name

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

    def resolve_vulnerabilities(self, info, vuln_type="", state=""):
        """Resolve vulnerabilities attribute."""
        del info
        vuln_filtered = self.vulnerabilities
        if vuln_type:
            vuln_filtered = [i for i in vuln_filtered if i.vuln_type == vuln_type]
        if state:
            vuln_filtered = [i for i in vuln_filtered if i.current_state == state]
        return vuln_filtered

    def resolve_open_vulnerabilities(self, info):
        """Resolve open vulnerabilities attribute."""
        del info
        return self.open_vulnerabilities

    def resolve_release_date(self, info):
        """Resolve release date attribute."""
        del info
        return self.release_date
