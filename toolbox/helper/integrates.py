# Standard library
from typing import Any, Dict, Tuple
import json

# Local imports
from toolbox import api, logger
from toolbox.constants import API_TOKEN, SAST, DAST


def does_finding_exist(finding_id: str) -> bool:
    """Return True if the finding exists."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    return response.ok


def is_finding_accepted(finding_id: str) -> bool:
    """Return True if a finding has an 'ACCEPTED' treatment."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    treatment: str = 'NEW'
    his_treatment: list = response.data['finding'].get('historicTreatment')
    if his_treatment:
        treatment = his_treatment[-1]['treatment']
    return treatment == 'ACCEPTED'


def is_finding_released(finding_id: str) -> bool:
    """Return True if the finding has been released."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    released_date: str = response.data['finding']['releaseDate']
    return bool(released_date)


def is_finding_open(finding_id: str, finding_types: tuple) -> bool:
    """Return True if the finding is open."""
    is_open: bool = False
    response = api.integrates.Queries.finding(API_TOKEN,
                                              finding_id,
                                              with_vulns='true')
    vulnerabilities = response.data['finding']['vulnerabilities']

    for vuln in vulnerabilities:
        if vuln['vulnType'] not in finding_types:
            continue
        current_state = vuln['historicState'][-1]
        current_state_status = current_state['state']
        approval_status = current_state.get('approval_status', 'APPROVED')

        if approval_status == 'APPROVED' and current_state_status == 'open':
            is_open = True
            break

    return is_open


def get_finding_title(finding_id: str) -> str:
    """Return the title of a fiding."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    title: str = response.data['finding']['title'].strip()
    return title


def get_finding_cvss_score(finding_id: str) -> float:
    """Return the cvss score."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    cvss_basescore: float = response.data['finding']['severityScore']
    return cvss_basescore


def get_finding_description(finding_id: str) -> str:
    """Return the description of a fiding."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    description: str = response.data['finding']['description'].strip()
    return description


def get_finding_threat(finding_id: str) -> str:
    """Return the threat of a fiding."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    threat: str = response.data['finding']['threat'].strip()
    return threat


def get_finding_attack_vector(finding_id: str) -> str:
    """Return the attack vector of a fiding."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    attack_vector_desc: str = \
        response.data['finding']['attackVectorDesc'].strip()
    return attack_vector_desc


def get_finding_recommendation(finding_id: str) -> str:
    """Return the recommendation of a fiding."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    recommendation: str = response.data['finding']['recommendation'].strip()
    return recommendation


def get_finding_wheres(finding_id: str) -> Tuple[Tuple[str, str, bool], ...]:
    """Return a tuple of (vuln_type, where, state) of a finding."""
    response = api.integrates.Queries.finding(API_TOKEN,
                                              finding_id,
                                              with_vulns='true')
    vulnerabilities = response.data['finding']['vulnerabilities']

    type_where_state: Tuple[Tuple[str, str, bool], ...] = tuple(
        (vuln['vulnType'], vuln['where'], current_state['state'] == 'open')
        for vuln in vulnerabilities
        for current_state in (vuln['historicState'][-1],)
        if current_state.get('approval_status', 'APPROVED') == 'APPROVED'
    )
    return type_where_state


def get_finding_static_where_states(finding_id: str
                                    ) -> Tuple[Dict[str, Any], ...]:
    """Return a tuple of {'path': str, 'state': bool}, True is OPEN."""
    states: Tuple[Dict[str, Any], ...] = tuple(
        {
            'path': where,
            'state': state,
        }
        for vuln_type, where, state in get_finding_wheres(finding_id)
        if vuln_type in SAST)

    return states


def get_finding_repos(finding_id: str) -> tuple:
    """Return the repositories of a finding."""
    repos = set()
    for element in get_finding_static_where_states(finding_id):
        where = element['path']

        if '/' in where:
            repos.add(where.split('/', 1)[0])
        else:
            logger.warn(f'weird where: {where} at finding {finding_id}')
            repos.add(where)
    return tuple(repos)


def get_finding_type(finding_id: str) -> Tuple[bool, bool]:
    """Return a tuple of booleans (sast, dast) for a finding."""
    finding_wheres: Tuple[Tuple[str, str, bool], ...] = get_finding_wheres(
        finding_id)

    is_sast: bool = \
        any(vuln_type in SAST for vuln_type, _, _ in finding_wheres)
    is_dast: bool = \
        any(vuln_type in DAST for vuln_type, _, _ in finding_wheres)

    return is_sast, is_dast


def get_project_findings(project: str) -> Tuple[Tuple[str, str], ...]:
    """Return tuples of (finding_id, finding_title) for a project."""
    response = api.integrates.Queries.project(
        api_token=API_TOKEN,
        project_name=project,
        with_findings='true')

    findings = response.data['project']['findings']

    result: Tuple[Tuple[str, str], ...] = tuple(
        (finding['id'], finding['title'])
        for finding in findings)

    return result


def delete_pending_vulns(finding_id: str) -> bool:
    """Delete all pending vulnerabilities for a finding."""
    response = api.integrates.Mutations.approve_vulns(
        api_token=API_TOKEN,
        finding_id=finding_id,
        approval_status='false')
    return response.data['approveVulnerability']['success']


def get_project_repos(project: str) -> list:
    """Return the repositories for a porject"""
    response = api.integrates.Queries.resources(
        api_token=API_TOKEN,
        project_name=project)

    repositories = json.loads(response.data['resources']['repositories'])

    return repositories
