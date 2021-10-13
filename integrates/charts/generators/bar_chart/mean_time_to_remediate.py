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
from groups import (
    domain as groups_domain,
)
from typing import (
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
            groups_domain.get_mean_remediate_severity_new(
                loaders, group, 9, 10, min_date
            ),
            groups_domain.get_mean_remediate_severity_new(
                loaders, group, 7, 8.9, min_date
            ),
            groups_domain.get_mean_remediate_severity_new(
                loaders, group, 4, 6.9, min_date
            ),
            groups_domain.get_mean_remediate_severity_new(
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
    groups: List[str], loaders: Dataloaders, min_date: Optional[date] = None
) -> Remediate:
    groups_data: Tuple[Remediate, ...] = await collect(
        [
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ]
    )

    return sum_mttr_many_groups(groups_data=groups_data)


def format_data(data: Remediate) -> dict:
    translations: Dict[str, str] = {
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
                categories=[value for _, value in translations.items()],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Calendar days per severity (less is better)",
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
