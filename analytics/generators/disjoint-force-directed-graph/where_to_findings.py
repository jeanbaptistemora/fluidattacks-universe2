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


def generate_one(group: str):
    data: dict = {
        'nodes': set(),
        'links': set(),
    }

    for finding_id in group_domain.list_findings(group):
        finding = finding_domain.get_finding(finding_id)

        data['nodes'].add(frozendict({
            'group': 'finding_id',
            'id': finding_id,
            'score': finding['severityCvss'],
        }))

        for vulnerability in vulnerability_domain.list_vulnerabilities([
            finding_id
        ]):
            root = utils.get_vulnerability_root(vulnerability)

            data['nodes'].add(frozendict({
                'group': 'where',
                'id': root,
            }))
            data['links'].add(frozendict({
                'source': root,
                'target': finding_id,
            }))

    return data


def generate_all():
    for group in utils.iterate_groups():
        data = generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    generate_all()
