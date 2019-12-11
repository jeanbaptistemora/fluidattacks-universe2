import io
import re
import random
import threading
from datetime import datetime
from decimal import Decimal
from time import time

import pytz
import rollbar
from django.conf import settings
from django.core.files.base import ContentFile
from graphql import GraphQLError
from i18n import t

from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_MAIL_REVIEWERS, FI_MAIL_REPLYERS
)
from app import util
from app.dal import integrates_dal, finding as finding_dal
from app.domain import (
    project as project_domain, user as user_domain,
    vulnerability as vuln_domain
)
from app.exceptions import (
    AlreadyApproved, AlreadySubmitted, FindingNotFound, IncompleteDraft,
    NotSubmitted, InvalidFileSize, InvalidDraftTitle
)
from app.mailer import (
    send_mail_comment, send_mail_verified_finding, send_mail_remediate_finding,
    send_mail_accepted_finding, send_mail_reject_draft,
    send_mail_delete_finding, send_mail_new_draft
)
from app.utils import cvss, notifications, findings as finding_utils


def save_file_url(finding_id, field_name, file_url):
    return add_file_attribute(finding_id, field_name, 'file_url', file_url)


def add_file_attribute(finding_id, file_name, file_attr, file_attr_value):
    attr_name = 'files'
    files = integrates_dal.get_finding_attributes_dynamo(finding_id, [attr_name])
    index = 0
    response = False
    primary_keys = ['finding_id', finding_id]
    if files and files.get(attr_name):
        for file_obj in files.get(attr_name):
            if file_obj.get('name') == file_name:
                response = integrates_dal.update_item_list_dynamo(
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
        is_url_saved = integrates_dal.add_list_resource_dynamo(
            'FI_findings',
            'finding_id',
            finding_id,
            file_data,
            attr_name)
    return is_url_saved


def remove_repeated(vulnerabilities):
    """Remove vulnerabilities that changes in the same day."""
    vuln_casted = []
    for vuln in vulnerabilities:
        for state in vuln['historic_state']:
            vuln_without_repeated = {}
            format_date = state.get('date').split(' ')[0]
            vuln_without_repeated[format_date] = {vuln['UUID']: state.get('state')}
            if state.get('approval_status') != 'PENDING':
                vuln_casted.append(vuln_without_repeated)
            else:
                # don't append pending's state to tracking
                pass
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
    if sorted_dates:
        tracking_dict[sorted_dates[0]] = unique_dict[sorted_dates[0]]
        for date in range(1, len(sorted_dates)):
            prev_date = sorted_dates[date - 1]
            tracking_dict[sorted_dates[date]] = tracking_dict[prev_date].copy()
            actual_date_dict = list(unique_dict[sorted_dates[date]].items())
            for vuln, state in actual_date_dict:
                tracking_dict[sorted_dates[date]][vuln] = state
    return tracking_dict


def group_by_state(tracking_dict):
    """Group vulnerabilities by state."""
    tracking = {}
    for tracking_date, status in list(tracking_dict.items()):
        for vuln_state in list(status.values()):
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


def filter_evidence_filename(evidence_files, name):
    evidence_info = [evidence for evidence in evidence_files
                     if evidence['name'] == name]
    return evidence_info[0].get('file_url', '') if evidence_info else ''


def get_email_recipients(project_name, comment_type):
    project_users = project_domain.get_users(project_name)
    recipients = []

    if comment_type == 'observation':
        approvers = FI_MAIL_REVIEWERS.split(',')
        analysts = [user for user in project_users
                    if user_domain.get_data(user, 'role') == 'analyst']

        recipients += approvers
        recipients += analysts
    else:
        recipients = project_users
        replyers = FI_MAIL_REPLYERS.split(',')
        recipients += replyers

    return recipients


def send_comment_mail(user_email, comment_data, finding_id):
    comment_type = comment_data['comment_type']
    finding = get_finding(finding_id)
    recipients = get_email_recipients(finding.get('projectName'), comment_type)

    is_draft = 'releaseDate' in finding
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_context = {
        'project': finding.get('projectName'),
        'finding_name': finding.get('finding'),
        'user_email': user_email,
        'finding_id': finding_id,
        'comment': comment_data['content'].replace('\n', ' '),
        'comment_type': comment_type,
        'parent': comment_data['parent'],
        'comment_url':
            base_url
            + '/project/{project}/{finding_type}/{id}/{comment_type}s'.format(
            comment_type=comment_type,
            finding_type='findings' if is_draft else 'drafts',
            id=finding_id,
            project=finding.get('projectName'))
    }

    email_send_thread = threading.Thread(
        name='New {} email thread'.format(comment_type),
        target=send_mail_comment,
        args=(recipients, email_context))
    email_send_thread.start()


def add_comment(user_email, comment_data, finding_id, is_remediation_comment):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_data['created'] = current_time
    comment_data['modified'] = current_time

    if not is_remediation_comment:
        send_comment_mail(user_email, comment_data, finding_id)

    return integrates_dal.add_finding_comment_dynamo(int(finding_id),
                                                     user_email, comment_data)


def send_finding_verified_email(finding_id, finding_name, project_name):
    recipients = project_domain.get_users(project_name)

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
            'finding_id': finding_id
        }))

    email_send_thread.start()


