""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import io
import re

import boto3
from backports import csv
from graphql import GraphQLError
from graphene import String, ObjectType, Boolean, List, Int, JSONString, Mutation, Field

from .. import util
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from ..api.drive import DriveAPI
from app.decorators import require_login, require_role, require_finding_access_gql
from app.dto.finding import FindingDTO, finding_vulnerabilities
from app.domain.finding import migrate_all_files, update_file_to_s3

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

        finding_id = str(identifier)
        resp = finding_vulnerabilities(finding_id)

        if resp:
            self.id = finding_id
            self.project_name = resp.get('fluidProject')
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

    def resolve_records(self, info):
        """
        Resolve compromised records attribute

        Verifies if there are records in dynamo. if not, it gets them from formstack
        """
        del info

        formstack_records = self.records
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', self.id)
        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            file_info = filter(lambda evidence: evidence['name'] == 'fileRecords', dynamo_evidence[0].get('files'))
            if file_info:
                file_name = file_info[0]['file_url']
                self.records = get_records_from_file(self, file_name)
            else:
                self.records = formstack_records
        else:
            self.records = formstack_records

        return self.records

def get_records_from_file(self, file_name):
    file_id = '/'.join([self.project_name.lower(), self.id, file_name])
    is_s3_file = util.list_s3_objects(client_s3, bucket_s3, file_id)

    if is_s3_file:
        start = file_id.find(self.id) + len(self.id)
        localfile = "/tmp" + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)

        client_s3.download_file(bucket_s3, file_id, tmp_filepath)
        return read_csv(tmp_filepath)
    else:
        if not re.match("[a-zA-Z0-9_-]{20,}", file_name):
            raise Exception('Wrong file id format')
        else:
            drive_api = DriveAPI()
            tmp_filepath = drive_api.download(file_name)

            return read_csv(tmp_filepath)

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
