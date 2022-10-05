# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from groups.domain import (
    get_mean_remediate_non_treated_severity_cvssf,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    critical, high, medium, low = await collect(
        [
            get_mean_remediate_non_treated_severity_cvssf(
                loaders, group, Decimal("9"), Decimal("10"), min_date
            ),
            get_mean_remediate_non_treated_severity_cvssf(
                loaders, group, Decimal("7"), Decimal("8.9"), min_date
            ),
            get_mean_remediate_non_treated_severity_cvssf(
                loaders, group, Decimal("4"), Decimal("6.9"), min_date
            ),
            get_mean_remediate_non_treated_severity_cvssf(
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
    groups: List[str], loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    groups_data: Tuple[Remediate, ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ),
        workers=24,
    )

    return sum_mttr_many_groups(groups_data=groups_data)


def format_data(data: Remediate) -> Dict[str, Any]:
    translations: Dict[str, str] = {
        "critical_severity": "Critical Severity",
        "high_severity": "High Severity",
        "medium_severity": "Medium Severity",
        "low_severity": "Low Severity",
    }
    return dict(
        data=dict(
            columns=[
                [
                    "Mean time to remediate",
                    *[
                        Decimal(getattr(data, key)).to_integral_exact(
                            rounding=ROUND_CEILING
                        )
                        for key, _ in translations.items()
                    ],
                ]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            labels=True,
            type="bar",
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
                ),
                label=dict(
                    text="Days per Exposure",
                    position="inner-top",
                ),
            ),
        ),
        legend=dict(
            show=False,
        ),
        tooltip=dict(
            show=False,
        ),
        bar=dict(
            width=dict(
                ratio=BAR_RATIO_WIDTH,
            ),
        ),
        barChartYTickFormat=True,
    )


if __name__ == "__main__":
    run(
        generate_all(
            format_data=format_data,
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            alternative="Mean time to remediate non treated (cvssf) in days",
        )
    )
