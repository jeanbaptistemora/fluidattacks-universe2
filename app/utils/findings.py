from app import util
from app.dao import integrates_dao
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


def format_data(finding):
    finding = {
        util.snakecase_to_camelcase(attribute): finding.get(attribute)
        for attribute in finding
    }

    finding['age'] = util.calculate_datediff_since(finding['releaseDate']).days
    finding['detailedSeverity'] = finding.get('severity', 0)
    finding['exploitable'] = forms_utils.is_exploitable(
        float(finding['exploitability']), finding['cvssVersion'])

    vulns = integrates_dao.get_vulnerabilities_dynamo(finding['findingId'])
    open_vulns = [vuln for vuln in vulns
                  if vuln['historic_state'][-1]['state'] == 'open']
    closed_vulns = [vuln for vuln in vulns
                    if vuln['historic_state'][-1]['state'] == 'closed']
    finding['vulnerabilities'] = vulns
    finding['openVulnerabilities'] = len(open_vulns)
    finding['closedVulnerabilities'] = len(closed_vulns)
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
