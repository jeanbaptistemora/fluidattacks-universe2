""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import io
import re

import rollbar
import boto3
from backports import csv
from graphql import GraphQLError
from graphene import String, ObjectType, Boolean, List, Int, JSONString, Mutation, Field

from .. import util
from ..utils import forms as forms_utils
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from ..api.drive import DriveAPI
from ..api.formstack import FormstackAPI
from app.decorators import require_login, require_role, require_finding_access_gql
from app.dto.finding import FindingDTO, finding_vulnerabilities, save_severity
from app.domain.finding import (
    migrate_all_files, update_file_to_s3, remove_repeated,
    group_by_state, cast_tracking
)
from graphene.types.generic import GenericScalar

client_s3 = boto3.client('s3',
                            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = FI_AWS_S3_BUCKET

class Finding(ObjectType):
    """Formstack Finding Class."""

    id = String()
    success = Boolean()
    error_message = String()
    vulnerabilities = List(
        Vulnerability,
        vuln_type=String(),
        state=String())
    open_vulnerabilities = Int()
    closed_vulnerabilities = Int()
    project_name = String()
    release_date = String()
    records = JSONString()
    tracking = List(GenericScalar)
    severity = GenericScalar()
    exploit = String()
    evidence = GenericScalar()

    def __init__(self, info, identifier):
        """Class constructor."""
        self.id = ''
        self.vulnerabilities = []
        self.success = False
        self.error_message = ''
        self.open_vulnerabilities = 0
        self.closed_vulnerabilities = 0
        self.project_name = ''
        self.release_date = ''
        self.records = {}
        self.severity = {}
        self.tracking = []

        finding_id = str(identifier)
        resp = finding_vulnerabilities(finding_id)

        if resp:
            self.id = finding_id
            self.project_name = resp.get('projectName')
            if resp.get('releaseDate'):
                self.release_date = resp.get('releaseDate')
            else:
                self.release_date = ''
            vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
            if vulnerabilities:
                self.vulnerabilities = [Vulnerability(i) for i in vulnerabilities]
                open_vulnerabilities = [i for i in self.vulnerabilities if i.current_state == 'open']
                self.open_vulnerabilities = len(open_vulnerabilities)
                closed_vulnerabilities = [i for i in self.vulnerabilities if i.current_state == 'closed']
                self.closed_vulnerabilities = len(closed_vulnerabilities)
            elif resp.get('vulnerabilities'):
                is_file_valid = validate_formstack_file(resp.get('vulnerabilities'), finding_id, info)
                if is_file_valid:
                    vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                    self.vulnerabilities = [Vulnerability(i) for i in vulnerabilities]
                else:
                    self.success = False
                    self.error_message = 'Error in file'
            else:
                vuln_info = {'finding_id': self.id, 'vuln_type': 'old', 'where': resp.get('where')}
                self.vulnerabilities = [Vulnerability(vuln_info)]

            if 'fileRecords' in resp.keys():
                self.records = get_records_from_file(self, resp['fileRecords'])
            else:
                self.records = {}

            if 'exploit' in resp.keys():
                self.exploit = resp['exploit']
            else:
                self.exploit = ''
            severity_fields = ['accessVector', 'accessComplexity',
                               'authentication', 'exploitability',
                               'confidentialityImpact', 'integrityImpact',
                               'availabilityImpact', 'resolutionLevel',
                               'confidenceLevel', 'collateralDamagePotential',
                               'findingDistribution', 'confidentialityRequirement',
                               'integrityRequirement', 'availabilityRequirement']
            self.severity = {k: resp.get(k) for k in severity_fields}

            self.evidence = {
                'animation': { 'url': resp.get('animation', ''), 'description': '' },
                'evidence1': { 'url': resp.get('evidence_route_1', ''), 'description': resp.get('evidence_description_1', '') },
                'evidence2': { 'url': resp.get('evidence_route_2', ''), 'description': resp.get('evidence_description_2', '') },
                'evidence3': { 'url': resp.get('evidence_route_3', ''), 'description': resp.get('evidence_description_3', '') },
                'evidence4': { 'url': resp.get('evidence_route_4', ''), 'description': resp.get('evidence_description_4', '') },
                'evidence5': { 'url': resp.get('evidence_route_5', ''), 'description': resp.get('evidence_description_5', '') },
                'exploitation': { 'url': resp.get('exploitation', ''), 'description': '' },
            }

        else:
            self.success = False
            self.error_message = 'Finding does not exist'
        self.success = True

    def resolve_id(self, info):
        """Resolve id attribute."""
        del info
        return self.id

    def resolve_project_name(self, info):
        """Resolve project_name attribute."""
        del info
        return self.project_name

    def resolve_success(self, info):
        """Resolve success attribute."""
        del info
        return self.success

    def resolve_error_message(self, info):
        """Resolve error_message attribute."""
        del info
        return self.error_message

    def resolve_vulnerabilities(self, info, vuln_type='', state=''):
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

    def resolve_closed_vulnerabilities(self, info):
        """Resolve closed vulnerabilities attribute."""
        del info
        return self.closed_vulnerabilities

    def resolve_tracking(self, info):
        """Resolve tracking attribute."""
        del info
        if (self.release_date and
            (self.open_vulnerabilities or
                self.closed_vulnerabilities)):
            vuln_casted = remove_repeated(self.vulnerabilities)
            tracking = group_by_state(vuln_casted)
            order_tracking = sorted(tracking.items())
            tracking_casted = cast_tracking(order_tracking)
            self.tracking = tracking_casted
        else:
            self.tracking = []
        return self.tracking

    def resolve_records(self, info):
        """
        Resolve compromised records attribute

        Verifies if there are records in dynamo. if not, it gets them from formstack
        """
        del info

        formstack_records = self.records
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', self.id)
        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            file_info = list(filter(lambda evidence: evidence['name'] == 'fileRecords', dynamo_evidence[0].get('files')))
            if file_info:
                file_name = file_info[0]['file_url']
                self.records = get_records_from_file(self, file_name)
            else:
                self.records = formstack_records
        else:
            self.records = formstack_records

        return self.records

    def resolve_severity(self, info):
        """ Resolve severity values from Formstack """
        del info

        return self.severity

    def resolve_exploit(self, info):
        """
        Resolve exploit attribute

        Verifies if the exploit is in dynamo. if not, it gets the filename from formstack
        """
        del info

        formstack_exploit = '' if self.exploit == '' else get_exploit_from_file(self, self.exploit)
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', self.id)
        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            file_info = list(filter(lambda evidence: evidence['name'] == 'exploit', dynamo_evidence[0].get('files')))
            if file_info:
                file_name = file_info[0]['file_url']
                self.exploit = get_exploit_from_file(self, file_name)
            else:
                self.exploit = formstack_exploit
        else:
            self.exploit = formstack_exploit

        return self.exploit

    def resolve_evidence(self, info):
        """
        Resolve evidence attribute

        Verifies if the evidence is in dynamo. if not, it gets the filenames from formstack
        """
        del info

        formstack_evidence = self.evidence
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', self.id)

        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            self.evidence = {
                'animation': { 'url': filter_evidence_filename(dynamo_evidence, 'animation'), 'description': '' },
                'evidence1': {
                    'url': filter_evidence_filename(dynamo_evidence, 'evidence_route_1'),
                    'description': formstack_evidence['evidence1'].get('description')
                },
                'evidence2': {
                    'url': filter_evidence_filename(dynamo_evidence, 'evidence_route_2'),
                    'description': formstack_evidence['evidence2'].get('description')
                },
                'evidence3': {
                    'url': filter_evidence_filename(dynamo_evidence, 'evidence_route_3'),
                    'description': formstack_evidence['evidence3'].get('description')
                },
                'evidence4': {
                    'url': filter_evidence_filename(dynamo_evidence, 'evidence_route_4'),
                    'description': formstack_evidence['evidence4'].get('description')
                },
                'evidence5': {
                    'url': filter_evidence_filename(dynamo_evidence, 'evidence_route_5'),
                    'description': formstack_evidence['evidence5'].get('description')
                },
                'exploitation': { 'url': filter_evidence_filename(dynamo_evidence, 'exploitation'), 'description': '' },
            }
        else:
            self.evidence = formstack_evidence

        return self.evidence

def filter_evidence_filename(dynamo_evidence, name):
    evidence_info = filter(lambda evidence: evidence['name'] == name, dynamo_evidence[0].get('files'))
    return evidence_info[0]['file_url'] if evidence_info else ''

def get_exploit_from_file(self, file_name):
    return read_script(download_evidence_file(self, file_name))

def get_records_from_file(self, file_name):
    return read_csv(download_evidence_file(self, file_name))

def download_evidence_file(self, file_name):
    file_id = '/'.join([self.project_name.lower(), self.id, file_name])
    is_s3_file = util.list_s3_objects(client_s3, bucket_s3, file_id)

    if is_s3_file:
        start = file_id.find(self.id) + len(self.id)
        localfile = '/tmp' + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)

        client_s3.download_file(bucket_s3, file_id, tmp_filepath)
        return tmp_filepath
    else:
        if not re.match('[a-zA-Z0-9_-]{20,}', file_name):
            raise Exception('Wrong file id format')
        else:
            drive_api = DriveAPI()
            tmp_filepath = drive_api.download(file_name)

            return tmp_filepath

