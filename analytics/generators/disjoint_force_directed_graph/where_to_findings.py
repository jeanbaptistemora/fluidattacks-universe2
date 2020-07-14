# Standard library
import asyncio

# Third party libraries
from backend.domain import (
    finding as finding_domain,
    project as group_domain,
    vulnerability as vulnerability_domain,
)
from frozendict import frozendict

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    data: dict = {
        'nodes': set(),
        'links': set(),
    }

    for finding_id in group_domain.list_findings(group):
        finding = await finding_domain.get_finding(finding_id)
        finding_title = finding['finding']
        finding_cvss = finding['severityCvss']

        for vulnerability in (
            await vulnerability_domain.list_vulnerabilities_async([
                finding_id
            ])
        ):
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
    for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