def get_age_finding(act_finding):
    """Get days since the vulnerabilities was release"""
    today = datetime.now()
    release_date = act_finding['releaseDate'].split(' ')
    age = abs(datetime.strptime(release_date[0], '%Y-%m-%d') - today).days
    return age


def get_tracking_vulnerabilities(vulnerabilities):
    """get tracking vulnerabilities dictionary"""
    tracking = []
    vulns_filtered = [vuln for vuln in vulnerabilities
                      if vuln['historic_state'][-1].get('approval_status')
                      != 'PENDING' or vuln_domain.get_last_approved_status(
                          vuln)]

    vulns_filtered = [vuln for vuln in vulns_filtered
                      if vuln_domain.get_last_approved_status(
                          vuln) != 'DELETED']
    vuln_casted = remove_repeated(vulns_filtered)
    unique_dict = get_unique_dict(vuln_casted)
    tracking = get_tracking_dict(unique_dict)
    tracking_grouped = group_by_state(tracking)
    order_tracking = sorted(tracking_grouped.items())
    tracking_casted = cast_tracking(order_tracking)
    tracking = tracking_casted
    return tracking


def verify_finding(finding_id, user_email):
    finding = get_finding(finding_id)
    project_name = finding.get('projectName')
    finding_name = finding.get('finding')
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    success = finding_dal.update(finding_id, {'verification_date': today})

    if success:
        vuln_domain.update_vulnerabilities_date(user_email, finding_id)
        send_finding_verified_email(finding_id, finding_name, project_name)
        project_users = project_domain.get_users(project_name)
        notifications.notify_mobile(
            project_users,
            t('notifications.verified.title'),
            t('notifications.verified.content',
                finding=finding_name, project=project_name.upper()))
    else:
        rollbar.report_message(
            'Error: An error occurred verifying the finding', 'error')

    return success


def send_remediation_email(user_email, finding_id, finding_name,
                           project_name, justification):
    recipients = project_domain.get_users(project_name)

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_send_thread = threading.Thread(
        name='Remediate finding email thread',
        target=send_mail_remediate_finding,
        args=(recipients, {
            'project': project_name.lower(),
            'finding_name': finding_name,
            'finding_url':
                base_url + '/project/{project!s}/{finding!s}/description'
            .format(project=project_name, finding=finding_id),
            'finding_id': finding_id,
            'user_email': user_email,
            'solution_description': justification
        }))

    email_send_thread.start()


