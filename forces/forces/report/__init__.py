"""Fluid Forces report module"""
# Standard imports
import asyncio
from typing import AsyncGenerator, Any, Dict, List, Union
from timeit import default_timer as timer

# 3d Impors

# Local imports
from forces import get_verbose_level
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
    get_vulnerabilities,
)


async def vulns_generator(project: str) -> AsyncGenerator[Dict[
        str, Union[str, List[Dict[str, Dict[str, Any]]]]], None]:
    """
    Returns a generator with all the vulnerabilities of a project.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    findings = await get_findings(project)
    vulns_tasks = [get_vulnerabilities(fin) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_tasks):
        for vuln in await vulnerabilities:
            yield vuln


async def generate_report(project: str) -> Dict[str, Any]:
    """
    Generate a project vulnerability report.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    _start_time = timer()
    _summary_dict = {'open': 0, 'closed': 0, 'accepted': 0}
    raw_report: Dict[str, List[Any]] = {'findings': list()}
    findings_dict: Dict[str, Dict[str, Any]] = dict()

    finding_tasks = [
        get_finding(fin)
        for fin in await get_findings(project)
    ]
    for _find in asyncio.as_completed(finding_tasks):
        find: Dict[str, str] = await _find
        findings_dict[find['id']] = find
        findings_dict[find['id']].update({
            'open': 0,
            'closed': 0,
            'accepted': 0
        })

        if get_verbose_level() > 1:
            findings_dict[find['id']]['vulnerabilities'] = list()

    async for vuln in vulns_generator(project):
        find_id: str = vuln['findingId']  # type: ignore
        state = vuln['currentState']
        if state == 'closed':
            _summary_dict['closed'] += 1
            findings_dict[find_id]['closed'] += 1
        elif state == 'accepted':
            _summary_dict['accepted'] += 1
            findings_dict[find_id]['accepted'] += 1
        elif state == 'open':
            _summary_dict['open'] += 1
            findings_dict[find_id]['open'] += 1
        if get_verbose_level() == 1:
            continue
        vulnerability = {
            'type': 'SAST' if vuln['vulnType'] == 'lines' else 'DAST',
            'where': vuln['where'],
            'state': vuln['currentState']
        }

        if get_verbose_level() == 2 and vulnerability['state'] in ('accepted',
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


async def _proccess(project: str) -> Dict[str, Any]:
    report = await generate_report(project)
    return report


def process(project: str) -> Dict[str, Any]:
    """Process a report."""
    return asyncio.run(_proccess(project))
