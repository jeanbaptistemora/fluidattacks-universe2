""" GraphQL Entity for Formstack Findings """
# pylint: disable=F0401
# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
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
from graphene import String, ObjectType, Boolean, List, Int, Float, JSONString, Mutation, Field
from graphene.types.generic import GenericScalar

from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from app.decorators import require_login, require_role, require_finding_access_gql
from app.dto.finding import (
    FindingDTO, finding_vulnerabilities, save_severity,
    has_migrated_evidence, get_project_name
)
from app.domain.finding import (
    migrate_all_files, update_file_to_s3, remove_repeated,
    group_by_state, cast_tracking, get_dynamo_evidence,
    add_file_attribute, migrate_evidence_description,
    list_comments, add_comment, verify_finding,
    get_unique_dict, get_tracking_dict, request_verification,
    update_description, update_treatment
)
from .. import util
from ..dao import integrates_dao
from .vulnerability import Vulnerability, validate_formstack_file
from ..api.drive import DriveAPI
from ..api.formstack import FormstackAPI

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

BUCKET_S3 = FI_AWS_S3_BUCKET


class Finding(ObjectType):  # noqa pylint: disable=too-many-instance-attributes
    """Formstack Finding Class."""

    id = String()  # noqa pylint: disable=invalid-name
    success = Boolean()
    error_message = String()
    state = String()
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
    title = String()
    scenario = String()
    actor = String()
    description = String()
    requirements = String()
    attack_vector = String()
    threat = String()
    recommendation = String()
    affected_systems = String()
    compromised_attributes = String()
    compromised_records = Int()
    cwe_url = String()
    bts_url = String()
    treatment = String()
    treatment_manager = String()
    treatment_justification = String()
    remediated = Boolean()

    # Additional attributes of detailed findings
    client_code = String()
    client_project = String()
    probability = String()
    detailed_severity = Int()
    risk = String()
    risk_level = String()
    ambit = String()
    category = String()

    # pylint: disable=too-many-statements
    def __init__(self, info, identifier):
        """Class constructor."""
        set_initial_values(self)

        finding_id = str(identifier)
        resp = finding_vulnerabilities(finding_id)

        if resp:
            self.id = finding_id  # noqa pylint: disable=invalid-name
            self.project_name = resp.get('projectName')
            self.release_date = resp.get('releaseDate', '')
            vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
            if vulnerabilities:
                self.vulnerabilities = [Vulnerability(i) for i in vulnerabilities]
                open_vulnerabilities = \
                    [i for i in self.vulnerabilities if i.current_state == 'open']
                self.open_vulnerabilities = len(open_vulnerabilities)
                closed_vulnerabilities = \
                    [i for i in self.vulnerabilities if i.current_state == 'closed']
                self.closed_vulnerabilities = len(closed_vulnerabilities)
                self.success = True
            elif resp.get('vulnerabilities'):
                is_file_valid = \
                    validate_formstack_file(resp.get('vulnerabilities'), finding_id, info)
                if is_file_valid:
                    vulnerabilities = integrates_dao.get_vulnerabilities_dynamo(finding_id)
                    self.vulnerabilities = [Vulnerability(i) for i in vulnerabilities]
                    self.success = True
                else:
                    self.success = False
                    self.error_message = 'Error in file'
            else:
                vuln_info = \
                    {'finding_id': self.id, 'vuln_type': 'old',
                     'where': resp.get('where')}
                self.vulnerabilities = [Vulnerability(vuln_info)]
                self.success = True

            if 'fileRecords' in resp.keys():
                self.records = get_records_from_file(self, resp['fileRecords'])
            else:
                self.records = {}

            self.exploit = resp.get('exploit', '')
            severity_fields = ['accessVector', 'accessComplexity',
                               'authentication', 'exploitability',
                               'confidentialityImpact', 'integrityImpact',
                               'availabilityImpact', 'resolutionLevel',
                               'confidenceLevel', 'collateralDamagePotential',
                               'findingDistribution', 'confidentialityRequirement',
                               'integrityRequirement', 'availabilityRequirement']
            self.severity = {k: resp.get(k) for k in severity_fields}

            self.evidence = {
                'animation': {'url': resp.get('animation', ''), 'description': ''},
                'evidence1':
                    {'url': resp.get('evidence_route_1', ''),
                     'description': resp.get('evidence_description_1', '')},
                'evidence2':
                    {'url': resp.get('evidence_route_2', ''),
                     'description': resp.get('evidence_description_2', '')},
                'evidence3':
                    {'url': resp.get('evidence_route_3', ''),
                     'description': resp.get('evidence_description_3', '')},
                'evidence4':
                    {'url': resp.get('evidence_route_4', ''),
                     'description': resp.get('evidence_description_4', '')},
                'evidence5':
                    {'url': resp.get('evidence_route_5', ''),
                     'description': resp.get('evidence_description_5', '')},
                'exploitation':
                    {'url': resp.get('exploitation', ''), 'description': ''},
            }
            self.report_level = resp.get('reportLevel', '')
            self.title = resp.get('finding', '')
            self.scenario = resp.get('scenario', '')
            self.actor = resp.get('actor', '')
            self.description = resp.get('vulnerability', '')
            self.requirements = resp.get('requirements', '')
            self.attack_vector = resp.get('attackVector', '')
            self.threat = resp.get('threat', '')
            self.recommendation = resp.get('effectSolution', '')
            self.affected_systems = resp.get('affectedSystems', '')
            self.compromised_attributes = resp.get('records', '')
            self.compromised_records = int(resp.get('recordsNumber', '0'))
            self.cwe_url = resp.get('cwe', '')
            self.bts_url = resp.get('externalBts', '')
            self.treatment = resp.get('treatment', '')
            self.treatment_manager = resp.get('treatmentManager', '')
            self.treatment_justification = resp.get('treatmentJustification', '')
            self.client_code = resp.get('clientCode', '')
            self.client_project = resp.get('clientProject', '')
            self.probability = resp.get('probability', '')
            self.detailed_severity = int(resp.get('severity', '0'))
            self.risk = resp.get('risk', '')
            self.risk_level = resp.get('riskValue', '')
            self.ambit = resp.get('ambit', '')
            self.category = resp.get('category', '')
            self.state = resp.get('estado', '')
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
            unique_dict = get_unique_dict(vuln_casted)
            tracking = get_tracking_dict(unique_dict)
            tracking_grouped = group_by_state(tracking)
            order_tracking = sorted(tracking_grouped.items())
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
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings',
                                                         'finding_id', self.id)
        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            file_info = \
                list(filter(lambda evidence: evidence['name'] == 'fileRecords',
                            dynamo_evidence[0].get('files')))
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

        formstack_exploit = \
            '' if self.exploit == '' else get_exploit_from_file(self, self.exploit)
        dynamo_evidence = integrates_dao.get_data_dynamo('FI_findings',
                                                         'finding_id', self.id)
        if dynamo_evidence and 'files' in dynamo_evidence[0].keys():
            file_info = \
                list(filter(lambda evidence: evidence['name'] == 'exploit',
                            dynamo_evidence[0].get('files')))
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
        evidence_names = ['animation', 'evidence1', 'evidence2', 'evidence3',
                          'evidence4', 'evidence5', 'exploitation']
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

        return self.report_level

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_title(self, info):
        """ Resolve title attribute """
        del info

        return self.title

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_scenario(self, info):
        """ Resolve scenario attribute """
        del info

        return self.scenario

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_actor(self, info):
        """ Resolve actor attribute """
        del info

        return self.actor

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_description(self, info):
        """ Resolve description attribute """
        del info

        return self.description

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_requirements(self, info):
        """ Resolve requirements attribute """
        del info

        return self.requirements

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_attack_vector(self, info):
        """ Resolve requirements attribute """
        del info

        return self.attack_vector

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_threat(self, info):
        """ Resolve threat attribute """
        del info

        return self.threat

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_recommendation(self, info):
        """ Resolve recommendation attribute """
        del info

        return self.recommendation

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_affected_systems(self, info):
        """ Resolve affected_systems attribute """
        del info

        return self.affected_systems

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_compromised_attributes(self, info):
        """ Resolve compromised_attributes attribute """
        del info

        return self.compromised_attributes

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_compromised_records(self, info):
        """ Resolve compromised_records attribute """
        del info

        return self.compromised_records

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_cwe_url(self, info):
        """ Resolve cwe_url attribute """
        del info

        return self.cwe_url

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_bts_url(self, info):
        """ Resolve bts_url attribute """
        del info

        return self.bts_url

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_treatment(self, info):
        """ Resolve treatment attribute """
        del info

        return self.treatment

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_treatment_manager(self, info):
        """ Resolve treatment_manager attribute """
        del info

        return self.treatment_manager

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_treatment_justification(self, info):
        """ Resolve treatment_justification attribute """
        del info

        return self.treatment_justification

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_client_code(self, info):
        """ Resolve client_code attribute """
        del info

        return self.client_code

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_client_project(self, info):
        """ Resolve client_project attribute """
        del info

        return self.client_project

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_probability(self, info):
        """ Resolve probability attribute """
        del info

        return self.probability

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_detailed_severity(self, info):
        """ Resolve detailed_severity attribute """
        del info

        return self.detailed_severity

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_risk(self, info):
        """ Resolve risk attribute """
        del info

        return self.risk

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_risk_level(self, info):
        """ Resolve risk_level attribute """
        del info

        return self.risk_level

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_ambit(self, info):
        """ Resolve ambit attribute """
        del info

        return self.ambit

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_category(self, info):
        """ Resolve category attribute """
        del info

        return self.category

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_state(self, info):
        """ Resolve state attribute """
        del info

        return self.state

    @require_role(['analyst', 'customer', 'admin'])
    def resolve_remediated(self, info):
        """ Resolve remediated attribute """
        del info

        remediations = integrates_dao.get_remediated_dynamo(int(self.id))
        self.remediated = remediations[-1]['remediated'] if remediations else False

        return self.remediated


