import io
import itertools

import threading
from datetime import datetime
from typing import Dict, List, Union, cast
import rollbar
from backports import csv  # type: ignore
from magic import Magic

from backend import util
from backend.utils import cvss, forms as forms_utils

from backend.dal import finding as finding_dal, project as project_dal, vulnerability as vuln_dal
from backend.typing import Finding as FindingType
from backend.mailer import (
    send_mail_verified_finding, send_mail_remediate_finding, send_mail_delete_finding,
    send_mail_accepted_finding, send_mail_reject_draft, send_mail_new_draft
)
from __init__ import (
    FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS, FI_MAIL_REVIEWERS
)


CVSS_PARAMETERS = {
    '2': {
        'bs_factor_1': 0.6, 'bs_factor_2': 0.4, 'bs_factor_3': 1.5,
        'impact_factor': 10.41, 'exploitability_factor': 20
    },
    '3.1': {
        'impact_factor_1': 6.42, 'impact_factor_2': 7.52,
        'impact_factor_3': 0.029, 'impact_factor_4': 3.25,
        'impact_factor_5': 0.02, 'impact_factor_6': 15,
        'exploitability_factor_1': 8.22, 'basescore_factor': 1.08,
        'mod_impact_factor_1': 0.915, 'mod_impact_factor_2': 6.42,
        'mod_impact_factor_3': 7.52, 'mod_impact_factor_4': 0.029,
        'mod_impact_factor_5': 3.25, 'mod_impact_factor_6': 0.02,
        'mod_impact_factor_7': 13, 'mod_impact_factor_8': 0.9731
    }
}


def _get_evidence(name: str, items: List[Dict[str, str]]) -> Dict[str, str]:
    evidence = [
        {'url': item['file_url'], 'description': item.get('description', '')}
        for item in items
        if item['name'] == name]

    return evidence[0] if evidence else {'url': '', 'description': ''}


def _download_evidence_file(project_name: str, finding_id: str, file_name: str) -> str:
    file_id = '/'.join([project_name.lower(), finding_id, file_name])
    file_exists = finding_dal.search_evidence(file_id)

    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = '/tmp' + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)
        finding_dal.download_evidence(file_id, tmp_filepath)
        return tmp_filepath
    raise Exception('Evidence not found')


def get_records_from_file(
        project_name: str, finding_id: str, file_name: str) -> List[Dict[object, object]]:
    file_path = _download_evidence_file(project_name, finding_id, file_name)
    file_content = []
    encoding = Magic(mime_encoding=True).from_file(file_path)

    try:
        with io.open(file_path, mode='r', encoding=encoding) as records_file:
            csv_reader = csv.reader(records_file)
            max_rows = 1000
            headers = next(csv_reader)
            file_content = [util.list_to_dict(headers, row)
                            for row in itertools.islice(csv_reader, max_rows)]
    except (csv.Error, LookupError, UnicodeDecodeError) as ex:
        rollbar.report_message('Error: Couldnt read records file', 'error',
                               extra_data=ex, payload_data=locals())

    return file_content


def get_exploit_from_file(project_name: str, finding_id: str, file_name: str) -> str:
    file_path = _download_evidence_file(project_name, finding_id, file_name)
    file_content = ''

    with open(file_path, 'r') as exploit_file:
        file_content = exploit_file.read()

    return file_content


