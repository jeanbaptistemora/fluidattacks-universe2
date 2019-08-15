import io
import itertools

import rollbar
from backports import csv
from magic import Magic

from app import util
from app.dal import finding as finding_dal, vulnerability as vuln_dal
from app.utils import cvss, forms as forms_utils


CVSS_PARAMETERS = {
    '2': {
        'bs_factor_1': 0.6, 'bs_factor_2': 0.4, 'bs_factor_3': 1.5,
        'impact_factor': 10.41, 'exploitability_factor': 20
    },
    '3': {
        'impact_factor_1': 6.42, 'impact_factor_2': 7.52,
        'impact_factor_3': 0.029, 'impact_factor_4': 3.25,
        'impact_factor_5': 0.02, 'impact_factor_6': 15,
        'exploitability_factor_1': 8.22, 'basescore_factor': 1.08,
        'mod_impact_factor_1': 0.915, 'mod_impact_factor_2': 6.42,
        'mod_impact_factor_3': 7.52, 'mod_impact_factor_4': 0.029,
        'mod_impact_factor_5': 3.25, 'mod_impact_factor_6': 0.02,
        'mod_impact_factor_7': 15
    }
}


def _get_evidence(name, items):
    evidence = [
        {'url': item['file_url'], 'description': item.get('description', '')}
        for item in items
        if item['name'] == name]

    return evidence[0] if evidence else {'url': '', 'description': ''}


def _download_evidence_file(project_name, finding_id, file_name):
    file_id = '/'.join([project_name.lower(), finding_id, file_name])
    file_exists = finding_dal.search_evidence(file_id)

    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = '/tmp' + file_id[start:]
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)
        finding_dal.download_evidence(file_id, tmp_filepath)
        return tmp_filepath
    else:
        raise Exception('Evidence not found')


def get_records_from_file(project_name, finding_id, file_name):
    file_path = _download_evidence_file(project_name, finding_id, file_name)
    file_content = []
    encoding = Magic(mime_encoding=True).from_file(file_path)

    try:
        with io.open(file_path, mode='r', encoding=encoding) as records_file:
            csv_reader = csv.reader(records_file)
            max_rows = 1000
            headers = csv_reader.next()
            file_content = [util.list_to_dict(headers, row)
                            for row in itertools.islice(csv_reader, max_rows)]
    except (csv.Error, LookupError, UnicodeDecodeError) as ex:
        rollbar.report_message('Error: Couldnt read records file', 'error',
                               extra_data=ex, payload_data=locals())

    return file_content


def get_exploit_from_file(project_name, finding_id, file_name):
    file_path = _download_evidence_file(project_name, finding_id, file_name)
    file_content = ''

    with open(file_path, 'r') as exploit_file:
        file_content = exploit_file.read()

    return file_content


def format_data(finding):
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
            finding['releaseDate']).days
    finding['detailedSeverity'] = finding.get('severity', 0)
    finding['exploitable'] = forms_utils.is_exploitable(
        float(finding['exploitability']), finding['cvssVersion'])
    finding['remediated'] = (
        True if finding.get('verificationRequestDate')
        and not finding.get('verificationDate')
        or finding.get('verificationDate')
        < finding.get('verificationRequestDate')
        else False)

    finding['evidence'] = {
        'animation': _get_evidence('animation', finding['files']),
        'evidence1': _get_evidence('evidence_route_1', finding['files']),
        'evidence2': _get_evidence('evidence_route_2', finding['files']),
        'evidence3': _get_evidence('evidence_route_3', finding['files']),
        'evidence4': _get_evidence('evidence_route_4', finding['files']),
        'evidence5': _get_evidence('evidence_route_5', finding['files']),
        'exploitation': _get_evidence('exploitation', finding['files'])
    }
    finding['compromisedAttrs'] = finding.get('records', '')
    finding['records'] = _get_evidence('fileRecords', finding['files'])
    finding['exploit'] = _get_evidence('exploit', finding['files'])

    open_vulns, closed_vulns = vuln_dal.get_vulns_state(finding['findingId'])
    finding['openVulnerabilities'] = open_vulns
    finding['closedVulnerabilities'] = closed_vulns
    finding['state'] = 'open' if open_vulns else 'closed'

    cvss_fields = {
        '2': ['accessComplexity', 'accessVector', 'authentication',
              'availabilityImpact', 'availabilityRequirement',
              'collateralDamagePotential', 'confidenceLevel',
              'confidentialityImpact', 'confidentialityRequirement',
              'exploitability', 'findingDistribution', 'integrityImpact',
              'integrityRequirement', 'resolutionLevel'],
        '3': ['attackComplexity', 'attackVector', 'availabilityImpact',
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
        field: float(finding[field])
        for field in cvss_fields[finding['cvssVersion']]
    }
    base_score = cvss.calculate_cvss_basescore(
        finding['severity'], CVSS_PARAMETERS[finding['cvssVersion']],
        finding['cvssVersion'])
    finding['severityCvss'] = cvss.calculate_cvss_temporal(
        finding['severity'], base_score, finding['cvssVersion'])

    return finding
