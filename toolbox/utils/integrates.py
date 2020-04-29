# Standard library
import json
import os
from typing import (
    Dict,
    List,
    Set,
    Tuple,
)

# Local imports
from toolbox import api
from toolbox.constants import API_TOKEN, SAST, DAST


def get_integrates_url(group: str, finding_id: str) -> str:
    return (
        f'https://fluidattacks.com/integrates/dashboard'
        f'#!/project/{group.upper()}/findings/{finding_id}/description'
    )


def _split_repo_and_rel_path(where: str) -> Tuple[str, str]:
    """Take an Integrates where, and return (repo, relative/path/to/file)."""
    if '/' in where:
        repo, relative_path = where.split('/', 1)
    elif '\\' in where:
        repo, relative_path = where.split('\\', 1)
    else:
        repo, relative_path = where, ''
    return repo, relative_path


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
    return treatment in ('ACCEPTED', 'ACCEPTED_UNDEFINED')


def is_finding_released(finding_id: str) -> bool:
    """Return True if the finding has been released."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    released_date: str = response.data['finding']['releaseDate']
    return bool(released_date)


def is_finding_in_subscription(finding_id: str, subscription: str) -> bool:
    """Return True if the finding is member of the provided subscription."""
    response = api.integrates.Queries.finding(API_TOKEN, finding_id)
    project_name: str = response.data['finding']['projectName']
    return project_name == subscription


def is_finding_open(finding_id: str, finding_types: tuple) -> bool:
    """Return True if the finding is open."""
    is_open: bool = False
    response = api.integrates.Queries.finding(API_TOKEN,
                                              finding_id,
                                              with_vulns=True)
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


def get_finding_wheres(
    finding_id: str,
) -> Tuple[Tuple[str, str, str, bool], ...]:
    """Return a tuple of (vuln_type, where, specific, is_open) of a finding."""
    response = api.integrates.Queries.finding(API_TOKEN,
                                              finding_id,
                                              with_vulns=True)
    vulnerabilities = response.data['finding']['vulnerabilities']

    type_where_state = tuple(
        (
            vuln['vulnType'],
            vuln['where'],
            vuln['specific'],
            current_state['state'] == 'open',
        )
        for vuln in vulnerabilities
        for current_state in (vuln['historicState'][-1],)
        if current_state.get('approval_status', 'APPROVED') == 'APPROVED'
        and current_state.get('state') != 'DELETED'
    )
    return type_where_state


def get_finding_static_states(
    finding_id: str,
) -> Tuple[Tuple[str, str, str, bool], ...]:
    """Return a tuple of (repo, relative_path, specific, is_open)."""
    states: Tuple[Tuple[str, str, str, bool], ...] = tuple(
        (*_split_repo_and_rel_path(where), specific, is_open)
        for vuln_type, where, specific, is_open
        in get_finding_wheres(finding_id)
        if vuln_type in SAST)

    return states


def get_finding_dynamic_states(
    finding_id: str,
) -> Tuple[Tuple[str, str, bool], ...]:
    """Return a tuple of (where, specific, is_open)."""
    states: Tuple[Tuple[str, str, bool], ...] = tuple(
        (where, specific, is_open)
        for vuln_type, where, specific, is_open
        in get_finding_wheres(finding_id)
        if vuln_type in DAST)

    return states


def get_finding_static_data(
    finding_id: str,
) -> Dict[str, List[Dict[str, str]]]:
    """Return a dict mapping repos to its cardinalities."""
    repo_to_cardinalities: Dict[str, List[Dict[str, str]]] = {}
    for repo, relative_path, specific, is_open in \
            get_finding_static_states(finding_id):

        data: Dict[str, str] = {
            'full_path': os.path.join(repo, relative_path),
            'relative_path': relative_path,
            'specific': specific,
            'status': 'OPEN' if is_open else 'CLOSED',
        }

        try:
            repo_to_cardinalities[repo].append(data)
        except KeyError:
            repo_to_cardinalities[repo] = [data]
    return repo_to_cardinalities


def get_finding_static_repos_states(finding_id: str) -> Dict[str, bool]:
    """Return a dict mapping repos to its expected state (OPEN, CLOSED)."""
    repos_states: Dict[str, bool] = {}
    for repo, _, _, is_open in get_finding_static_states(finding_id):
        try:
            repos_states[repo] = repos_states[repo] or is_open
        except KeyError:
            repos_states[repo] = is_open
    return repos_states


def get_finding_static_repos_vulns(
    finding_id: str,
) -> Dict[str, Dict[str, int]]:
    """Return a dict mapping repos to its vulnerabilities."""
    repos_vulns: Dict[str, Dict[str, int]] = {}
    for repo, _, _, is_open in get_finding_static_states(finding_id):
        try:
            repos_vulns[repo]['open'] += 1 if is_open else 0
            repos_vulns[repo]['closed'] += 1 if not is_open else 0
        except KeyError:
            repos_vulns[repo] = {
                'open': 1 if is_open else 0,
                'closed': 1 if not is_open else 0,
            }

    return repos_vulns


def get_finding_repos(finding_id: str) -> Tuple[str, ...]:
    """Return the repositories of a finding."""
    repos: Set[str] = set()
    for repo, _, _, _ in get_finding_static_states(finding_id):
        repos.add(repo)
    return tuple(repos)


def get_finding_type(finding_id: str) -> Tuple[bool, bool]:
    """Return a tuple of booleans (sast, dast) for a finding."""
    finding_wheres = get_finding_wheres(finding_id)

    is_sast: bool = \
        any(vuln_type in SAST for vuln_type, _, _, _ in finding_wheres)
    is_dast: bool = \
        any(vuln_type in DAST for vuln_type, _, _, _ in finding_wheres)

    return is_sast, is_dast


def get_project_findings(project: str) -> Tuple[Tuple[str, str], ...]:
    """Return tuples of (finding_id, finding_title) for a project."""
    response = api.integrates.Queries.project(
        api_token=API_TOKEN,
        project_name=project,
        with_findings=True)

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
        approval_status=False)
    return response.data['approveVulnerability']['success']


def get_project_repos(project: str) -> list:
    """Return the repositories for a porject"""
    response = api.integrates.Queries.resources(
        api_token=API_TOKEN,
        project_name=project)

    repositories = json.loads(response.data['resources']['repositories'])

    return repositories
