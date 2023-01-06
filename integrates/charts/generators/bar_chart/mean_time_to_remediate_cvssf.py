from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    Remediate,
    sum_mttr_many_groups,
)
from charts.generators.bar_chart.utils_mean_time_to_remediate import (
    generate_all,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.common.utils import (
    BAR_RATIO_WIDTH,
    get_max_axis,
)
from dataloaders import (
    Dataloaders,
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
from typing import (
    Optional,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    critical, high, medium, low = await collect(
        [
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("9"), Decimal("10"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("7"), Decimal("8.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("4"), Decimal("6.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("0.1"), Decimal("3.9"), min_date
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
    groups: tuple[str, ...],
    loaders: Dataloaders,
    min_date: Optional[date] = None,
) -> Remediate:
    groups_data: tuple[Remediate, ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ),
        workers=24,
    )

    return sum_mttr_many_groups(groups_data=groups_data)


def format_data(data: Remediate) -> dict:
    translations: dict[str, str] = {
        "critical_severity": "Critical",
        "high_severity": "High",
        "medium_severity": "Medium",
        "low_severity": "Low",
    }
    values: list[Decimal] = [
        Decimal(getattr(data, key)).to_integral_exact(rounding=ROUND_CEILING)
        for key, _ in translations.items()
    ]
    max_value: Decimal = list(
        sorted(
            [abs(value) for value in values],
            reverse=True,
        )
    )[0]
    max_axis_value: Decimal = (
        get_max_axis(value=max_value)
        if max_value > Decimal("0.0")
        else Decimal("0.0")
    )

    return dict(
        data=dict(
            columns=[
                [
                    "Mean time to remediate",
                    *values,
                ]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            labels=True,
            type="bar",
        ),
        bar=dict(
            width=dict(
                ratio=BAR_RATIO_WIDTH,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[value for _, value in translations.items()],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                    top=0,
                ),
                label=dict(
                    text="Days",
                    position="inner-top",
                ),
                tick=dict(
                    count=5,
                ),
                **(
                    {}
                    if max_axis_value == Decimal("0.0")
                    else dict(max=max_axis_value)
                ),
            ),
        ),
        mttrCvssf=True,
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        legend=dict(
            show=False,
        ),
        tooltip=dict(
            show=False,
        ),
        barChartYTickFormat=True,
        hideXTickLine=True,
        hideYAxisLine=True,
    )


if __name__ == "__main__":
    run(
        generate_all(
            format_data=format_data,
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            alternative="Mean time to remediate (cvssf) in days",
        )
    )
