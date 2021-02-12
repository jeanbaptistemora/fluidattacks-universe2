# Standard library

# Third party libraries
from aioextensions import run

from backend.api import get_new_context
from frozendict import frozendict

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    context = get_new_context()
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings
    data: dict = {
        'nodes': set(),
        'links': set(),
    }
    group_findings = await group_findings_loader.load(group)
    for finding in group_findings:
        finding_id = finding['finding_id']
        finding_title = finding['title']
        finding_cvss = finding['cvss_temporal']

        finding_vulns = await finding_vulns_loader.load(finding_id)
        for vulnerability in finding_vulns:
            source = utils.get_vulnerability_source(vulnerability)
            target = f'{finding_title} {source}'

            data['nodes'].add(frozendict({
                'group': 'source',
                'id': source,
            }))
            data['nodes'].add(frozendict({
                'group': 'target',
                'id': target,
                'score': float(finding_cvss),
                'isOpen': vulnerability['current_state'] == 'open',
                'display': f'[{finding_cvss}] {finding_title}',
            }))
            data['links'].add(frozendict({
                'source': source,
                'target': target,
            }))

    return data


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    run(generate_all())
