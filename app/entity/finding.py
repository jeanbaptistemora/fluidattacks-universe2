""" GraphQL Entity for Formstack Events """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import yaml
from .. import util
from app.dto import finding
from graphene import String, ObjectType, Boolean, Mutation
from ..services import has_access_to_finding
from graphene_file_upload.scalars import Upload
from pykwalify.core import Core
from pykwalify.errors import CoreError

FILE_PATH = "/usr/src/app/app/entity/"


class Finding(ObjectType):
    """Formstack Finding Class."""

    id = String()
    access = Boolean()

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


class UploadFile(Mutation):
    """Upload a file with the vuvlnerabilities."""

    class Arguments(object):
        """Arguments of the class."""

        file_in = Upload()
        finding_id = String()
    access = Boolean()
    success = Boolean()

    @classmethod
    def mutate(self, args, info, **kwargs):
        """Process file input."""
        del args
        self.success = False
        if (info.context.session['role'] in ['analyst', 'customer', 'admin'] \
            and has_access_to_finding(
                info.context.session['access'],
                kwargs.get('finding_id'),
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
                    self.success = True
                except CoreError:
                    self.success = False
        else:
            self.access = False

        return UploadFile(access=self.access, success=self.success)
