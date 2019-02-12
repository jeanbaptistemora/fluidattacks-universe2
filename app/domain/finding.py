# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import, division
import io
import re
import os
import sys
import threading
from datetime import datetime
from time import time
from decimal import Decimal

import boto3
import rollbar
from backports import csv
from botocore.exceptions import ClientError
from graphql import GraphQLError

from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from app import util
from app.utils import forms as forms_utils
from app.api.drive import DriveAPI
from app.api.formstack import FormstackAPI
from app.dao import integrates_dao
from app.dto.finding import (
    FindingDTO, get_project_name, calc_cvss_basescore,
    calc_cvss_enviroment, calc_cvss_temporal
)
from app.mailer import (
    send_mail_new_comment, send_mail_reply_comment, send_mail_verified_finding,
    send_mail_remediate_finding, send_mail_accepted_finding
)
from .vulnerability import update_vulnerabilities_date

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

BUCKET_S3 = FI_AWS_S3_BUCKET


def save_file_url(finding_id, field_name, file_url):
    return add_file_attribute(finding_id, field_name, 'file_url', file_url)


# pylint: disable=too-many-arguments
def send_file_to_s3(filename, parameters, field, fieldname, ext, fileurl):
    fileroute = '/tmp/:id.tmp'.replace(':id', filename)
    namecomplete = fileurl + '-' + field + '-' + filename + ext
    with open(fileroute, 'r') as file_obj:
        try:
            CLIENT_S3.upload_fileobj(file_obj, BUCKET_S3, namecomplete)
        except ClientError:
            rollbar.report_exc_info()
            return False
    file_name = namecomplete.split('/')[2]
    is_file_saved = save_file_url(parameters['finding_id'], fieldname, file_name)
    os.unlink(fileroute)
    return is_file_saved


def update_file_to_s3(parameters, field, fieldname, upload, fileurl):
    key_val = fileurl + '-' + field
    key_list = util.list_s3_objects(CLIENT_S3, BUCKET_S3, key_val)
    if key_list:
        for k in key_list:
            CLIENT_S3.delete_object(Bucket=BUCKET_S3, Key=k)
    file_name_complete = fileurl + '-' + field + '-' + upload.name
    try:
        CLIENT_S3.upload_fileobj(upload.file, BUCKET_S3, file_name_complete)
        file_name = file_name_complete.split('/')[2]
        save_file_url(parameters['finding_id'], fieldname, file_name)
        return True
    except ClientError:
        rollbar.report_exc_info()
        return False


def add_file_attribute(finding_id, file_name, file_attr, file_attr_value):
    attr_name = 'files'
    files = integrates_dao.get_finding_attributes_dynamo(finding_id, [attr_name])
    index = 0
    response = False
    primary_keys = ['finding_id', finding_id]
    if files and files.get(attr_name):
        for file_obj in files.get(attr_name):
            if file_obj.get('name') == file_name:
                response = integrates_dao.update_item_list_dynamo(
                    primary_keys, attr_name, index, file_attr, file_attr_value)
                break
            else:
                response = False
            index += 1
    else:
        response = False
    if response:
        is_url_saved = True
    else:
        file_data = []
        file_data.append({'name': file_name, file_attr: file_attr_value})
        is_url_saved = integrates_dao.add_list_resource_dynamo(
            'FI_findings',
            'finding_id',
            finding_id,
            file_data,
            attr_name)
    return is_url_saved


