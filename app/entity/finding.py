""" GraphQL Entity for Formstack Events """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import yaml
import pytz
import uuid
import rollbar
from .. import util
from app.dto import finding
from graphene import String, ObjectType, Boolean, Mutation, List, JSONString
from ..services import has_access_to_finding
from pykwalify.core import Core
from pykwalify.errors import CoreError, SchemaError
from datetime import datetime
from ..dao import integrates_dao

FILE_PATH = "/usr/src/app/app/entity/"


class Finding(ObjectType):
    """Formstack Finding Class."""

    id = String()
    access = Boolean()
    vulnerabilities = List(JSONString)

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
                vuln = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                self.vulnerabilities = vuln
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

    def resolve_vulnerabilities(self, info):
        """Resolve vulnerabilities attribute."""
        del info
        return self.vulnerabilities


class UploadFile(Mutation):
    """Upload a file with the vulnerabilities."""

    class Arguments(object):
        """Arguments of the class."""

        finding_id = String(required=True)
    access = Boolean()
    success = Boolean()

    @classmethod
    def mutate(self, args, info, **kwargs):
        """Process file input."""
        del args
        self.success = False
        finding_id = kwargs.get('finding_id')
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_finding(
                info.context.session['access'],
                finding_id,
                info.context.session['role'])):
            self.access = True
            file_input = info.context.FILES.get("file", None)
            if file_input:
                vulnerabilities = yaml.load(file_input.read())
                stream = file("/tmp/vulnerabilities.yaml", 'w')
                yaml.dump(vulnerabilities, stream)
                c = Core(source_file="/tmp/vulnerabilities.yaml", schema_files=[FILE_PATH + "schema.yaml"])
                try:
                    c.validate(raise_exception=True)
                    where = ["inputs", "lines", "ports"]
                    for vuln in where:
                        file_vuln = vulnerabilities.get(vuln)
                        if file_vuln:
                            inputs_added = list(
                                map(lambda x, vuln=vuln: add_to_dynamo(x, vuln, finding_id, info),
                                    file_vuln))
                            self.success = all(inputs_added)
                except (CoreError, SchemaError):
                    rollbar.report_message(
                        'Error: An error occurred adding vulnerabilities',
                        'error',
                        info.context)
                    self.success = False
        else:
            self.access = False
        return UploadFile(access=self.access, success=self.success)


def get_last_state(state_list):
    """Get the last state of a vulnerability."""
    for state in state_list:
        current_date = datetime.today().min
        state_date = datetime.strptime(state.get('date'), '%Y-%m-%d %H:%M:%S')
        current_state = ""
        if state_date > current_date:
            current_date = state_date
            current_state = state.get('state')
    return current_state


def add_to_dynamo(item, vuln_type, finding_id, info):
    """Add vulnerability to dynamo."""
    historic_state = []
    tzn = pytz.timezone('America/Bogota')
    where_haders = {}
    where_haders["inputs"] = {"where": "url", "specific": "field"}
    where_haders["lines"] = {"where": "path", "specific": "line"}
    where_haders["ports"] = {"where": "ip", "specific": "port"}
    response = False
    current_day = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    for vuln, vuln_info in where_haders.items():
        if vuln_type == vuln:
            where = item.get(vuln_info.get("where"))
            specific = item.get(vuln_info.get("specific"))
            vuln_exits = integrates_dao.get_vulnerability_dynamo(finding_id, vuln, where, specific)
            if vuln_exits:
                response = update_state(vuln_exits, item, finding_id, current_day)
            else:
                data = {}
                data["vuln_type"] = vuln
                data["where"] = where
                data["specific"] = specific
                data["finding_id"] = finding_id
                data["UUID"] = str(uuid.uuid4())
                if item.get('state'):
                    historic_state.append({'date': current_day, 'state': item.get('state')})
                    data["historic_state"] = historic_state
                    response = integrates_dao.add_vulnerability_dynamo("FI_vulnerabilities", data)
                else:
                    util.cloudwatch_log(
                        info.context,
                        'Security: Attempted to add vulnerability without state')
    return response


def update_state(vuln_exits, item, finding_id, current_day):
    """Update vulnerability state."""
    last_state = get_last_state(vuln_exits[0].get('historic_state'))
    response = False
    if last_state != item.get('state'):
        historic_state = []
        current_state = {'date': current_day, 'state': item.get('state')}
        historic_state.append(current_state)
        response = integrates_dao.update_state_dynamo(
            finding_id,
            vuln_exits[0].get("UUID"),
            "historic_state",
            historic_state,
            vuln_exits)
    else:
        response = False
    return response
