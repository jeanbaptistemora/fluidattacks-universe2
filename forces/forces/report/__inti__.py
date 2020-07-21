# Standard imports
import asyncio
from typing import Dict, Iterator, List, Union
from timeit import default_timer as timer

# 3d Impors
from gql import AIOHTTPTransport, Client
import oyaml as yaml

# Local imports
from forces import get_api_token
from forces import INTEGRATES_API_URL
from forces.apis.integrates import get_finding
from forces.apis.integrates import get_findings
from forces.apis.integrates import get_vulnerabilities


async def vulns_generator(
        client: Client, project: str
) -> Iterator[Union[str, Dict[str, Union[str, List[str]]]]]:
    """
    Returns a generator with all the vulnerabilities of a project.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    findings = await get_findings(client, project)
    vulns_tasks = [get_vulnerabilities(client, fin) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_tasks):
        for vuln in await vulnerabilities:
            yield vuln


async def generate_report(client: Client, project: str):
    """
    Generate a project vulnerability report.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    start_time = timer()
    _summary_dict = {'open': 0, 'closed': 0, 'accepted': 0}
    raw_report = {'findings': list()}
    findings_dict = dict()

    findings = await get_findings(client, project)
    finding_tasks = [get_finding(client, fin) for fin in findings]
    for find in asyncio.as_completed(finding_tasks):
        find = await find
        findings_dict[find['id']] = find
        findings_dict[find['id']]['vulnerabilities'] = list()

    async for vuln in vulns_generator(client, project):
        state = vuln['historicState'][-1]['state']
        if state == 'closed':
            _summary_dict['closed'] += 1
        elif state == 'accepted':
            _summary_dict['accepted'] += 1
        elif state == 'open':
            _summary_dict['open'] += 1
        vulnerability = {
            'type': 'SAST' if vuln['vulnType'] == 'lines' else 'DAST',
            'where': vuln['where'],
            'date': vuln['historicState'][-1]['date'],
            'state': vuln['historicState'][-1]['state']
        }
        findings_dict[vuln['findingId']]['vulnerabilities'].append(
            vulnerability)

    for find in findings_dict.values():
        raw_report['findings'].append(find)

    elapsed_time = timer() - start_time
    summary = {
        'summary': {
            'total': _summary_dict['open'] + _summary_dict['closed'] +
            _summary_dict['accepted'],
            **_summary_dict,
            'time': '%.4f seconds' % elapsed_time
        }
    }
    raw_report.update(summary)
    return raw_report


async def _proccess(project: str):
    transport = AIOHTTPTransport(
        url=INTEGRATES_API_URL,
        headers={
            'Authorization': f'Bearer {get_api_token()}'
        })
    async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
    ) as client:
        report = await generate_report(client, project)
        yaml_report = yaml.dump(report)
        with open('result.yml', 'w') as writer:
            writer.write(yaml_report)


def process(project: str) -> None:
    asyncio.run(_proccess(project))