def migrate_all_files(parameters, file_url, request):
    fin_dto = FindingDTO()
    try:
        api = FormstackAPI()
        frmreq = api.get_submission(parameters['finding_id'])
        finding = fin_dto.parse(parameters['finding_id'], frmreq)
        files = [
            {'id': '0', 'name': 'animation', 'field': fin_dto.ANIMATION, 'ext': '.gif'},
            {'id': '1', 'name': 'exploitation', 'field': fin_dto.EXPLOTATION, 'ext': '.png'},
            {'id': '2', 'name': 'evidence_route_1', 'field': fin_dto.DOC_ACHV1, 'ext': '.png'},
            {'id': '3', 'name': 'evidence_route_2', 'field': fin_dto.DOC_ACHV2, 'ext': '.png'},
            {'id': '4', 'name': 'evidence_route_3', 'field': fin_dto.DOC_ACHV3, 'ext': '.png'},
            {'id': '5', 'name': 'evidence_route_4', 'field': fin_dto.DOC_ACHV4, 'ext': '.png'},
            {'id': '6', 'name': 'evidence_route_5', 'field': fin_dto.DOC_ACHV5, 'ext': '.png'},
            {'id': '7', 'name': 'exploit', 'field': fin_dto.EXPLOIT, 'ext': '.py'},
            {'id': '8', 'name': 'fileRecords', 'field': fin_dto.REG_FILE, 'ext': '.csv'}
        ]
        for file_obj in files:
            filename = '{file_url}-{field}'.format(file_url=file_url, field=file_obj['field'])
            folder = util.list_s3_objects(CLIENT_S3, BUCKET_S3, filename)
            if finding.get(file_obj['name']) and \
                    parameters.get('id') != file_obj['id'] and not folder:
                file_id = finding[file_obj['name']]
                fileroute = '/tmp/:id.tmp'.replace(':id', file_id)
                if os.path.exists(fileroute):
                    send_file_to_s3(finding[file_obj['name']], parameters,
                                    file_obj['field'], file_obj['name'],
                                    file_obj['ext'], file_url)
                else:
                    drive_api = DriveAPI()
                    file_download_route = drive_api.download(file_id)
                    if file_download_route:
                        send_file_to_s3(finding[file_obj['name']], parameters,
                                        file_obj['field'], file_obj['name'],
                                        file_obj['ext'], file_url)
                    else:
                        rollbar.report_message(
                            'Error: An error occurred downloading file from Drive',
                            'error',
                            request)
    except KeyError:
        rollbar.report_exc_info(sys.exc_info(), request)


def remove_repeated(vulnerabilities):
    """Remove vulnerabilities that changes in the same day."""
    vuln_casted = []
    for vuln in vulnerabilities:
        for state in vuln.historic_state:
            vuln_without_repeated = {}
            format_date = state.get('date').split(' ')[0]
            vuln_without_repeated[format_date] = {vuln.id: state.get('state')}
            vuln_casted.append(vuln_without_repeated)
    return vuln_casted


def get_unique_dict(list_dict):
    """Get unique dict."""
    unique_dict = {}
    for entry in list_dict:
        date = next(iter(entry))
        if not unique_dict.get(date):
            unique_dict[date] = {}
        vuln = next(iter(entry[date]))
        unique_dict[date][vuln] = entry[date][vuln]
    return unique_dict


def get_tracking_dict(unique_dict):
    """Get tracking dictionary."""
    sorted_dates = sorted(unique_dict.keys())
    tracking_dict = {}
    tracking_dict[sorted_dates[0]] = unique_dict[sorted_dates[0]]
    for date in range(1, len(sorted_dates)):
        prev_date = sorted_dates[date - 1]
        tracking_dict[sorted_dates[date]] = tracking_dict[prev_date].copy()
        actual_date_dict = unique_dict[sorted_dates[date]].items()
        for vuln, state in actual_date_dict:
            tracking_dict[sorted_dates[date]][vuln] = state
    return tracking_dict


def group_by_state(tracking_dict):
    """Group vulnerabilities by state."""
    tracking = {}
    for tracking_date, status in tracking_dict.items():
        for vuln_state in status.values():
            status_dict = \
                tracking.setdefault(tracking_date, {'open': 0, 'closed': 0})
            status_dict[vuln_state] += 1
    return tracking


