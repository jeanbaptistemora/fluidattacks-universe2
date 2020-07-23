"""Fluid Forces report module"""
# Standard imports
import asyncio
from typing import (
    Any,
    Dict,
    List,
)
from timeit import default_timer as timer

# 3d Impors

# Local imports
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
    vulns_generator,
)


async def create_findings_dict(project: str,
                               verbose_level: int,
                               **kwargs: str) -> Dict[str, Dict[str, Any]]:
    """Returns a dictionary containing as key the findings of a project."""
    findings_dict: Dict[str, Dict[str, Any]] = dict()
    findings_futures = [
        get_finding(fin) for fin in await get_findings(project, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: Dict[str, str] = await _find
        findings_dict[find['id']] = find
        findings_dict[find['id']].update({
            'open': 0,
            'closed': 0,
            'accepted': 0
        })
        if verbose_level > 1:
            findings_dict[find['id']]['vulnerabilities'] = list()
    return findings_dict


async def generate_report(project: str,
                          verbose_level: int,
                          **kwargs: str) -> Dict[str, Any]:
    """
    Generate a project vulnerability report.

    :param project: Project Name.
    :param verbose_level: Level of detail of the report.
    """
    _start_time = timer()
    _summary_dict = {'open': 0, 'closed': 0, 'accepted': 0}
    raw_report: Dict[str, List[Any]] = {'findings': list()}
    findings_dict = await create_findings_dict(
        project, verbose_level, **kwargs)

    async for vuln in vulns_generator(project):
        find_id: str = vuln['findingId']  # type: ignore
        state = vuln['currentState']
        if state == 'open' and findings_dict[find_id]['state'] == 'accepted':
            state = 'accepted'

        if state == 'closed':
            _summary_dict['closed'] += 1
            findings_dict[find_id]['closed'] += 1
        elif state == 'accepted':
            _summary_dict['accepted'] += 1
            findings_dict[find_id]['accepted'] += 1
        elif state == 'open':
            _summary_dict['open'] += 1
            findings_dict[find_id]['open'] += 1
        if verbose_level == 1:
            continue
        vulnerability = {
            'type': 'SAST' if vuln['vulnType'] == 'lines' else 'DAST',
            'where': vuln['where'],
            'specific': ('https://fluidattacks.com/integrates/groups/'
                         f'{project}/findings/{vuln["findingId"]}'),
            'state': vuln['currentState']
        }

        if verbose_level == 2 and vulnerability['state'] in ('accepted',
                                                             'closed'):
            continue
        findings_dict[find_id]['vulnerabilities'].append(vulnerability)

    for find in findings_dict.values():
        raw_report['findings'].append(find)

    summary = {
        'summary': {
            'total': _summary_dict['open'] + _summary_dict['closed'] +
            _summary_dict['accepted'],
            **_summary_dict,
            'time': '%.4f seconds' % (timer() - _start_time)
        }
    }
    raw_report.update(summary)  # type: ignore
    return raw_report


def process(project: str, verbose_level: int) -> Dict[str, Any]:
    """Process a report."""
    async def _proccess() -> Dict[str, Any]:
        return await generate_report(project, verbose_level)
    return asyncio.run(_proccess())