def request_verification(finding_id, user_email, user_fullname, justification):
    finding = get_finding(finding_id)
    project_name = finding.get('projectName')
    finding_name = finding.get('finding')
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    success = finding_dal.update(finding_id, {
        'verification_request_date': today})
    if success:
        comment_data = {
            'user_id': int(round(time() * 1000)),
            'comment_type': 'verification',
            'content': justification,
            'fullname': user_fullname,
            'parent': 0
        }
        add_comment(
            user_email=user_email,
            comment_data=comment_data,
            finding_id=finding_id,
            is_remediation_comment=True
        )
        send_remediation_email(user_email, finding_id, finding_name,
                               project_name, justification)
        project_users = project_domain.get_users(project_name)
        notifications.notify_mobile(
            project_users,
            t('notifications.remediated.title'),
            t('notifications.remediated.content',
                finding=finding_name, project=project_name.upper()))
    else:
        rollbar.report_message(
            'Error: An error occurred remediating the finding', 'error')

    return success


def calc_risk_level(probability, severity):
    return str(round((probability / 100) * severity, 1))


def update_description(finding_id, updated_values):
    updated_values['finding'] = updated_values.get('title')
    updated_values['vulnerability'] = updated_values.get('description')
    updated_values['effect_solution'] = updated_values.get('recommendation')
    updated_values['records_number'] = str(updated_values.get('records_number'))
    updated_values['id'] = finding_id
    del updated_values['title']
    del updated_values['description']
    del updated_values['recommendation']

    updated_values = {util.camelcase_to_snakecase(k): updated_values.get(k)
                      for k in updated_values}

    if re.search(r'^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+', updated_values['finding']):

        return integrates_dal.update_mult_attrs_dynamo(
            'FI_findings',
            {'finding_id': finding_id},
            updated_values
        )
    raise InvalidDraftTitle()


def send_accepted_email(finding_id, justification):
    finding = get_finding(finding_id)
    project_name = finding.get('projectName')
    finding_name = finding.get('finding')
    recipients = project_domain.get_users(project_name)

    email_send_thread = threading.Thread(
        name='Accepted finding email thread',
        target=send_mail_accepted_finding,
        args=(recipients, {
            'finding_name': finding_name,
            'finding_id': finding_id,
            'project': project_name.capitalize(),
            'justification': justification,
        }))

    email_send_thread.start()


def update_treatment_in_vuln(finding_id, updated_values):
    vulns = integrates_dal.get_vulnerabilities_dynamo(finding_id)
    for vuln in vulns:
        result_update_treatment = \
            integrates_dal.update_mult_attrs_dynamo('FI_vulnerabilities',
                                                    {'finding_id': finding_id,
                                                     'UUID': vuln['UUID']},
                                                    updated_values)
        if not result_update_treatment:
            return False
    return True


def update_treatment(finding_id, updated_values):
    valid_update_values = util.update_treatment_values(updated_values)
    return validate_update_treatment(finding_id, valid_update_values)


def validate_update_treatment(finding_id, updated_values):
    result_update_finding = integrates_dal.update_mult_attrs_dynamo(
        'FI_findings',
        {'finding_id': finding_id},
        updated_values
    )
    result_update_vuln = update_treatment_in_vuln(finding_id, updated_values)
    if result_update_finding and result_update_vuln:
        if updated_values['treatment'] == 'ACCEPTED':
            send_accepted_email(finding_id, updated_values.get('treatment_justification'))
        return True
    return False