def cast_tracking(tracking):
    """Cast tracking in accordance to schema."""
    cycle = 0
    tracking_casted = []
    for date, value in tracking:
        effectiveness = \
            int(round((value['closed'] / float((value['open'] +
                       value['closed']))) * 100))
        closing_cicle = {
            'cycle': cycle,
            'open': value['open'],
            'closed': value['closed'],
            'effectiveness': effectiveness,
            'date': date,
        }
        cycle += 1
        tracking_casted.append(closing_cicle)
    return tracking_casted


def get_dynamo_evidence(finding_id):
    finding_data = integrates_dao.get_data_dynamo('FI_findings',
                                                  'finding_id', finding_id)
    evidence_files = finding_data[0].get('files') \
        if finding_data and 'files' in finding_data[0].keys() else []
    parsed_evidence = {
        'animation': {'url':
                      filter_evidence_filename(evidence_files,
                                               'animation')},
        'evidence1': {'url':
                      filter_evidence_filename(evidence_files,
                                               'evidence_route_1')},
        'evidence2': {'url':
                      filter_evidence_filename(evidence_files,
                                               'evidence_route_2')},
        'evidence3': {'url':
                      filter_evidence_filename(evidence_files,
                                               'evidence_route_3')},
        'evidence4': {'url':
                      filter_evidence_filename(evidence_files,
                                               'evidence_route_4')},
        'evidence5': {'url':
                      filter_evidence_filename(evidence_files,
                                               'evidence_route_5')},
        'exploitation': {'url':
                         filter_evidence_filename(evidence_files,
                                                  'exploitation')},
    }

    return parsed_evidence


def filter_evidence_filename(evidence_files, name):
    evidence_info = filter(lambda evidence: evidence['name'] == name,
                           evidence_files)
    return evidence_info[0]['file_url'] if evidence_info else ''


def migrate_evidence_description(finding):
    """Migrate evidence description to dynamo."""
    finding_id = finding['id']
    description_fields = {
        'evidence_description_1': 'evidence_route_1',
        'evidence_description_2': 'evidence_route_2',
        'evidence_description_3': 'evidence_route_3',
        'evidence_description_4': 'evidence_route_4',
        'evidence_description_5': 'evidence_route_5'}
    description = {k: finding.get(k)
                   for (k, v) in description_fields.items()
                   if finding.get(k)}
    response = [add_file_attribute(finding_id, description_fields[k],
                                   'description', v)
                for (k, v) in description.items()]
    return all(response)


def list_comments(user_email, comment_type, finding_id):
    comments = list(map(lambda comment: {
        'content': comment['content'],
        'created': comment['created'],
        'created_by_current_user': comment['email'] == user_email,
        'email': comment['email'],
        'fullname': comment['fullname'],
        'id': int(comment['user_id']),
        'modified': comment['modified'],
        'parent': int(comment['parent'])
    }, integrates_dao.get_comments_dynamo(int(finding_id), comment_type)))

    return comments


def comment_has_parent(parent):
    return parent != '0'


def get_email_recipients(project_name, comment_type):
    project_users = integrates_dao.get_project_users(project_name)
    recipients = []

    if comment_type == 'observation':
        admins = [user[0] for user in integrates_dao.get_admins()]
        analysts = [user[0] for user in project_users
                    if integrates_dao.get_role_dao(user[0]) == 'analyst']

        recipients += admins
        recipients += analysts
    else:
        recipients = [user[0] for user in project_users if user[1] == 1]

    return recipients


