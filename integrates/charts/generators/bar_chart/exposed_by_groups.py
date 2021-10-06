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
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score_new,
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
    finding_cvssf: Dict[str, Decimal] = {}
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
        finding_cvssf = {
            finding.id: utils.get_cvssf(
                get_severity_score_new(finding.severity)
            )
            for finding in group_findings_new
        }
    else:
        group_findings_data = await loaders.group_findings.load(group.lower())
        finding_ids = [
            finding["finding_id"] for finding in group_findings_data
        ]
        finding_cvssf = {
            str(finding["finding_id"]): utils.get_cvssf(
                Decimal(finding.get("cvss_temporal", "0.0")).quantize(
                    Decimal("0.1")
                )
            )
            for finding in group_findings_data
        }

    vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        if vulnerability["current_state"] == "open":
            counter.update(
                {
                    "open": Decimal(
                        finding_cvssf[str(vulnerability["finding_id"])]
                    ).quantize(Decimal("0.001"))
                }
            )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=Decimal(counter["open"]).quantize(Decimal("0.1")),
    )


async def get_data_many_groups(
    *,
    groups: Tuple[str, ...],
    loaders: Dataloaders,
) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(
        [get_data_one_group(group=group, loaders=loaders) for group in groups]
    )

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["Open Severity (CVSSF)"] + [group.value for group in data],
            ],
            colors={
                "Open Severity (CVSSF)": RISK.more_agressive,
            },
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
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
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