def read_script(script_file):
    if util.assert_file_mime(script_file, ['text/x-python', 'text/x-c', 'text/plain', 'text/html']):
        with open(script_file, 'r') as file_obj:
            return file_obj.read()
    else:
        raise GraphQLError('Invalid exploit file format')

def read_csv(csv_file):
    file_content = []

    with io.open(csv_file, 'r', encoding='utf-8', errors='ignore') as file_obj:
        try:
            csvReader = csv.reader(x.replace('\0', '') for x in file_obj)
            cont = 0
            header = csvReader.next()
            for row in csvReader:
                if cont <= 1000:
                    file_content.append(util.list_to_dict(header, row))
                    cont += 1
                else:
                    break
            return file_content
        except csv.Error:
            raise GraphQLError('Invalid record file format')

class UpdateEvidence(Mutation):
    """ Update evidence files """

    class Arguments(object):
        finding_id = String(required=True)
        project_name = String(required=True)
        id = String(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        success = False
        uploaded_file = info.context.FILES.get('document', '')

        if util.assert_uploaded_file_mime(uploaded_file,
            ['image/gif', 'image/png', 'text/x-python', 'text/x-c', 'text/plain', 'text/html']
            ):
            if evidence_exceeds_size(uploaded_file, int(parameters.get('id'))):
                util.cloudwatch_log(info.context, 'Security: Attempted to upload evidence file heavier than allowed')
                raise GraphQLError('File exceeds the size limits')
            else:
                fieldNum = FindingDTO()
                fieldname = [
                    ['animation', fieldNum.ANIMATION], ['exploitation', fieldNum.EXPLOTATION],
                    ['evidence_route_1', fieldNum.DOC_ACHV1], ['evidence_route_2', fieldNum.DOC_ACHV2],
                    ['evidence_route_3', fieldNum.DOC_ACHV3], ['evidence_route_4', fieldNum.DOC_ACHV4],
                    ['evidence_route_5', fieldNum.DOC_ACHV5], ['exploit', fieldNum.EXPLOIT],
                    ['fileRecords', fieldNum.REG_FILE]
                ]
                file_id = '{project}/{finding_id}/{project}-{finding_id}'.format(
                    project=parameters.get('project_name'),
                    finding_id=parameters.get('finding_id')
                )

                migrate_all_files(parameters, file_id, info.context)
                success = update_file_to_s3(
                            parameters,
                            fieldname[int(parameters.get('id'))][1],
                            fieldname[int(parameters.get('id'))][0],
                            uploaded_file, file_id)
        else:
            util.cloudwatch_log(info.context, 'Security: Attempted to upload evidence file with a non-allowed format')
            raise GraphQLError('Extension not allowed')

        return UpdateEvidence(success=success, \
            finding=Finding(info=info, identifier=parameters.get('finding_id')))

class UpdateEvidenceDescription(Mutation):
    """ Update evidence description """

    class Arguments(object):
        description = String(required=True)
        finding_id = String(required=True)
        field = String(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, finding_id, field, description):
        success = False

        try:
            finding_dto = FindingDTO()
            evidence_description_dict = finding_dto.parse_evidence_description(field, description)
            formstack_payload = forms_utils.to_formstack(evidence_description_dict['data'])
            api = FormstackAPI()
            success = api.update(finding_id, formstack_payload)['success']
        except KeyError:
            rollbar.report_message('Error: An error occurred updating evidence description', 'error', info.context)

        return UpdateEvidenceDescription(success=success, finding=Finding(info=info, identifier=finding_id))

def evidence_exceeds_size(uploaded_file, evidence_type):
    ANIMATION = 0
    EXPLOITATION = 1
    EVIDENCE = [2, 3, 4, 5, 6]
    EXPLOIT = 7
    RECORDS = 8
    MIB = 1048576

    if evidence_type == ANIMATION:
        return uploaded_file.size > 10 * MIB
    elif evidence_type == EXPLOITATION:
        return uploaded_file.size > 2 * MIB
    elif evidence_type in EVIDENCE:
        return uploaded_file.size > 2 * MIB
    elif evidence_type == EXPLOIT:
        return uploaded_file.size > 1 * MIB
    elif evidence_type == RECORDS:
        return uploaded_file.size > 1 * MIB
    else:
        util.cloudwatch_log_plain('Security: Attempted to upload an unknown type of evidence')
        raise Exception('Invalid evidence id')

class UpdateSeverity(Mutation):

    class Arguments(object):
        finding_id = String(required=True)
        data = GenericScalar(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        success = False
        success = save_severity(parameters.get('data'))

        return UpdateSeverity(success=success,
            finding=Finding(info=info, identifier=parameters.get('finding_id')))
