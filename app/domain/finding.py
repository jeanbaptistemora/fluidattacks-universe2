from __future__ import absolute_import, division
import sys
import threading
from datetime import datetime, timedelta
from decimal import Decimal
from time import time

import pytz
import rollbar
from django.conf import settings
from graphql import GraphQLError
from i18n import t

from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_MAIL_REVIEWERS, FI_MAIL_REPLYERS
)
from app import util
from app.dal.helpers.drive import DriveAPI
from app.dal.helpers.formstack import FormstackAPI
from app.dal import integrates_dal, finding as finding_dal, user as user_dal
from app.domain.vulnerability import update_vulnerabilities_date
from app.dto.finding import (
    FindingDTO, get_project_name, migrate_description, migrate_treatment,
    migrate_report_date, finding_vulnerabilities
)
from app.exceptions import FindingNotFound
from app.mailer import (
    send_mail_comment, send_mail_verified_finding, send_mail_remediate_finding,
    send_mail_accepted_finding, send_mail_delete_draft, send_mail_delete_finding
)
from app.utils import (
    cvss, forms as forms_utils, notifications, findings as finding_utils
)


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


def migrate_all_files(finding_id, project_name):
    fin_dto = FindingDTO()
    api = FormstackAPI()
    try:
        finding = fin_dto.parse(finding_id, api.get_submission(finding_id))
        files = [
            {'id': '0', 'name': 'animation', 'field': fin_dto.ANIMATION, 'ext': '.gif'},
            {'id': '1', 'name': 'exploitation', 'field': fin_dto.EXPLOTATION, 'ext': '.png'},
            {'id': '2', 'name': 'evidence_route_1', 'field': fin_dto.DOC_ACHV1, 'ext': '.png'},
            {'id': '3', 'name': 'evidence_route_2', 'field': fin_dto.DOC_ACHV2, 'ext': '.png'},
            {'id': '4', 'name': 'evidence_route_3', 'field': fin_dto.DOC_ACHV3, 'ext': '.png'},
            {'id': '5', 'name': 'evidence_route_4', 'field': fin_dto.DOC_ACHV4, 'ext': '.png'},
            {'id': '6', 'name': 'evidence_route_5', 'field': fin_dto.DOC_ACHV5, 'ext': '.png'},
            {'id': '7', 'name': 'exploit', 'field': fin_dto.EXPLOIT, 'ext': '.exp'},
            {'id': '8', 'name': 'fileRecords', 'field': fin_dto.REG_FILE, 'ext': '.csv'}
        ]
        for file_obj in files:
            base_name = '{proj}/{fin}/{proj}-{fin}-{field}'.format(
                field=file_obj['field'],
                fin=finding_id,
                proj=project_name)
            already_migrated = finding_dal.search_evidence(base_name)
            has_file = file_obj['name'] in finding
            if has_file and not already_migrated:
                drive_api = DriveAPI()

                file_name = finding[file_obj['name']]
                download_path = drive_api.download(file_name)
                if download_path:
                    full_name = '{base}-{name}{ext}'.format(
                        base=base_name,
                        ext=file_obj['ext'],
                        name=file_name.replace(' ', '-'))
                    if finding_dal.migrate_evidence(download_path, full_name):
                        file_name = full_name.split('/')[2]
                        save_file_url(finding_id, file_obj['name'], file_name)
                else:
                    rollbar.report_message(
                        'Error: An error occurred downloading file from Drive',
                        'error')
    except KeyError:
        rollbar.report_exc_info(sys.exc_info())


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
    if sorted_dates:
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


def filter_evidence_filename(evidence_files, name):
    evidence_info = [evidence for evidence in evidence_files
                     if evidence['name'] == name]
    return evidence_info[0].get('file_url', '') if evidence_info else ''


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
    if not all(response):
        return False
    return True


