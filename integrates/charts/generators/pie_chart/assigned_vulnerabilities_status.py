from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.common import (
    format_csv_data,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
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
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from typing import (
    Counter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> Counter[VulnerabilityStateStatus]:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )

    return Counter(
        tuple(
            vulnerability.state.status
            for vulnerability in vulnerabilities
            if vulnerability.treatment and vulnerability.treatment.assigned
        )
    )


async def get_data_many_groups(
    *, groups: tuple[str, ...], loaders: Dataloaders
) -> Counter[VulnerabilityStateStatus]:
    groups_data: tuple[Counter[VulnerabilityStateStatus], ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(*, data: Counter[VulnerabilityStateStatus]) -> dict:

    return dict(
        data=dict(
            columns=[
                ["Open", data[VulnerabilityStateStatus.VULNERABLE]],
                ["Closed", data[VulnerabilityStateStatus.SAFE]],
            ],
            type="pie",
            colors=dict(
                Open=RISK.more_agressive,
                Closed=RISK.more_passive,
            ),
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    headers: list[str] = ["Status of assigned vulnerabilities", "Number"]
    async for group in iterate_groups():
        document = format_data(
            data=await get_data_one_group(group=group, loaders=loaders),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=headers),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(
                groups=org_groups, loaders=loaders
            ),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=headers),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=headers
                ),
            )


if __name__ == "__main__":
    run(generate_all())