def set_initial_values(self):
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
    self.title = ''
    self.scenario = ''
    self.actor = ''
    self.description = ''
    self.requirements = ''
    self.attack_vector = ''
    self.threat = ''
    self.recommendation = ''
    self.affected_systems = ''
    self.compromised_attributes = ''
    self.compromised_records = 0
    self.cwe_url = ''
    self.bts_url = ''
    self.treatment = ''
    self.treatment_manager = ''
    self.treatment_justification = ''


def get_exploit_from_file(self, file_name):
    return read_script(download_evidence_file(self, file_name))


def get_records_from_file(self, file_name):
    return read_csv(download_evidence_file(self, file_name))


def download_evidence_file(self, file_name):
    file_id = '/'.join([self.project_name.lower(), self.id, file_name])
    is_s3_file = util.list_s3_objects(CLIENT_S3, BUCKET_S3, file_id)

    if is_s3_file:
        start = file_id.find(self.id) + len(self.id)
        localfile = '/tmp' + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)

        CLIENT_S3.download_file(BUCKET_S3, file_id, tmp_filepath)
        return tmp_filepath
    else:
        if not re.match('[a-zA-Z0-9_-]{20,}', file_name):
            raise Exception('Wrong file id format')
        else:
            drive_api = DriveAPI()
            tmp_filepath = drive_api.download(file_name)

            return tmp_filepath


