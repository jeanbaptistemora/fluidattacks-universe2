# Standard library

# Third party libraries
from aioextensions import run
from backend.domain import (
    finding as finding_domain,
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
    findings = await finding_domain.list_findings([group])
    for finding_id in findings[0]:
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
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    run(generate_all())
