""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import io
import re
from time import time

import rollbar
import boto3
from backports import csv
from graphql import GraphQLError
from graphene import String, ObjectType, Boolean, List, Int, JSONString, Mutation, Field

from .. import util
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file
from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from ..api.drive import DriveAPI
from ..api.formstack import FormstackAPI
from app.decorators import require_login, require_role, require_finding_access_gql
from app.dto.finding import (
    FindingDTO, finding_vulnerabilities, save_severity,
    has_migrated_evidence
)
from app.domain.finding import (
    migrate_all_files, update_file_to_s3, remove_repeated,
    group_by_state, cast_tracking, get_dynamo_evidence,
    add_file_attribute, migrate_evidence_description,
    list_comments, add_comment
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
    comments = List(GenericScalar)
    observations = List(GenericScalar)
    report_level = String()

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
        self.comments = []
        self.observations = []
        self.report_level = ''

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
                self.success = True
            elif resp.get('vulnerabilities'):
                is_file_valid = validate_formstack_file(resp.get('vulnerabilities'), finding_id, info)
                if is_file_valid:
                    vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                    self.vulnerabilities = [Vulnerability(i) for i in vulnerabilities]
                    self.success = True
                else:
                    self.success = False
                    self.error_message = 'Error in file'
            else:
                vuln_info = {'finding_id': self.id, 'vuln_type': 'old', 'where': resp.get('where')}
                self.vulnerabilities = [Vulnerability(vuln_info)]
                self.success = True

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
            self.report_level = resp.get('reportLevel', '')
        else:
            self.success = False
            self.error_message = 'Finding does not exist'

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
        dynamo_evidence = get_dynamo_evidence(self.id)
        evidence_names = ['animation', 'evidence1', 'evidence2', 'evidence3', 'evidence4', 'evidence5', 'exploitation']
        for evidence_name in evidence_names:
            dyn_url = dynamo_evidence[evidence_name]['url']
            fs_url = formstack_evidence[evidence_name]['url']
            self.evidence[evidence_name]['url'] = dyn_url if dyn_url else fs_url
        return self.evidence

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_comments(self, info):
        """ Resolve comments attribute """

        self.comments = list_comments(
            user_email=util.get_jwt_content(info.context)['user_email'],
            comment_type='comment',
            finding_id=self.id
            )
        return self.comments

    @require_role(['analyst', 'admin'])
    def resolve_observations(self, info):
        """ Resolve observations attribute """

        self.observations = list_comments(
            user_email=util.get_jwt_content(info.context)['user_email'],
            comment_type='observation',
            finding_id=self.id
            )
        return self.observations

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_report_level(self, info):
        """ Resolve report_level attribute """
        del info

        dynamo_value = integrates_dao.get_finding_attributes_dynamo(self.id, ['report_level'])
        fs_value = self.report_level
        self.report_level = dynamo_value['report_level'] if 'report_level' in dynamo_value else fs_value
        return self.report_level

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
        util.invalidate_cache(parameters.get('finding_id'))
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
        util.invalidate_cache(finding_id)
        success = False

        try:
            description_parse = {
                'evidence2_description': 'evidence_route_1',
                'evidence3_description': 'evidence_route_2',
                'evidence4_description': 'evidence_route_3',
                'evidence5_description': 'evidence_route_4',
                'evidence6_description': 'evidence_route_5',
            }
            has_migrated_description = has_migrated_evidence(finding_id)
            if not has_migrated_description:
                generic_dto = FindingDTO()
                api = FormstackAPI()
                submission_data = api.get_submission(finding_id)
                if submission_data is None or 'error' in submission_data:
                    return util.response([], 'error', True)
                else:
                    finding = generic_dto.parse_evidence_info(submission_data, finding_id)
                    finding['id'] = finding_id
                    migrate_evidence_description(finding)
            else:
                # Finding has the description field migrated to dynamo.
                pass
            success = add_file_attribute(
                finding_id,
                description_parse[field],
                'description',
                description)
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
        finding_id = parameters.get('finding_id')
        project = integrates_dao.get_finding_project(finding_id)
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project)
        success = False
        success = save_severity(parameters.get('data'))

        return UpdateSeverity(success=success,
            finding=Finding(info=info, identifier=finding_id))

class AddFindingComment(Mutation):
    """ Add comment to finding """

    class Arguments(object):
        content = String(required=True)
        finding_id = String(required=True)
        parent = String(required=True)
        type = String(required=True)
    success = Boolean()
    comment_id = String()

    @require_login
    @require_role(['analyst', 'customer', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        if parameters.get('type') in ['comment', 'observation']:
            user_email = util.get_jwt_content(info.context)['user_email']
            util.invalidate_cache(parameters.get('finding_id'))
            comment_id = int(round(time() * 1000))
            success = add_comment(
                user_email=user_email,
                user_fullname=str.join(' ', [info.context.session['first_name'], \
                                        info.context.session['last_name']]),
                parent=parameters.get('parent'),
                content=parameters.get('content'),
                comment_type=parameters.get('type'),
                comment_id=comment_id,
                finding_id=parameters.get('finding_id'),
                is_remediation_comment=False
                )
        else:
            raise GraphQLError('Invalid comment type')

        return AddFindingComment(success=success, comment_id=comment_id)