def send_comment_mail(user_email, content, parent, comment_type, finding_id):
    project_name = get_project_name(finding_id).lower()
    recipients = get_email_recipients(project_name, comment_type)

    if comment_has_parent(parent):
        mail_title = \
            "New {comment_type!s} email thread".format(comment_type=comment_type)
        mail_function = send_mail_new_comment
    else:
        mail_title = \
            "Reply {comment_type!s} email thread".format(comment_type=comment_type)
        mail_function = send_mail_reply_comment

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    dynamo_value = integrates_dao.get_finding_attributes_dynamo(
        finding_id, ['finding'])
    if dynamo_value:
        finding_title = dynamo_value.get('finding')
    else:
        fin_dto = FindingDTO()
        api = FormstackAPI()
        finding_title = fin_dto.parse(
            finding_id, api.get_submission(finding_id)
        ).get('finding')

    email_send_thread = threading.Thread(
        name=mail_title,
        target=mail_function,
        args=(recipients, {
            'project': project_name,
            'finding_name': finding_title,
            'user_email': user_email,
            'finding_id': finding_id,
            'comment': content.replace('\n', ' '),
            'finding_url':
                base_url + '/project/{project!s}/{finding!s}/{comment_type!s}s'
            .format(project=project_name, finding=finding_id,
                    comment_type=comment_type)
        }, comment_type))
    email_send_thread.start()


def add_comment(user_email, user_fullname, parent, content,
                comment_type, comment_id, finding_id, is_remediation_comment):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_data = {
        'user_id': comment_id,
        'comment_type': comment_type,
        'content': content,
        'created': current_time,
        'fullname': user_fullname,
        'modified': current_time,
        'parent': int(parent)
    }

    if not is_remediation_comment:
        send_comment_mail(user_email, content, parent,
                          comment_type, finding_id)

    return integrates_dao.add_finding_comment_dynamo(int(finding_id),
                                                     user_email, comment_data)


def send_finding_verified_email(company, finding_id,
                                finding_name, project_name):
    project_users = integrates_dao.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
    recipients.append('continuous@fluidattacks.com')
    recipients.append('projects@fluidattacks.com')

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_send_thread = threading.Thread(
        name='Verified finding email thread',
        target=send_mail_verified_finding,
        args=(recipients, {
            'project': project_name,
            'finding_name': finding_name,
            'finding_url':
                base_url + '/project/{project!s}/{finding!s}/tracking'
            .format(project=project_name, finding=finding_id),
            'finding_id': finding_id,
            'company': company,
        }))

    email_send_thread.start()


def verify_finding(company, finding_id, user_email):
    project_name = get_project_name(finding_id).lower()
    finding_name = \
        integrates_dao.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')
    success = \
        integrates_dao.add_remediated_dynamo(int(finding_id), False,
                                             project_name, finding_name)
    if success:
        update_vulnerabilities_date(user_email, finding_id)
        send_finding_verified_email(company, finding_id,
                                    finding_name, project_name)
    else:
        rollbar.report_message(
            'Error: An error occurred verifying the finding', 'error')

    return success


def send_remediation_email(user_email, finding_id, finding_name,
                           project_name, justification):
    project_users = integrates_dao.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
    recipients.append('continuous@fluidattacks.com')
    recipients.append('projects@fluidattacks.com')

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_send_thread = threading.Thread(
        name='Remediate finding email thread',
        target=send_mail_remediate_finding,
        args=(recipients, {
            'project': project_name,
            'finding_name': finding_name,
            'finding_url':
                base_url + '/project/{project!s}/{finding!s}/description'
            .format(project=project_name, finding=finding_id),
            'finding_id': finding_id,
            'user_mail': user_email,
            'solution': justification
        }))

    email_send_thread.start()


def request_verification(finding_id, user_email, user_fullname, justification):
    project_name = get_project_name(finding_id).lower()
    finding_name = \
        integrates_dao.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')
    success = integrates_dao.add_remediated_dynamo(int(finding_id), True,
                                                   project_name, finding_name)
    if success:
        add_comment(
            user_email=user_email,
            parent='0',
            content=justification,
            comment_type='comment',
            comment_id=int(round(time() * 1000)),
            finding_id=finding_id,
            user_fullname=user_fullname,
            is_remediation_comment=True
        )
        send_remediation_email(user_email, finding_id, finding_name,
                               project_name, justification)
    else:
        rollbar.report_message(
            'Error: An error occurred remediating the finding', 'error')

    return success


def calc_risk_level(probability, severity):
    probability_value = int(probability[:3].replace('%', ''))
    return str(round((probability_value / 100) * severity, 1))


