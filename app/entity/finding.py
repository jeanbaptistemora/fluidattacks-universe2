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
from graphene import String, ObjectType, Boolean, List, Int, JSONString

from .. import util
from app.dto import finding
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from ..api.drive import DriveAPI

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
        resp = finding.finding_vulnerabilities(finding_id)

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

        Verifies if records were retrieved from formstack. if not, it
        attempts to get them from dynamodb
        """
        del info

        if self.records:
            return self.records
        else:
            dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', self.id)
            if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
                file_info = filter(lambda evidence: evidence['name'] == 'fileRecords', dynamo_evidence[0].get('files'))
                if file_info:
                    file_name = file_info[0]['file_url']
                    self.records = get_records_from_file(self, file_name)
                else:
                    self.records = {}
            else:
                self.records = {}

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
