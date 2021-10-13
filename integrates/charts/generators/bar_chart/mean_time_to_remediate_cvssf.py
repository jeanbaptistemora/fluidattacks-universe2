from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils import (
    Remediate,
    sum_mttr_many_groups,
)
from charts.generators.bar_chart.utils_mean_time_to_remediate import (
    generate_all,
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
            groups_domain.get_mean_remediate_severity_cvssf_new(
                loaders, group, Decimal("9"), Decimal("10"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf_new(
                loaders, group, Decimal("7"), Decimal("8.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf_new(
                loaders, group, Decimal("4"), Decimal("6.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf_new(
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
        [
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ]
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
                    text="Days per Severity",
                    position="inner-top",
                ),
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
        )
    )
