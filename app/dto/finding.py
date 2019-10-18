# coding=utf-8
""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level

from ..dal import integrates_dal
from ..domain import vulnerability as vuln_domain


def total_vulnerabilities(finding_id):
    """Get total vulnerabilities in new format."""
    vulnerabilities = integrates_dal.get_vulnerabilities_dynamo(finding_id)
    finding = {'openVulnerabilities': 0, 'closedVulnerabilities': 0}
    for vuln in vulnerabilities:
        current_state = vuln_domain.get_last_approved_status(vuln)
        if current_state == 'open':
            finding['openVulnerabilities'] += 1
        elif current_state == 'closed':
            finding['closedVulnerabilities'] += 1
        else:
            # Vulnerability does not have a valid state
            pass
    return finding
