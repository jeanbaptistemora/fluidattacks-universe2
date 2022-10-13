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
from charts import (
    utils,
)
from charts.generators.bar_chart.utils import (
    LIMIT,
)
from charts.generators.stacked_bar_chart import (  # type: ignore
    format_csv_data,
)
from charts.generators.stacked_bar_chart.utils import (
    AssignedFormatted,
    format_stacked_vulnerabilities_data,
)
from collections import (
    defaultdict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Counter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> dict[str, list[Vulnerability]]:
    loaders: Dataloaders = get_new_context()
    assigned: dict[str, list[Vulnerability]] = defaultdict(list)
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        finding_ids
    )

    for vulnerability in vulnerabilities:
        if vulnerability.treatment and vulnerability.treatment.assigned:
            assigned[vulnerability.treatment.assigned].append(vulnerability)

    return assigned


async def get_data_many_groups(
    groups: tuple[str, ...],
) -> dict[str, list[Vulnerability]]:
    groups_data: tuple[dict[str, list[Vulnerability]], ...] = await collect(
        map(get_data_one_group, groups), workers=32
    )
    assigned: dict[str, list[Vulnerability]] = defaultdict(list)

    for group in groups_data:
        for user, vulnerabilities in group.items():
            assigned[user].extend(vulnerabilities)

    return assigned


def format_assigned(
    user: str, vulnerabilities: list[Vulnerability]
) -> AssignedFormatted:
    status: Counter[str] = Counter(
        vulnerability.state.status for vulnerability in vulnerabilities
    )

    treatment: Counter[str] = Counter(
        vulnerability.treatment.status  # type: ignore
        for vulnerability in vulnerabilities
        if vulnerability.state.status == VulnerabilityStateStatus.OPEN
        and vulnerability.treatment.status  # type: ignore
        in {
            VulnerabilityTreatmentStatus.ACCEPTED,
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        }
    )

    remaining_open: Decimal = Decimal(
        status[VulnerabilityStateStatus.OPEN]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED]
    )

    return AssignedFormatted(
        accepted=treatment[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        closed_vulnerabilities=status[VulnerabilityStateStatus.CLOSED],
        open_vulnerabilities=status[VulnerabilityStateStatus.OPEN],
        remaining_open_vulnerabilities=remaining_open
        if remaining_open > Decimal("0.0")
        else Decimal("0.0"),
        user=user,
    )


def format_data(
    assigned_data: dict[str, list[Vulnerability]]
) -> dict[str, Any]:
    data: tuple[AssignedFormatted, ...] = tuple(
        format_assigned(user, vulnerabilities)
        for user, vulnerabilities in assigned_data.items()
    )
    limited_data = list(
        sorted(
            data,
            key=lambda x: (
                x.open_vulnerabilities
                / (x.closed_vulnerabilities + x.open_vulnerabilities)
                if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
                else 0
            ),
            reverse=True,
        )
    )[:LIMIT]

    return format_stacked_vulnerabilities_data(limited_data=limited_data)


async def generate_all() -> None:
    header: str = "User"
    async for group in utils.iterate_groups():
        document = format_data(assigned_data=await get_data_one_group(group))
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            assigned_data=await get_data_many_groups(org_groups)
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                assigned_data=await get_data_many_groups(groups)
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )


if __name__ == "__main__":
    run(generate_all())
