from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    Benchmarking,
    generate_all_mttr_benchmarking,
    get_vulnerability_reattacks,
    get_vulnerability_reattacks_date,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date as datetype,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from groups.domain import (
    get_mean_remediate_cvssf_new,
)
from typing import (
    Optional,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: Optional[datetype] = None
) -> Benchmarking:
    group_findings_new: Tuple[
        Finding, ...
    ] = await loaders.group_findings_new.load(group.lower())
    vulnerabilities = await loaders.finding_vulns.load_many_chained(
        [finding.id for finding in group_findings_new]
    )

    if min_date:
        number_of_reattacks: int = sum(
            get_vulnerability_reattacks_date(
                vulnerability=vulnerability, min_date=min_date
            )
            for vulnerability in vulnerabilities
        )
    else:
        number_of_reattacks = sum(
            get_vulnerability_reattacks(vulnerability=vulnerability)
            for vulnerability in vulnerabilities
        )

    mttr: Decimal = await get_mean_remediate_cvssf_new(
        loaders, group.lower(), min_date=min_date
    )

    return Benchmarking(
        is_valid=number_of_reattacks > 10,
        subject=group.lower(),
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


if __name__ == "__main__":
    run(
        generate_all_mttr_benchmarking(
            get_data_one_group=get_data_one_group,
        )
    )
