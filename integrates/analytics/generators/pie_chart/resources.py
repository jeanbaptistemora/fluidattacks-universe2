# Standard library
from typing import (
    Any,
    Dict,
    List,
    NamedTuple
)

# Third party libraries
from aioextensions import run
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.typing import GitRoot


# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    OTHER,
)


Resources = NamedTuple('Resources', [
    ('environments', List[str]),
    ('repositories', List[GitRoot]),
])


def format_data(data: Resources) -> Dict[str, Any]:
    return {
        'data': {
            'columns': [
                ['Repositories', len(data.repositories)],
                ['Environments', len(data.environments)],
            ],
            'type': 'pie',
            'colors': {
                'Repositories': OTHER.more_passive,
                'Environments': OTHER.more_agressive,
            },
        },
        'legend': {
            'position': 'right',
        },
        'pie': {
            'label': {
                'show': True,
            },
        },
    }


def format_resources(roots: List[GitRoot]) -> Resources:
    return Resources(
        environments=[
            env_url
            for root in roots
            for env_url in root.environment_urls
        ],
        repositories=roots,
    )


async def generate_all() -> None:
    async for org_id, org_name, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        loader = GroupRootsLoader()
        grouped_roots = [
            [
                root
                for root in group_roots
                if isinstance(root, GitRoot)
                and root.state == 'ACTIVE'
            ]
            for group_roots in await loader.load_many(org_groups)
        ]
        org_roots = [
            root
            for group_roots in grouped_roots
            for root in group_roots
        ]

        utils.json_dump(
            document=format_data(
                data=format_resources(org_roots)
            ),
            entity='organization',
            subject=org_id,
        )

        for group_name, group_roots in zip(org_groups, grouped_roots):
            utils.json_dump(
                document=format_data(
                    data=format_resources(group_roots),
                ),
                entity='group',
                subject=group_name,
            )

        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            set_groups = set(groups)
            portfolio_roots = [
                root for group_roots in grouped_roots
                for group_name, root in zip(org_groups, group_roots)
                if group_name in set_groups
            ]
            utils.json_dump(
                document=format_data(
                    data=format_resources(portfolio_roots)
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