def save_severity(finding):
    """Organize severity metrics to save in dynamo."""
    primary_keys = ['finding_id', str(finding['id'])]
    cvss_version = finding.get('cvssVersion', '')
    cvss_parameters = finding_utils.CVSS_PARAMETERS[cvss_version]
    if cvss_version == '3':
        severity_fields = ['attackVector', 'attackComplexity',
                           'privilegesRequired', 'userInteraction',
                           'severityScope', 'confidentialityImpact',
                           'integrityImpact', 'availabilityImpact',
                           'exploitability', 'remediationLevel',
                           'reportConfidence', 'confidentialityRequirement',
                           'integrityRequirement', 'availabilityRequirement',
                           'modifiedAttackVector', 'modifiedAttackComplexity',
                           'modifiedPrivilegesRequired', 'modifiedUserInteraction',
                           'modifiedSeverityScope', 'modifiedConfidentialityImpact',
                           'modifiedIntegrityImpact', 'modifiedAvailabilityImpact']
        severity = {util.camelcase_to_snakecase(k): Decimal(str(finding.get(k)))
                    for k in severity_fields}
        unformatted_severity = {k: float(str(finding.get(k))) for k in severity_fields}
        privileges = cvss.calculate_privileges(
            unformatted_severity['privilegesRequired'],
            unformatted_severity['severityScope'])
        unformatted_severity['privilegesRequired'] = privileges
        severity['privileges_required'] = \
            Decimal(privileges).quantize(Decimal('0.01'))
        modified_priviles = cvss.calculate_privileges(
            unformatted_severity['modifiedPrivilegesRequired'],
            unformatted_severity['modifiedSeverityScope'])
        unformatted_severity['modifiedPrivilegesRequired'] = modified_priviles
        severity['modified_privileges_required'] = \
            Decimal(modified_priviles).quantize(Decimal('0.01'))
    else:
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
    severity['cvss_basescore'] = cvss.calculate_cvss_basescore(
        unformatted_severity, cvss_parameters, cvss_version)
    severity['cvss_temporal'] = cvss.calculate_cvss_temporal(
        unformatted_severity, float(severity['cvss_basescore']), cvss_version)
    severity['cvss_env'] = cvss.calculate_cvss_environment(
        unformatted_severity, cvss_parameters, cvss_version)
    severity['cvss_version'] = cvss_version
    response = \
        integrates_dal.add_multiple_attributes_dynamo('FI_findings',
                                                      primary_keys, severity)
    return response


def delete_comment(comment):
    """Delete comment."""
    if comment:
        finding_id = comment['finding_id']
        user_id = comment['user_id']
        response = integrates_dal.delete_comment_dynamo(finding_id, user_id)
    else:
        response = True
    return response


def delete_all_comments(finding_id):
    """Delete all comments of a finding."""
    all_comments = integrates_dal.get_comments_dynamo(int(finding_id), 'comment')
    comments_deleted = [delete_comment(i) for i in all_comments]
    util.invalidate_cache(finding_id)
    return all(comments_deleted)


def delete_all_evidences_s3(finding_id, project, context):
    """Delete s3 evidences files."""
    evidences_list = finding_dal.search_evidence(project + '/' + finding_id)
    is_evidence_deleted = False
    if evidences_list:
        is_evidence_deleted_s3 = list(map(finding_dal.remove_evidence, evidences_list))
        is_evidence_deleted = any(is_evidence_deleted_s3)
    else:
        util.cloudwatch_log(
            context,
            'Info: Finding ' + finding_id + ' does not have evidences in s3')
        is_evidence_deleted = True
    return is_evidence_deleted


def send_draft_reject_mail(draft_id, project_name, discoverer_email, finding_name, reviewer_email):
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients.append(discoverer_email)

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_context = {
        'admin_mail': reviewer_email,
        'analyst_mail': discoverer_email,
        'draft_url': '{}/project/{}/drafts/{}/description'.format(
            base_url, project_name, draft_id),
        'finding_id': draft_id,
        'finding_name': finding_name,
        'project': project_name
    }
    email_send_thread = threading.Thread(
        name='Reject draft email thread',
        target=send_mail_reject_draft,
        args=(recipients, email_context))
    email_send_thread.start()


def reject_draft(draft_id, reviewer_email):
    draft_data = get_finding(draft_id)
    history = draft_data.get('historicState', [{}])
    status = history[-1].get('state')
    success = False

    if 'releaseDate' not in draft_data:
        if status == 'SUBMITTED':
            tzn = pytz.timezone(settings.TIME_ZONE)
            rejection_date = datetime.now(tz=tzn).today()
            rejection_date = rejection_date.strftime('%Y-%m-%d %H:%M:%S')
            history.append({
                'date': rejection_date,
                'analyst': reviewer_email,
                'state': 'REJECTED'
            })

            success = finding_dal.update(draft_id, {
                'release_date': None,
                'historic_state': history
            })
            if success:
                send_draft_reject_mail(
                    draft_id, draft_data['projectName'], draft_data['analyst'],
                    draft_data['finding'], reviewer_email)
        else:
            raise NotSubmitted()
    else:
        raise AlreadyApproved()

    return success


