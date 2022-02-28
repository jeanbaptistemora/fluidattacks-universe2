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
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from typing import (
    Any,
    Dict,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group_name: str, loaders: Dataloaders) -> Decimal:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name.lower()
    )
    findings_ids: Tuple[str, ...] = tuple(
        finding.id for finding in group_findings
    )
    finding_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many(findings_ids)

    counter: Decimal = Decimal("0.0")
    for finding, vulnerabilities in zip(group_findings, finding_vulns):
        for vulnerability in vulnerabilities:
            if vulnerability.state.status == VulnerabilityStateStatus.OPEN:
                if finding.min_time_to_remediate:
                    counter += Decimal(finding.min_time_to_remediate)
                else:
                    counter += Decimal("60.0")

    minutes_days: Decimal = Decimal("24.0") * Decimal("60.0")

    return Decimal(counter / minutes_days).quantize(Decimal("0.001"))


async def get_data_many_groups(
    groups: Tuple[str, ...], loaders: Dataloaders
) -> Decimal:

    groups_data: Tuple[Decimal, ...] = await collect(
        tuple(get_data_one_group(group, loaders) for group in groups),
        workers=32,
    )

    return Decimal(sum(group for group in groups_data))


def format_data(days: Decimal) -> Dict[str, Any]:

    return {
        "fontSizeRatio": 0.5,
        "text": days.to_integral_exact(rounding=ROUND_CEILING),
    }


async def generate_all() -> None:

    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                days=await get_data_one_group(group, loaders),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                days=await get_data_many_groups(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    days=await get_data_many_groups(tuple(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
