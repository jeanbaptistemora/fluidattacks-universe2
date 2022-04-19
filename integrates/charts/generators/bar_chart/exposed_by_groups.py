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
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
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
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from operator import (
    attrgetter,
)
from typing import (
    Counter,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
        for finding in group_findings
    }

    vulnerabilities = (
        await loaders.finding_vulnerabilities_nzr.load_many_chained(
            finding_ids
        )
    )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        if vulnerability.state.status == VulnerabilityStateStatus.OPEN:
            counter.update(
                {
                    "open": Decimal(
                        finding_cvssf[vulnerability.finding_id]
                    ).quantize(Decimal("0.001"))
                }
            )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=utils.format_cvssf(Decimal(counter["open"])),
    )


async def get_data_many_groups(
    *,
    groups: Tuple[str, ...],
    loaders: Dataloaders,
) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["Open Severity"]
                + [utils.format_cvssf_log(group.value) for group in data],
            ],
            colors={
                "Open Severity": RISK.more_agressive,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[group.group_name for group in data],
                type="category",
                tick=dict(
                    rotate=utils.TICK_ROTATION,
                    multiline=False,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="inner-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        maxValue=format_max_value(
            [(group.group_name, Decimal(group.value)) for group in data]
        ),
        maxValueLog=format_max_value(
            [
                (
                    group.group_name,
                    utils.format_cvssf_log(Decimal(group.value)),
                )
                for group in data
            ]
        ),
        originalValues=[
            utils.format_cvssf(Decimal(value)) for _, value in data
        ],
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(
                    groups=org_groups, loaders=loaders
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(
                        groups=tuple(groups), loaders=loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
