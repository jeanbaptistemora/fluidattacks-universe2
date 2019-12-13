import datetime
import io
import itertools

import rollbar
from backports import csv
from magic import Magic

from backend import util
from backend.utils import cvss, forms as forms_utils

from app.dal import finding as finding_dal


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
    raise Exception('Evidence not found')


def get_records_from_file(project_name, finding_id, file_name):
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


def get_exploit_from_file(project_name, finding_id, file_name):
    file_path = _download_evidence_file(project_name, finding_id, file_name)
    file_content = ''

    with open(file_path, 'r') as exploit_file:
        file_content = exploit_file.read()

    return file_content


# pylint: disable=simplifiable-if-expression
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
    finding['exploitable'] = forms_utils.is_exploitable(
        float(finding['exploitability']), finding['cvssVersion']) == 'Si'

    def_date = '1900-1-1 0:0:0'
    ver_date = finding.get('verificationDate') \
        if finding.get('verificationDate') else def_date
    ver_date = datetime.datetime.strptime(ver_date, '%Y-%m-%d %H:%M:%S')
    ver_req_date = finding.get('verificationRequestDate') \
        if finding.get('verificationRequestDate') else def_date
    ver_req_date = datetime.datetime.strptime(ver_req_date,
                                              '%Y-%m-%d %H:%M:%S')
    finding['remediated'] = (
        True if ver_req_date != def_date and ver_date == def_date
        or ver_date < ver_req_date else False)

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
        field: float(finding.get(field, 0))
        for field in cvss_fields[finding['cvssVersion']]
    }
    base_score = cvss.calculate_cvss_basescore(
        finding['severity'], CVSS_PARAMETERS[finding['cvssVersion']],
        finding['cvssVersion'])
    finding['severityCvss'] = cvss.calculate_cvss_temporal(
        finding['severity'], base_score, finding['cvssVersion'])

    return finding