def update_description(finding_id, updated_values):
    updated_values['finding'] = updated_values.get('title')
    updated_values['vulnerability'] = updated_values.get('description')
    updated_values['effect_solution'] = updated_values.get('recommendation')
    updated_values['kb'] = updated_values.get('kb_url')
    updated_values['records_number'] = str(updated_values.get('records_number'))
    updated_values['id'] = finding_id
    del updated_values['title']
    del updated_values['description']
    del updated_values['recommendation']
    del updated_values['kb_url']

    if updated_values.get('probability') and updated_values.get('severity'):
        if updated_values['severity'] < 0 or updated_values['severity'] > 5:
            raise GraphQLError('Invalid severity')
        else:
            updated_values['risk_value'] = calc_risk_level(
                updated_values['probability'],
                updated_values['severity'])

    description = integrates_dao.get_finding_attributes_dynamo(
        finding_id,
        ['vulnerability'])

    if not description:
        finding_dto = FindingDTO()
        api = FormstackAPI()
        submission_data = api.get_submission(finding_id)
        description_info = \
            finding_dto.parse_description(submission_data, finding_id)
        project_info = \
            finding_dto.parse_project(submission_data, finding_id)
        aditional_info = \
            forms_utils.dict_concatenation(description_info,
                                           project_info)
        updated_values = \
            forms_utils.dict_concatenation(aditional_info, updated_values)
    else:
        # Finding data has been already migrated
        pass

    updated_values = {util.camelcase_to_snakecase(k): updated_values.get(k)
                      for k in updated_values}
    return integrates_dao.update_mult_attrs_dynamo(
        'FI_findings',
        ['finding_id', finding_id],
        updated_values
    )


def send_accepted_email(finding_id, user_email, justification):
    project_name = get_project_name(finding_id).lower()
    project_users = integrates_dao.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
    finding_name = \
        integrates_dao.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')

    email_send_thread = threading.Thread(
        name='Accepted finding email thread',
        target=send_mail_accepted_finding,
        args=(recipients, {
            'user_mail': user_email,
            'finding_name': finding_name,
            'finding_id': finding_id,
            'project_name': project_name.capitalize(),
            'justification': justification,
        }))

    email_send_thread.start()


def update_treatment(finding_id, updated_values, user_email):
    updated_values['external_bts'] = updated_values.get('bts_url')
    del updated_values['bts_url']

    if updated_values['treatment'] == 'Asumido':
        send_accepted_email(finding_id, user_email,
                            updated_values.get('treatment_justification'))

    return integrates_dao.update_mult_attrs_dynamo(
        'FI_findings',
        ['finding_id', finding_id],
        updated_values
    )


def save_severity(finding):
    """Organize severity metrics to save in dynamo."""
    fin_dto = FindingDTO()
    primary_keys = ['finding_id', str(finding['id'])]
    severity_fields = ['accessVector', 'accessComplexity',
                       'authentication', 'exploitability',
                       'confidentialityImpact', 'integrityImpact',
                       'availabilityImpact', 'resolutionLevel',
                       'confidenceLevel', 'collateralDamagePotential',
                       'findingDistribution', 'confidentialityRequirement',
                       'integrityRequirement', 'availabilityRequirement']
    severity = {util.camelcase_to_snakecase(k): Decimal(str(finding.get(k)))
                for k in severity_fields}
    unformatted_severity = {k: float(str(finding.get(k))) for k in severity_fields}
    severity['cvss_basescore'] = calc_cvss_basescore(unformatted_severity,
                                                     fin_dto.CVSS_PARAMETERS)
    severity['cvss_temporal'] = calc_cvss_temporal(unformatted_severity,
                                                   severity['cvss_basescore'])
    severity['cvss_env'] = calc_cvss_enviroment(unformatted_severity,
                                                fin_dto.CVSS_PARAMETERS)
    response = \
        integrates_dao.add_multiple_attributes_dynamo('FI_findings',
                                                      primary_keys, severity)
    return response


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
