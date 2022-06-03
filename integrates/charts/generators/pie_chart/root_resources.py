from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.colors import (
    OTHER,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)

Resources = NamedTuple(
    "Resources",
    [
        ("environments", List[str]),
        ("repositories", List[GitRoot]),
    ],
)


def format_data(data: Resources) -> Dict[str, Any]:
    return {
        "data": {
            "columns": [
                ["Repositories", len(data.repositories)],
                ["Environments", len(data.environments)],
            ],
            "type": "pie",
            "colors": {
                "Repositories": OTHER.more_passive,
                "Environments": OTHER.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


def format_resources(roots: List[GitRoot]) -> Resources:
    return Resources(
        environments=[
            env_url
            for root in roots
            for env_url in root.state.environment_urls
        ],
        repositories=roots,
    )


async def generate_all() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    active_group_names: set[str] = set(
        sorted(await orgs_domain.get_all_active_group_names(loaders))
    )
    async for group in utils.iterate_groups():
        group_roots = await loaders.group_roots.load(group)
        utils.json_dump(
            document=format_data(
                data=format_resources(
                    [
                        root
                        for root in group_roots
                        if isinstance(root, GitRoot)
                        and root.state.status == RootStatus.ACTIVE
                    ]
                ),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, org_name, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        grouped_roots = [
            [
                root
                for root in group_roots
                if isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            ]
            for group_roots in await loaders.group_roots.load_many(org_groups)
        ]
        org_roots = [
            root for group_roots in grouped_roots for root in group_roots
        ]

        utils.json_dump(
            document=format_data(data=format_resources(org_roots)),
            entity="organization",
            subject=org_id,
        )

        all_org_groups = await orgs_domain.get_group_names(loaders, org_id)
        valid_org_groups = active_group_names.intersection(all_org_groups)
        grouped_roots = [
            [
                root
                for root in group_roots
                if isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            ]
            for group_roots in await loaders.group_roots.load_many(
                valid_org_groups
            )
        ]

        for group_name, group_roots in zip(valid_org_groups, grouped_roots):
            utils.json_dump(
                document=format_data(
                    data=format_resources(group_roots),
                ),
                entity="group",
                subject=group_name,
            )

        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            grouped_portfolios_roots = [
                [
                    root
                    for root in group_roots
                    if isinstance(root, GitRoot)
                    and root.state.status == RootStatus.ACTIVE
                ]
                for group_roots in await loaders.group_roots.load_many(
                    list(groups)
                )
            ]
            portfolio_roots = [
                root
                for group_roots in grouped_portfolios_roots
                for root in group_roots
            ]
            utils.json_dump(
                document=format_data(data=format_resources(portfolio_roots)),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