def read_script(script_file):
    if util.assert_file_mime(script_file, ['text/x-python', 'text/x-c',
                                           'text/plain', 'text/html']):
        with open(script_file, 'r') as file_obj:
            return file_obj.read()
    else:
        raise GraphQLError('Invalid exploit file format')


def read_csv(csv_file):
    file_content = []

    with io.open(csv_file, 'r', encoding='utf-8', errors='ignore') as file_obj:
        try:
            csv_reader = csv.reader(x.replace('\0', '') for x in file_obj)
            cont = 0
            header = csv_reader.next()
            for row in csv_reader:
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
        id = String(required=True)  # noqa pylint: disable=invalid-name
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        success = False
        uploaded_file = info.context.FILES.get('document', '')

        if util.assert_uploaded_file_mime(uploaded_file,
                                          ['image/gif',
                                           'image/png',
                                           'text/x-python',
                                           'text/x-c',
                                           'text/plain',
                                           'text/html']):
            if evidence_exceeds_size(uploaded_file, int(parameters.get('id'))):
                util.cloudwatch_log(info.context,
                                    'Security: \
Attempted to upload evidence file heavier than allowed')
                raise GraphQLError('File exceeds the size limits')
            else:
                field_num = FindingDTO()
                fieldname = [
                    ['animation', field_num.ANIMATION],
                    ['exploitation', field_num.EXPLOTATION],
                    ['evidence_route_1', field_num.DOC_ACHV1],
                    ['evidence_route_2', field_num.DOC_ACHV2],
                    ['evidence_route_3', field_num.DOC_ACHV3],
                    ['evidence_route_4', field_num.DOC_ACHV4],
                    ['evidence_route_5', field_num.DOC_ACHV5],
                    ['exploit', field_num.EXPLOIT],
                    ['fileRecords', field_num.REG_FILE]
                ]
                project_name = get_project_name(parameters.get('finding_id')).lower()
                file_id = '{project}/{finding_id}/{project}-{finding_id}'.format(
                    project=project_name,
                    finding_id=parameters.get('finding_id')
                )

                migrate_all_files(parameters, file_id, info.context)
                success = update_file_to_s3(parameters,
                                            fieldname[int(parameters.get('id'))][1],
                                            fieldname[int(parameters.get('id'))][0],
                                            uploaded_file, file_id)
        else:
            util.cloudwatch_log(info.context,
                                'Security: \
Attempted to upload evidence file with a non-allowed format')
            raise GraphQLError('Extension not allowed')

        ret = UpdateEvidence(success=success,
                             finding=Finding(info=info,
                                             identifier=parameters.get('finding_id')))
        util.invalidate_cache(parameters.get('finding_id'))
        return ret


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
            rollbar.report_message('Error: \
An error occurred updating evidence description', 'error', info.context)

        ret = \
            UpdateEvidenceDescription(success=success,
                                      finding=Finding(info=info,
                                                      identifier=finding_id))
        util.invalidate_cache(finding_id)
        return ret


