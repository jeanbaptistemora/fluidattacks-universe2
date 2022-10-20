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
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
from groups.domain import (
    get_mean_remediate_non_treated_severity_cvssf,
)
from newutils.vulnerabilities import (
    is_accepted_undefined_vulnerability,
)
from typing import (
    Optional,
)


async def get_historic_verification(
    loaders: Dataloaders, vulnerability_id: str
) -> tuple[VulnerabilityVerification, ...]:
    return await loaders.vulnerability_historic_verification.load(
        vulnerability_id
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: Optional[datetype]
) -> Benchmarking:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    vulnerabilities_excluding_permanently_accepted: tuple[str, ...] = tuple(
        vulnerability.id
        for vulnerability in vulnerabilities
        if not is_accepted_undefined_vulnerability(vulnerability)
    )

    historics_verifications: tuple[
        tuple[VulnerabilityVerification, ...], ...
    ] = await collect(
        tuple(
            get_historic_verification(loaders, vulnerability)
            for vulnerability in vulnerabilities_excluding_permanently_accepted
        ),
        workers=32,
    )

    if min_date:
        number_of_reattacks: int = sum(
            get_vulnerability_reattacks_date(
                historic_verification=historic, min_date=min_date
            )
            for historic in historics_verifications
        )
    else:
        number_of_reattacks = sum(
            get_vulnerability_reattacks(historic_verification=historic)
            for historic in historics_verifications
        )

    mttr: Decimal = await get_mean_remediate_non_treated_severity_cvssf(
        loaders,
        group.lower(),
        Decimal("0.0"),
        Decimal("10.0"),
        min_date=min_date,
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
            alternative=(
                "Mean time to remediate non treated per exposure benchmarking"
            ),
        )
    )