def send_finding_delete_mail(
    finding_id, finding_name, project_name, discoverer_email, justification
):
    recipients = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients.extend(approvers)

    email_send_thread = threading.Thread(
        name='Delete finding email thread',
        target=send_mail_delete_finding,
        args=(recipients, {
            'mail_analista': discoverer_email,
            'name_finding': finding_name,
            'id_finding': finding_id,
            'description': justification,
            'project': project_name,
        }))
    email_send_thread.start()


def filter_deleted_findings(findings_ids):
    return [finding_id for finding_id in findings_ids
            if validate_finding(finding_id)]


def delete_finding(finding_id, project_name, justification, context):
    finding_data = get_finding(finding_id)
    submission_history = finding_data.get('historicState', [{}])
    success = False

    if submission_history[-1].get('state') != 'DELETED':
        tzn = pytz.timezone(settings.TIME_ZONE)
        delete_date = datetime.now(tz=tzn).today()
        delete_date = delete_date.strftime('%Y-%m-%d %H:%M:%S')
        submission_history.append({
            'state': 'DELETED',
            'date': delete_date,
            'justification': justification,
            'analyst': util.get_jwt_content(context)['user_email'],
        })
        success = finding_dal.update(finding_id, {
            'historic_state': submission_history
        })

        if success:
            justification_dict = {
                'DUPLICATED': 'It is duplicated',
                'FALSE_POSITIVE': 'It is a false positive',
                'NOT_REQUIRED': 'Finding not required',
            }
            send_finding_delete_mail(
                finding_id, finding_data['finding'], project_name,
                finding_data['analyst'], justification_dict[justification])

    return success


def approve_draft(draft_id, reviewer_email):
    draft_data = get_finding(draft_id)
    submission_history = draft_data.get('historicState')
    release_date = None
    success = False

    if 'releaseDate' not in draft_data and \
       submission_history[-1].get('state') != 'DELETED':
        has_vulns = vuln_domain.list_vulnerabilities([draft_id])
        if has_vulns:
            if 'reportDate' in draft_data:
                tzn = pytz.timezone(settings.TIME_ZONE)
                release_date = datetime.now(tz=tzn).today()
                release_date = release_date.strftime('%Y-%m-%d %H:%M:%S')
                history = draft_data.get('historicState', [{}])
                history.append({
                    'date': release_date,
                    'analyst': reviewer_email,
                    'state': 'APPROVED'
                })

                success = finding_dal.update(draft_id, {
                    'lastVulnerability': release_date,
                    'releaseDate': release_date,
                    'treatment': 'NEW',
                    'historic_state': history
                })
            else:
                raise NotSubmitted()
        else:
            raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
    else:
        raise AlreadyApproved()
    return success, release_date


def get_finding(finding_id):
    """Retrieves and formats finding attributes"""
    finding = finding_dal.get_finding(finding_id)
    if not finding or not validate_finding(finding=finding):
        raise FindingNotFound()

    return finding_utils.format_data(finding)


def get_findings(finding_ids):
    """Retrieves all attributes for the requested findings"""
    findings = [get_finding(finding_id) for finding_id in finding_ids
                if validate_finding(finding_id=finding_id)]
    if not findings:
        raise FindingNotFound()
    return findings


