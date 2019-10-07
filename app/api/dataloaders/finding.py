from collections import defaultdict

from promise import Promise
from promise.dataloader import DataLoader

from app.domain import finding as finding_domain
from app.entity.finding import Finding


def _batch_load_fn(finding_ids):
    """Batches the data load requests within the same execution fragment"""
    findings = defaultdict(list)

    for finding in finding_domain.get_findings(finding_ids):
        findings[finding['findingId']] = Finding(
            acceptance_date=finding.get('acceptanceDate', ''),
            actor=finding.get('actor', ''),
            affected_systems=finding.get('affectedSystems', ''),
            age=finding.get('age', 0),
            ambit=finding.get('ambit', ''),
            analyst=finding.get('analyst', ''),
            attack_vector_desc=finding.get('attackVectorDesc', ''),
            bts_url=finding.get('externalBts', ''),
            category=finding.get('category', ''),
            client_code=finding.get('clientCode', ''),
            client_project=finding.get('clientProject', ''),
            compromised_attributes=finding.get('compromisedAttrs', ''),
            compromised_records=finding.get('recordsNumber', 0),
            cvss_version=finding.get('cvssVersion', '3'),
            cwe_url=finding.get('cwe', ''),
            description=finding.get('vulnerability', ''),
            detailed_severity=finding.get('detailedSeverity', 0),
            evidence=finding.get('evidence', {}),
            exploit=finding.get('exploit', {}),
            id=finding.get('findingId', ''),
            is_exploitable=finding.get('exploitable', ''),
            last_vulnerability=finding.get('lastVulnerability', 0),
            probability=finding.get('probability', 0),
            project_name=finding.get('projectName', ''),
            recommendation=finding.get('effectSolution', ''),
            records=finding.get('records', {}),
            release_date=finding.get('releaseDate', ''),
            remediated=finding.get('remediated', False),
            report_date=finding.get('reportDate', ''),
            requirements=finding.get('requirements', ''),
            risk=finding.get('risk', ''),
            risk_level=finding.get('riskValue', ''),
            scenario=finding.get('scenario', ''),
            severity=finding.get('severity', {}),
            severity_score=finding.get('severityCvss', 0.0),
            threat=finding.get('threat', ''),
            title=finding.get('finding', ''),
            treatment=finding.get('treatment', ''),
            treatment_justification=finding.get(
                'treatmentJustification', ''),
            treatment_manager=finding.get('treatmentManager', ''),
            type=finding.get('findingType', '')
        )

    return Promise.resolve([findings.get(finding_id, [])
                            for finding_id in finding_ids])


class FindingLoader(DataLoader):
    def __init__(self):
        super(FindingLoader, self).__init__(batch_load_fn=_batch_load_fn)