# pylint: disable=simplifiable-if-expression
def format_data(finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    finding = {
        util.snakecase_to_camelcase(attribute): finding.get(attribute)
        for attribute in finding
    }

    is_draft = 'releaseDate' not in finding
    if is_draft:
        finding['age'] = 0
        finding['cvssVersion'] = finding.get('cvssVersion', '2')
    else:
        finding['age'] = util.calculate_datediff_since(
            cast(datetime, finding['releaseDate'])).days
    finding['exploitable'] = forms_utils.is_exploitable(
        float(str(finding.get('exploitability', ''))), str(finding.get('cvssVersion', ''))) == 'Si'

    historic_verification = cast(List[Dict[str, str]], finding.get('historicVerification', [{}]))
    finding['remediated'] = \
        (historic_verification[-1].get('status') == 'REQUESTED' and
         not historic_verification[-1].get('vulns', []))

    vulns = vuln_dal.get_vulnerabilities(str(finding.get('findingId', '')))
    open_vulns = \
        [vuln for vuln in vulns
         if cast(List[Dict[str, str]], vuln.get('historic_state', [{}]))[-1].get(
             'state') == 'open']
    remediated_vulns = \
        [vuln for vuln in open_vulns
         if cast(List[Dict[str, str]], vuln.get('historic_verification', [{}]))[-1].get(
             'status') == 'REQUESTED']
    finding['newRemediated'] = len(open_vulns) == len(remediated_vulns)
    finding['verified'] = len(remediated_vulns) == 0
    finding_files = cast(List[Dict[str, str]], finding.get('files'))
    finding['evidence'] = {
        'animation': _get_evidence('animation', finding_files),
        'evidence1': _get_evidence('evidence_route_1', finding_files),
        'evidence2': _get_evidence('evidence_route_2', finding_files),
        'evidence3': _get_evidence('evidence_route_3', finding_files),
        'evidence4': _get_evidence('evidence_route_4', finding_files),
        'evidence5': _get_evidence('evidence_route_5', finding_files),
        'exploitation': _get_evidence('exploitation', finding_files)
    }
    finding['compromisedAttrs'] = finding.get('records', '')
    finding['records'] = _get_evidence('fileRecords', finding_files)
    finding['exploit'] = _get_evidence('exploit', finding_files)

    cvss_fields = {
        '2': ['accessComplexity', 'accessVector', 'authentication',
              'availabilityImpact', 'availabilityRequirement',
              'collateralDamagePotential', 'confidenceLevel',
              'confidentialityImpact', 'confidentialityRequirement',
              'exploitability', 'findingDistribution', 'integrityImpact',
              'integrityRequirement', 'resolutionLevel'],
        '3.1': ['attackComplexity', 'attackVector', 'availabilityImpact',
                'availabilityRequirement', 'confidentialityImpact',
                'confidentialityRequirement', 'exploitability',
                'integrityImpact', 'integrityRequirement',
                'modifiedAttackComplexity', 'modifiedAttackVector',
                'modifiedAvailabilityImpact', 'modifiedConfidentialityImpact',
                'modifiedIntegrityImpact', 'modifiedPrivilegesRequired',
                'modifiedUserInteraction', 'modifiedSeverityScope',
                'privilegesRequired', 'remediationLevel', 'reportConfidence',
                'severityScope', 'userInteraction']
    }
    finding['severity'] = {
        field: cast(str, float(str(finding.get(field, 0))))
        for field in cvss_fields[str(finding['cvssVersion'])]
    }
    base_score = cvss.calculate_cvss_basescore(
        cast(Dict[str, float], finding['severity']), CVSS_PARAMETERS[str(finding['cvssVersion'])],
        str(finding['cvssVersion']))
    finding['severityCvss'] = cvss.calculate_cvss_temporal(
        cast(Dict[str, float], finding['severity']), base_score, str(finding['cvssVersion']))

    return finding


def send_finding_verified_email(finding_id: str, finding_name: str, project_name: str):
    recipients = project_dal.get_users(project_name)

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


def send_finding_delete_mail(finding_id: str, finding_name: str, project_name: str,
                             discoverer_email: str, justification: str):
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


def send_remediation_email(user_email: str, finding_id: str, finding_name: str,
                           project_name: str, justification: str):
    recipients = project_dal.get_users(project_name)
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


def send_accepted_email(finding: Dict[str, FindingType], justification: str):
    project_name = str(finding.get('projectName', ''))
    finding_name = str(finding.get('finding', ''))
    last_historic_treatment = cast(List[Dict[str, str]], finding.get('historicTreatment'))[-1]
    recipients = project_dal.get_users(project_name)
    treatment = 'Accepted'
    if last_historic_treatment['treatment'] == 'ACCEPTED_UNDEFINED':
        treatment = 'Indefinitely accepted'
    email_send_thread = threading.Thread(
        name='Accepted finding email thread',
        target=send_mail_accepted_finding,
        args=(recipients, {
            'finding_name': finding_name,
            'finding_id': finding.get('finding_id'),
            'project': project_name.capitalize(),
            'justification': justification,
            'user_email': last_historic_treatment['user'],
            'treatment': treatment
        }))

    email_send_thread.start()


def send_draft_reject_mail(draft_id: str, project_name: str, discoverer_email: str,
                           finding_name: str, reviewer_email: str):
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


def send_new_draft_mail(
        analyst_email: str, finding_id: str, finding_title: str, project_name: str):
    recipients = FI_MAIL_REVIEWERS.split(',')
    recipients += project_dal.list_internal_managers(project_name)

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