def list_comments(user_email, comment_type, finding_id):
    comments = [{
        'content': comment['content'],
        'created': util.format_comment_date(comment['created']),
        'created_by_current_user': comment['email'] == user_email,
        'email': comment['email'],
        'fullname': comment['fullname'],
        'id': int(comment['user_id']),
        'modified': util.format_comment_date(comment['modified']),
        'parent': int(comment['parent'])
    } for comment in integrates_dal.get_comments_dynamo(int(finding_id), comment_type)]

    return comments


def get_email_recipients(project_name, comment_type):
    project_users = integrates_dal.get_project_users(project_name)
    recipients = []

    if comment_type == 'observation':
        approvers = FI_MAIL_REVIEWERS.split(',')
        analysts = [user[0] for user in project_users
                    if user_dal.get_role(user[0]) == 'analyst']

        recipients += approvers
        recipients += analysts
    else:
        recipients = [user[0] for user in project_users if user[1] == 1]
        replyers = FI_MAIL_REPLYERS.split(',')
        recipients += replyers

    return recipients


def send_comment_mail(user_email, comment_data, finding_id):
    comment_type = comment_data['comment_type']
    project_name = get_project_name(finding_id).lower()
    recipients = get_email_recipients(project_name, comment_type)
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    dynamo_value = integrates_dal.get_finding_attributes_dynamo(
        finding_id, ['finding'])
    if dynamo_value:
        finding_title = dynamo_value.get('finding')
    else:
        fin_dto = FindingDTO()
        api = FormstackAPI()
        finding_title = fin_dto.parse(
            finding_id, api.get_submission(finding_id)
        ).get('finding')

    email_context = {
        'project': project_name,
        'finding_name': finding_title,
        'user_email': user_email,
        'finding_id': finding_id,
        'comment': comment_data['content'].replace('\n', ' '),
        'comment_type': comment_type,
        'parent': comment_data['parent'],
        'comment_url':
            base_url + '/project/{project!s}/{finding!s}/{comment_type!s}s'
        .format(project=project_name, finding=finding_id,
                comment_type=comment_type)
    }
    mail_title = \
        'New {comment_type!s} email thread'.format(comment_type=comment_type)
    email_send_thread = threading.Thread(
        name=mail_title,
        target=send_mail_comment,
        args=(recipients,
              email_context))
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
    project_users = integrates_dal.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]

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


def get_tracking_vulnerabilities(act_finding, vulnerabilities):
    """get tracking vulnerabilities dictionary"""
    tracking = []
    release_date = act_finding['releaseDate']
    if release_date:
        vuln_casted = remove_repeated(vulnerabilities)
        unique_dict = get_unique_dict(vuln_casted)
        tracking = get_tracking_dict(unique_dict)
        tracking_grouped = group_by_state(tracking)
        order_tracking = sorted(tracking_grouped.items())
        tracking_casted = cast_tracking(order_tracking)
        tracking = tracking_casted
    return tracking