def evidence_exceeds_size(uploaded_file, evidence_type):
    animation = 0
    exploitation = 1
    evidence = [2, 3, 4, 5, 6]
    exploit = 7
    records = 8
    mib = 1048576

    if evidence_type == animation:
        return uploaded_file.size > 10 * mib
    elif evidence_type == exploitation:
        return uploaded_file.size > 2 * mib
    elif evidence_type in evidence:
        return uploaded_file.size > 2 * mib
    elif evidence_type == exploit:
        return uploaded_file.size > 1 * mib
    elif evidence_type == records:
        return uploaded_file.size > 1 * mib
    else:
        util.cloudwatch_log_plain('Security: \
Attempted to upload an unknown type of evidence')
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
        success = False
        success = save_severity(parameters.get('data'))

        ret = UpdateSeverity(success=success,
                             finding=Finding(info=info,
                                             identifier=finding_id))
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project)
        return ret


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
            comment_id = int(round(time() * 1000))
            success = add_comment(
                user_email=user_email,
                user_fullname=str.join(' ', [info.context.session['first_name'],
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

        ret = AddFindingComment(success=success, comment_id=comment_id)
        util.invalidate_cache(parameters.get('finding_id'))
        return ret


class VerifyFinding(Mutation):
    """ Verify a finding """

    class Arguments(object):
        finding_id = String(required=True)
    success = Boolean()

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        user_email = util.get_jwt_content(info.context)['user_email']
        success = verify_finding(
            company=info.context.session['company'],
            finding_id=parameters.get('finding_id'),
            user_email=user_email
        )

        ret = VerifyFinding(success=success)
        util.invalidate_cache(parameters.get('finding_id'))
        return ret


class RequestVerification(Mutation):
    """ Request verification """

    class Arguments(object):
        finding_id = String(required=True)
        justification = String(required=True)
    success = Boolean()

    @require_login
    @require_role(['customer', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, **parameters):
        user_email = util.get_jwt_content(info.context)['user_email']
        success = request_verification(
            finding_id=parameters.get('finding_id'),
            user_email=user_email,
            user_fullname=str.join(' ',
                                   [info.context.session['first_name'],
                                    info.context.session['last_name']]),
            justification=parameters.get('justification')
        )

        ret = RequestVerification(success=success)
        util.invalidate_cache(parameters.get('finding_id'))
        return ret


class UpdateDescription(Mutation):
    """ Update description of a finding """

    class Arguments(object):
        actor = String(required=True)
        affected_systems = String(required=True)
        attack_vector = String(required=True)
        category = String()
        cwe = String(required=True)
        description = String(required=True)
        finding_id = String(required=True)
        probability = String()
        recommendation = String(required=True)
        records = String()
        records_number = Int(required=True)
        report_level = String(required=True)
        requirements = String(required=True)
        risk_value = Float()
        severity = Int()
        scenario = String(required=True)
        threat = String(required=True)
        title = String(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['analyst', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, finding_id, **parameters):
        success = update_description(finding_id, parameters)

        ret = \
            UpdateDescription(success=success,
                              finding=Finding(info=info, identifier=finding_id))
        project_name = get_project_name(finding_id)
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        return ret


class UpdateTreatment(Mutation):
    """ Update treatment of a finding """

    class Arguments(object):
        bts_url = String()
        finding_id = String(required=True)
        treatment = String(required=True)
        treatment_justification = String(required=True)
    success = Boolean()
    finding = Field(Finding)

    @require_login
    @require_role(['customer', 'admin'])
    @require_finding_access_gql
    def mutate(self, info, finding_id, **parameters):
        user_email = util.get_jwt_content(info.context)['user_email']
        success = update_treatment(finding_id, parameters, user_email)

        ret = UpdateTreatment(success=success, finding=Finding(info=info, identifier=finding_id))
        project_name = get_project_name(finding_id)
        util.invalidate_cache(finding_id)
        util.invalidate_cache(project_name)
        return ret
