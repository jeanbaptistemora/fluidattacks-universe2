from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.colors import (
    RISK,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from statistics import (
    mean,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)

Remediate = NamedTuple(
    "Remediate",
    [
        ("critical_severity", Decimal),
        ("high_severity", Decimal),
        ("medium_severity", Decimal),
        ("low_severity", Decimal),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    critical, high, medium, low = await collect(
        [
            groups_domain.get_mean_remediate_severity(
                loaders, group, 9, 10, min_date
            ),
            groups_domain.get_mean_remediate_severity(
                loaders, group, 7, 8.9, min_date
            ),
            groups_domain.get_mean_remediate_severity(
                loaders, group, 4, 6.9, min_date
            ),
            groups_domain.get_mean_remediate_severity(
                loaders, group, 0.1, 3.9, min_date
            ),
        ]
    )

    return Remediate(
        critical_severity=critical,
        high_severity=high,
        medium_severity=medium,
        low_severity=low,
    )


async def get_data_many_groups(
    *, groups: List[str], loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    groups_data = await collect(
        [
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ]
    )

    return Remediate(
        critical_severity=Decimal(
            mean([group.critical_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING),
        high_severity=Decimal(
            mean([group.high_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING),
        medium_severity=Decimal(
            mean([group.medium_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING),
        low_severity=Decimal(
            mean([group.low_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING),
    )


def format_data(data: Remediate) -> dict:
    translations = {
        "critical_severity": "Critical Severity",
        "high_severity": "High Severity",
        "medium_severity": "Medium Severity",
        "low_severity": "Low Severity",
    }
    return dict(
        data=dict(
            columns=[
                ["Mean time to remediate"]
                + [getattr(data, column) for column in translations]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            type="bar",
        ),
        axis=dict(
            x=dict(
                categories=[translations[column] for column in translations],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    list_days: List[int] = [30, 90]
    dates: List[date] = [
        datetime_utils.get_now_minus_delta(days=list_days[0]).date(),
        datetime_utils.get_now_minus_delta(days=list_days[1]).date(),
    ]
    for days, min_date in zip([None, *list_days], [None, *dates]):
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_data(
                    data=await get_data_one_group(
                        group=group, loaders=loaders, min_date=min_date
                    ),
                ),
                entity="group",
                subject=f"{group}_{days}" if days else group,
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            if org_groups:
                utils.json_dump(
                    document=format_data(
                        data=await get_data_many_groups(
                            groups=list(org_groups),
                            loaders=loaders,
                            min_date=min_date,
                        ),
                    ),
                    entity="organization",
                    subject=f"{org_id}_{days}" if days else org_id,
                )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                if groups:
                    utils.json_dump(
                        document=format_data(
                            data=await get_data_many_groups(
                                groups=groups,
                                loaders=loaders,
                                min_date=min_date,
                            ),
                        ),
                        entity="portfolio",
                        subject=f"{org_id}PORTFOLIO#{portfolio}_{days}"
                        if days
                        else f"{org_id}PORTFOLIO#{portfolio}",
                    )


if __name__ == "__main__":
    run(generate_all())