def append_records_to_file(records, new_file):
    header = records[0].keys()
    values = [list(v) for v in [record.values() for record in records]]
    new_file_records = new_file.read()
    new_file_header = new_file_records.decode('utf-8').split('\n')[0]
    new_file_records = r'\n'.join(new_file_records.decode('utf-8').split('\n')[1:])
    records_str = ''
    for record in values:
        records_str += repr(str(','.join(record)) + '\n').replace('\'', '')
    aux = records_str
    records_str = str(','.join(header)) + r'\n' + aux + str(new_file_records).replace('\'', '')
    if new_file_header != str(','.join(header)):
        raise GraphQLError('Wrong file structure')

    buff = io.BytesIO(records_str.encode('utf-8').decode('unicode_escape').encode('utf-8'))
    content_file = ContentFile(buff.read())
    content_file.close()
    return content_file


def save_evidence(evidence_name, finding_id, project_name, uploaded_file):
    full_name = '{proj}/{fin}/{proj}-{fin}-{name}'.format(
        fin=finding_id,
        name=uploaded_file.name.replace(' ', '_').replace('-', '_'),
        proj=project_name)

    if evidence_name == 'fileRecords':
        old_file = integrates_dal.get_finding_attributes_dynamo(finding_id, ['files'])
        old_file_name = next((
            item['file_url'] for item in old_file['files'] if item['name'] == 'fileRecords'), '')
        if old_file_name != '':
            old_records = finding_utils.get_records_from_file(
                project_name, finding_id, old_file_name)
            if old_records:
                uploaded_file = append_records_to_file(old_records, uploaded_file)
                uploaded_file.open()
    success = finding_dal.save_evidence(uploaded_file, full_name)
    if success:
        file_name = full_name.split('/')[2]
        save_file_url(finding_id, evidence_name, file_name)
    return success


def remove_evidence(evidence_name, finding_id, project_name):
    if evidence_name == 'fileRecords':
        old_file = integrates_dal.get_finding_attributes_dynamo(finding_id, ['files'])
        old_file_name = next((
            item['file_url'] for item in old_file['files'] if item['name'] == 'fileRecords'), '')
        full_name = '{proj}/{fin}/{proj}-{fin}-{name}'.format(
            fin=finding_id,
            name=old_file_name.split('-')[-1],
            proj=project_name)
        success = finding_dal.save_evidence(ContentFile(b''), full_name)
        if success:
            file_name = old_file_name
            save_file_url(finding_id, evidence_name, file_name)
        return success
    return False


def create_draft(info, project_name, title, **kwargs):
    last_fs_id = 550000000
    finding_id = str(random.randint(last_fs_id, 1000000000))
    tzn = pytz.timezone(settings.TIME_ZONE)
    project_name = project_name.lower()
    creation_date = datetime.now(tz=tzn).today()
    creation_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
    user_data = util.get_jwt_content(info.context)
    analyst_email = user_data['user_email']
    submission_history = {'analyst': analyst_email,
                          'date': creation_date,
                          'state': 'CREATED'}
    if util.is_api_token(user_data):
        submission_history.update({
            'analyst': f'api-{analyst_email}',
            'origin': kwargs.get('origin', 'api')})

    if 'description' in kwargs:
        kwargs['vulnerability'] = kwargs['description']
        del kwargs['description']
    if 'recommendation' in kwargs:
        kwargs['effect_solution'] = kwargs['recommendation']
        del kwargs['recommendation']
    if 'type' in kwargs:
        kwargs['finding_type'] = kwargs['type']
        del kwargs['type']

    finding_attrs = kwargs.copy()
    finding_attrs.update({
        'analyst': analyst_email,
        'cvss_version': '3',
        'exploitability': 0,
        'files': [],
        'finding': title,
        'report_date': creation_date,
        'historic_state': [submission_history]
    })

    if re.search(r'^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+', title):

        return finding_dal.create(finding_id, project_name, finding_attrs)
    raise InvalidDraftTitle()


def send_new_draft_mail(
    analyst_email, finding_id, finding_title, project_name
):
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients += project_domain.list_internal_managers(project_name)

    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_context = {
        'analyst_email': analyst_email,
        'finding_id': finding_id,
        'finding_name': finding_title,
        'finding_url': base_url + '/project/{project!s}/drafts/{id!s}'
                                  '/description'.format(
                                      project=project_name, id=finding_id),
        'project': project_name
    }
    email_send_thread = threading.Thread(
        name='New draft email thread',
        target=send_mail_new_draft,
        args=(recipients, email_context))
    email_send_thread.start()