def verify_finding(finding_id, user_email):
    project_name = get_project_name(finding_id).lower()
    finding_name = \
        integrates_dal.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')
    success = finding_dal.verify(finding_id)
    if success:
        update_vulnerabilities_date(user_email, finding_id)
        send_finding_verified_email(finding_id,
                                    finding_name, project_name)
        project_users = [user[0]
                         for user
                         in integrates_dal.get_project_users(project_name)
                         if user[1] == 1]
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
    project_users = integrates_dal.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]

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
    project_name = get_project_name(finding_id).lower()
    finding_name = \
        integrates_dal.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')
    success = finding_dal.request_verification(finding_id)
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
        project_users = [user[0]
                         for user
                         in integrates_dal.get_project_users(project_name)
                         if user[1] == 1]
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

    if updated_values.get('probability') and updated_values.get('severity'):
        if updated_values['severity'] < 0 or updated_values['severity'] > 5:
            raise GraphQLError('Invalid severity')
        else:
            updated_values['risk_value'] = calc_risk_level(
                updated_values['probability'],
                updated_values['severity'])

    description = integrates_dal.get_finding_attributes_dynamo(
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
    return integrates_dal.update_mult_attrs_dynamo(
        'FI_findings',
        {'finding_id': finding_id},
        updated_values
    )


def send_accepted_email(finding_id, user_email, justification):
    project_name = get_project_name(finding_id).lower()
    project_users = integrates_dal.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
    finding_name = \
        integrates_dal.get_finding_attributes_dynamo(finding_id,
                                                     ['finding']).get('finding')

    email_send_thread = threading.Thread(
        name='Accepted finding email thread',
        target=send_mail_accepted_finding,
        args=(recipients, {
            'user_mail': user_email,
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


def update_treatment(finding_id, updated_values, user_email):
    updated_values['external_bts'] = updated_values.get('bts_url')
    del updated_values['bts_url']

    if updated_values['treatment'] == 'NEW':
        updated_values['external_bts'] = ''
    if updated_values['treatment'] == 'ACCEPTED':
        updated_values['external_bts'] = ''
        send_accepted_email(finding_id, user_email,
                            updated_values.get('treatment_justification'))

    result_update_finding = integrates_dal.update_mult_attrs_dynamo(
        'FI_findings',
        {'finding_id': finding_id},
        updated_values
    )
    result_update_vuln = update_treatment_in_vuln(finding_id, updated_values)
    if result_update_finding and result_update_vuln:
        return True
    return False


def save_severity(finding):
    """Organize severity metrics to save in dynamo."""
    fin_dto = FindingDTO()
    primary_keys = ['finding_id', str(finding['id'])]
    cvss_version = finding.get('cvssVersion', '')
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
        cvss_parameters = fin_dto.CVSS3_PARAMETERS
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
        cvss_parameters = fin_dto.CVSS_PARAMETERS
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

    email_send_thread = threading.Thread(
        name='Reject draft email thread',
        target=send_mail_delete_draft,
        args=(recipients, {
            'project': project_name,
            'analyst_mail': discoverer_email,
            'finding_name': finding_name,
            'admin_mail': reviewer_email,
            'finding_id': draft_id,
        }))
    email_send_thread.start()


def reject_draft(draft_id, reviewer_email, project_name, context):
    fin_dto = FindingDTO()
    api = FormstackAPI()
    is_draft = ('releaseDate' not in
                integrates_dal.get_finding_attributes_dynamo(draft_id, ['releaseDate']))
    result = False

    if is_draft:
        finding_data = fin_dto.parse(draft_id, api.get_submission(draft_id))

        delete_all_comments(draft_id)
        delete_all_evidences_s3(draft_id, project_name, context)
        integrates_dal.delete_finding_dynamo(draft_id)

        for vuln in integrates_dal.get_vulnerabilities_dynamo(draft_id):
            integrates_dal.delete_vulnerability_dynamo(vuln['UUID'], draft_id)

        api.delete_submission(draft_id)
        send_draft_reject_mail(
            draft_id, project_name, finding_data['analyst'],
            finding_data['finding'], reviewer_email)
        result = True
    else:
        raise GraphQLError('CANT_REJECT_FINDING')

    return result


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


def delete_finding(finding_id, project_name, justification, context):
    fin_dto = FindingDTO()
    api = FormstackAPI()
    is_finding = ('releaseDate' in
                  integrates_dal.get_finding_attributes_dynamo(finding_id, ['releaseDate']))
    result = False

    if is_finding:
        finding_data = fin_dto.parse(finding_id, api.get_submission(finding_id))

        delete_all_comments(finding_id)
        delete_all_evidences_s3(finding_id, project_name, context)
        integrates_dal.delete_finding_dynamo(finding_id)

        for vuln in integrates_dal.get_vulnerabilities_dynamo(finding_id):
            integrates_dal.delete_vulnerability_dynamo(vuln['UUID'], finding_id)

        api.delete_submission(finding_id)
        send_finding_delete_mail(
            finding_id, finding_data['finding'], project_name,
            finding_data['analyst'], justification)
        result = True
    else:
        raise GraphQLError('CANT_DELETE_DRAFT')

    return result


def approve_draft(draft_id, project_name, context):
    fin_dto = FindingDTO()
    api = FormstackAPI()
    is_draft = ('releaseDate' not in
                integrates_dal.get_finding_attributes_dynamo(draft_id, ['releaseDate']))
    success = False
    has_vulns = integrates_dal.get_vulnerabilities_dynamo(draft_id)

    if is_draft:
        if has_vulns:
            finding_data = fin_dto.parse(draft_id, api.get_submission(draft_id))
            release_date, has_release, has_last_vuln = update_release(project_name,
                                                                      finding_data, draft_id)
            if has_release and has_last_vuln:
                integrates_dal.add_release_to_project_dynamo(
                    project_name, release_date)
            else:
                rollbar.report_message('Error: An error occurred accepting the draft', 'error')
        else:
            raise GraphQLError('CANT_APPROVE_FINDING_WITHOUT_VULNS')
    else:
        util.cloudwatch_log(context,
                            'Security: Attempted to accept an already \
                            released finding')
        raise GraphQLError('CANT_APPROVE_FINDING')
    return success, release_date


def update_release(project_name, finding_data, draft_id):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    release_date = datetime.now(tz=local_timezone).date()
    if ('subscription' in finding_data and
            finding_data['subscription'] in ['CONTINUOUS', 'Concurrente', 'Si']):
        releases = integrates_dal.get_project_dynamo(project_name)

        for release in releases:
            if 'lastRelease' in release:
                last_release = datetime.strptime(
                    release['lastRelease'].split(' ')[0], '%Y-%m-%d')
                last_release = last_release.replace(tzinfo=local_timezone).date()
                if last_release >= release_date:
                    release_date = last_release + timedelta(days=1)
    release_date = release_date.strftime('%Y-%m-%d %H:%M:%S')
    has_release = integrates_dal.add_attribute_dynamo('FI_findings', ['finding_id', draft_id],
                                                      'releaseDate', release_date)
    has_last_vuln = integrates_dal.add_attribute_dynamo('FI_findings', ['finding_id', draft_id],
                                                        'lastVulnerability', release_date)
    return release_date, has_release, has_last_vuln


def migrate_finding(draft_id, finding_data):
    migrate_all_files(draft_id, finding_data['projectName'])
    save_severity(finding_data)
    migrate_description(finding_data)
    migrate_treatment(finding_data)
    migrate_report_date(finding_data)
    migrate_evidence_description(finding_data)
    if not (save_severity or migrate_description or migrate_treatment or migrate_report_date or
            migrate_evidence_description):
        return False
    return True


def get_finding(finding_id):
    finding = finding_dal.get_finding(finding_id)
    if not finding:
        fs_finding = finding_vulnerabilities(finding_id)
        if fs_finding:
            migrate_finding(finding_id, fs_finding)
            finding = finding_dal.get_finding(finding_id)
        else:
            raise FindingNotFound()

    finding = finding_utils.format_data(finding)

    return finding


def list_findings(finding_ids):
    """Retrieves all attributes for the requested findings"""
    findings = []
    for finding_id in finding_ids:
        finding = finding_dal.get_finding(finding_id)
        if not finding:
            fs_finding = finding_vulnerabilities(finding_id)
            if fs_finding:
                migrate_finding(finding_id, fs_finding)
                finding = finding_dal.get_finding(finding_id)
            else:
                raise FindingNotFound()

        findings += finding_utils.format_data(finding)

    return findings


def save_evidence(evidence_field, finding_id, project_name, uploaded_file):
    full_name = '{proj}/{fin}/{proj}-{fin}-{field}-{name}'.format(
        field=evidence_field[1],
        fin=finding_id,
        name=uploaded_file.name.replace(' ', '-'),
        proj=project_name)
    success = finding_dal.save_evidence(uploaded_file, full_name)
    if success:
        file_name = full_name.split('/')[2]
        save_file_url(finding_id, evidence_field[0], file_name)

    return success
