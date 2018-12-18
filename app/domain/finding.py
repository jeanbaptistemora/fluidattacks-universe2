# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

from __future__ import absolute_import
import os
import sys

import boto3
import rollbar
from botocore.exceptions import ClientError

from __init__ import FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET
from app import util
from app.api.drive import DriveAPI
from app.api.formstack import FormstackAPI
from app.dao import integrates_dao
from app.dto.finding import FindingDTO

client_s3 = boto3.client('s3',
                            aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                            aws_secret_access_key=FI_AWS_S3_SECRET_KEY)

bucket_s3 = FI_AWS_S3_BUCKET

def save_file_url(finding_id, field_name, file_url):
    return add_file_attribute(finding_id, field_name, 'file_url', file_url)

#pylint: disable-msg=R0913
def send_file_to_s3(filename, parameters, field, fieldname, ext, fileurl):
    fileroute = '/tmp/:id.tmp'.replace(':id', filename)
    namecomplete = fileurl + '-' + field + '-' + filename + ext
    with open(fileroute, 'r') as file_obj:
        try:
            client_s3.upload_fileobj(file_obj, bucket_s3, namecomplete)
        except ClientError:
            rollbar.report_exc_info()
            return False
    file_name = namecomplete.split('/')[2]
    is_file_saved = save_file_url(parameters['finding_id'], fieldname, file_name)
    os.unlink(fileroute)
    return is_file_saved

def update_file_to_s3(parameters, field, fieldname, upload, fileurl):
    key_val = fileurl + '-' + field
    key_list = util.list_s3_objects(client_s3, bucket_s3, key_val)
    if key_list:
        for k in key_list:
            client_s3.delete_object(Bucket=bucket_s3, Key=k)
    file_name_complete = fileurl + '-' + field + '-' + upload.name
    try:
        client_s3.upload_fileobj(upload.file, bucket_s3, file_name_complete)
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
            folder = util.list_s3_objects(client_s3, bucket_s3, filename)
            if finding.get(file_obj['name']) and parameters.get('id') != file_obj['id'] and not folder:
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
        vuln_without_repeated = {}
        for state in vuln.historic_state:
            format_date = state.get('date').split(' ')[0]
            vuln_without_repeated[format_date] = state.get('state')
        vuln_casted.append(vuln_without_repeated)
    return vuln_casted


def group_by_state(vulnerabilities):
    """Group vulnerabilities by state."""
    tracking = {}
    for vuln in vulnerabilities:
        for date, status in vuln.items():
            status_dict = tracking.setdefault(date, {'open': 0, 'closed': 0})
            status_dict[status] += 1
    return tracking


def cast_tracking(tracking):
    """Cast tracking in accordance to schema."""
    cycle = 0
    tracking_casted = []
    for date, value in tracking:
        effectiveness = int(round((value['closed'] / float((value['open'] + value['closed']))) * 100))
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
    finding_data = integrates_dao.get_data_dynamo('FI_findings', 'finding_id', finding_id)
    evidence_files = finding_data[0].get('files') if finding_data and 'files' in finding_data[0].keys() else []
    parsed_evidence = {
        'animation': { 'url': filter_evidence_filename(evidence_files, 'animation') },
        'evidence1': { 'url': filter_evidence_filename(evidence_files, 'evidence_route_1') },
        'evidence2': { 'url': filter_evidence_filename(evidence_files, 'evidence_route_2') },
        'evidence3': { 'url': filter_evidence_filename(evidence_files, 'evidence_route_3') },
        'evidence4': { 'url': filter_evidence_filename(evidence_files, 'evidence_route_4') },
        'evidence5': { 'url': filter_evidence_filename(evidence_files, 'evidence_route_5') },
        'exploitation': { 'url': filter_evidence_filename(evidence_files, 'exploitation') },
    }

    return parsed_evidence

def filter_evidence_filename(evidence_files, name):
    evidence_info = filter(lambda evidence: evidence['name'] == name, evidence_files)
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
                   for (k, v) in description_fields.items() if finding.get(k)}
    response = [add_file_attribute(finding_id, description_fields[k], 'description', v)
                for (k, v) in description.items()]
    return all(response)