def submit_draft(finding_id, analyst_email):
    success = False
    finding = get_finding(finding_id)
    submission_history = finding.get('historicState')

    if 'releaseDate' not in finding and \
       submission_history[-1].get('state') != 'DELETED':
        is_submitted = submission_history[-1].get('state') == 'SUBMITTED'
        if not is_submitted:
            evidence_list = [finding['evidence'].get(ev_name)
                             for ev_name in finding['evidence']]
            has_evidence = any([evidence.get('url')
                                for evidence in evidence_list])
            has_severity = finding['severityCvss'] > Decimal(0)
            has_vulns = vuln_domain.list_vulnerabilities([finding_id])

            if all([has_evidence, has_severity, has_vulns]):
                tzn = pytz.timezone(settings.TIME_ZONE)
                report_date = datetime.now(tz=tzn).today()
                report_date = report_date.strftime('%Y-%m-%d %H:%M:%S')
                history = finding.get('historicState', [])
                history.append({
                    'analyst': analyst_email,
                    'date': report_date,
                    'state': 'SUBMITTED'
                })

                success = finding_dal.update(finding_id, {
                    'report_date': report_date,
                    'historic_state': history
                })
                if success:
                    send_new_draft_mail(analyst_email,
                                        finding_id,
                                        finding.get('finding'),
                                        finding.get('projectName'))
            else:
                required_fields = {
                    'evidence': has_evidence,
                    'severity': has_severity,
                    'vulnerabilities': has_vulns
                }
                raise IncompleteDraft([field for field in required_fields
                                       if not required_fields[field]])
        else:
            raise AlreadySubmitted()
    else:
        raise AlreadyApproved()

    return success


def mask_finding(finding_id):
    finding = get_finding(finding_id)

    attrs_to_mask = [
        'affected_systems', 'attack_vector_desc', 'effect_solution',
        'related_findings', 'risk', 'threat', 'treatment',
        'treatment_justification', 'treatment_manager', 'vulnerability'
    ]
    finding_result = finding_dal.update(finding_id, {
        attr: 'Masked' for attr in attrs_to_mask
    })

    evidence_prefix = '{}/{}'.format(finding['projectName'], finding_id)
    evidence_result = all([
        finding_dal.remove_evidence(file_name)
        for file_name in finding_dal.search_evidence(evidence_prefix)])
    finding_dal.update(finding_id, {
        'files': [
            {'file_url': 'Masked', 'name': 'Masked', 'description': 'Masked'}
            for _ in finding['evidence']
        ]
    })

    comments = integrates_dal.get_comments_dynamo(int(finding_id), 'comment')
    comments_result = all([integrates_dal.delete_comment_dynamo(
        comment['finding_id'], comment['user_id']) for comment in comments])

    vulns_result = all([
        vuln_domain.mask_vuln(finding_id, vuln['UUID'])
        for vuln in vuln_domain.get_vulnerabilities(finding_id)])

    success = all([
        finding_result, evidence_result, comments_result, vulns_result])
    util.invalidate_cache(finding_id)

    return success


def evidence_exceeds_size(uploaded_file, evidence_type, context):
    evidence = list(range(7))
    exploit = 7
    records = 8
    mib = 1048576
    if evidence_type in evidence:
        size = uploaded_file.size > 10 * mib
    elif evidence_type == exploit:
        size = uploaded_file.size > 1 * mib
    elif evidence_type == records:
        size = uploaded_file.size > 1 * mib
    else:
        util.cloudwatch_log(context, 'Security: \
Attempted to upload an unknown type of evidence')
        raise InvalidFileSize()
    return size


def validate_finding(finding_id=0, finding=None):
    """Validate if a finding is not deleted."""
    if not finding:
        finding = finding_dal.get_finding(finding_id)
    return finding.get(
        'historic_state', [{}])[-1].get('state', '') != 'DELETED'
