"""Fluid Forces report module"""
# Standard imports
import asyncio
from typing import (
    Any,
    Dict,
    List,
)
from timeit import default_timer as timer

# Third parties libraries
import oyaml as yaml

# Local imports
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
    vulns_generator,
)
from forces.utils.aio import (
    unblock,
)


def get_exploitability_measure(score: int) -> str:
    data = {'0.91': 'Unproven',
            '0.94': 'Proof of concept',
            '0.97': 'Functional',
            '1.0': 'High'}
    return data.get(str(score), '-')


async def create_findings_dict(project: str,
                               **kwargs: str) -> Dict[str, Dict[str, Any]]:
    """Returns a dictionary containing as key the findings of a project."""
    findings_dict: Dict[str, Dict[str, Any]] = dict()
    findings_futures = [
        get_finding(fin) for fin in await get_findings(project, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: Dict[str, Any] = await _find
        severity: Dict[str, Any] = find.pop('severity', dict())
        find['exploitability'] = severity.get('exploitability', 0)
        findings_dict[find['id']] = find
        findings_dict[find['id']].update({
            'open': 0,
            'closed': 0,
            'accepted': 0
        })
        findings_dict[find['id']]['vulnerabilities'] = list()
    return findings_dict


async def generate_report_log(report: Dict[str, Any],
                              verbose_level: int) -> str:
    for finding in report['findings']:
        explot = get_exploitability_measure(finding.get('exploitability', 0))
        finding['exploitability'] = explot
        for vuln in finding['vulnerabilities']:
            vuln['exploitability'] = explot
    if verbose_level == 1:
        for finding in report['findings']:
            finding.pop('vulnerabilities')
    elif verbose_level == 2:
        for finding in report['findings']:
            finding['vulnerabilities'] = [
                vuln for vuln in finding['vulnerabilities']
                if vuln['state'] == 'open'
            ]
    elif verbose_level == 3:
        for finding in report['findings']:
            finding['vulnerabilities'] = [
                vuln for vuln in finding['vulnerabilities']
                if vuln['state'] in ('open', 'closed')
            ]
    return await unblock(yaml.dump, report, allow_unicode=True)


async def generate_report(project: str, **kwargs: str) -> Dict[str, Any]:
    """
    Generate a project vulnerability report.

    :param project: Project Name.
    :param verbose_level: Level of detail of the report.
    """
    _start_time = timer()
    kind = kwargs.pop('kind', 'all')

    _summary_dict: Dict[str, Dict[str, int]] = {
        'open': {
            'total': 0
        },
        'closed': {
            'total': 0
        },
        'accepted': {
            'total': 0
        }
    }

    _summary_dict = _summary_dict if kind != 'all' else {
        key: {
            'DAST': 0,
            'SAST': 0,
            'total': 0
        }
        for key in _summary_dict
    }

    raw_report: Dict[str, List[Any]] = {'findings': list()}
    findings_dict = await create_findings_dict(project, **kwargs)

    async for vuln in vulns_generator(project):
        find_id: str = vuln['findingId']  # type: ignore
        state = vuln['currentState']

        vuln_type = 'SAST' if vuln['vulnType'] == 'lines' else 'DAST'
        if (kind == 'dynamic'
                and vuln_type == 'SAST') or (kind == 'static'
                                             and vuln_type == 'DAST'):
            continue

        for r_state in ('closed', 'accepted', 'open'):
            if state == r_state:
                _summary_dict[r_state]['total'] += 1
                if kind == 'all':
                    _summary_dict[r_state][
                        'DAST'] += 1 if vuln_type == 'DAST' else 0
                    _summary_dict[r_state][
                        'SAST'] += 1 if vuln_type == 'SAST' else 0
                findings_dict[find_id][r_state] += 1

        findings_dict[find_id]['vulnerabilities'].append({
            'type':
            vuln_type,
            'where':
            vuln['where'],
            'specific':
            vuln['specific'],
            'URL': ('https://integrates.fluidattacks.com/groups'
                    f'{project}/vulns/{vuln["findingId"]}'),
            'state':
            state,
            'exploitability':
            findings_dict[find_id]['exploitability']
        })

    for find in findings_dict.values():
        raw_report['findings'].append(find)

    summary = {
        'summary': {
            'total':
            _summary_dict['open']['total'] + _summary_dict['closed']['total'] +
            _summary_dict['accepted']['total'],
            **_summary_dict, 'time':
            '%.4f seconds' % (timer() - _start_time)
        }
    }
    raw_report.update(summary)  # type: ignore
    return raw_report
