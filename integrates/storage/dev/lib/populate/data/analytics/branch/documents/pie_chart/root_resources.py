from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.common.colors import (
    OTHER,
)
from charts.generators.pie_chart.common import (
    format_csv_data,
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
    RootEnvironmentUrl,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    NamedTuple,
)

Resources = NamedTuple(
    "Resources",
    [
        ("environments", list[str]),
        ("repositories", list[GitRoot]),
    ],
)


def format_data(data: Resources) -> dict:
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


async def format_resources(
    loaders: Dataloaders, roots: list[GitRoot]
) -> Resources:
    root_urls: list[
        list[RootEnvironmentUrl]
    ] = await loaders.root_environment_urls.load_many(
        [root.id for root in roots]
    )

    return Resources(
        environments=list({url.url for urls in root_urls for url in urls}),
        repositories=roots,
    )


async def generate_all() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    headers: list[str] = ["Active resources", "Occurrences"]
    active_group_names: set[str] = set(
        sorted(await orgs_domain.get_all_active_group_names(loaders))
    )
    async for group in utils.iterate_groups():
        document = format_data(
            data=await format_resources(
                loaders,
                [
                    root
                    for root in await loaders.group_roots.load(group)
                    if isinstance(root, GitRoot)
                    and root.state.status == RootStatus.ACTIVE
                ],
            ),
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=headers),
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
            for group_roots in await loaders.group_roots.load_many(
                list(org_groups)
            )
        ]
        org_roots = [
            root for group_roots in grouped_roots for root in group_roots
        ]

        document = format_data(data=await format_resources(loaders, org_roots))
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=headers),
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
                list(valid_org_groups)
            )
        ]

        for group_name, group_roots in zip(valid_org_groups, grouped_roots):
            document = format_data(
                data=await format_resources(loaders, group_roots),
            )
            utils.json_dump(
                document=document,
                entity="group",
                subject=group_name,
                csv_document=format_csv_data(
                    document=document, header=headers
                ),
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
            document = format_data(
                data=await format_resources(loaders, portfolio_roots)
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=headers
                ),
            )


if __name__ == "__main__":
    run(generate_all())
