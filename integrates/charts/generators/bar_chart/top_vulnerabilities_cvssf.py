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
from context import (
    FI_API_STATUS,
)
from custom_types import (
    Finding,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding as FindingNew,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from itertools import (
    groupby,
)
from typing import (
    Counter,
    List,
    Tuple,
    Union,
)


def get_finding_severity(findings: List[Finding], finding_id: str) -> Decimal:
    return Decimal(
        next(
            finding
            for finding in findings
            if finding["finding_id"] == finding_id
        ).get("cvss_temporal", "0.0")
    ).quantize(Decimal("0.1"))


def get_finding_severity_new(
    findings: Tuple[FindingNew, ...], finding_id: str
) -> Decimal:
    return findings_domain.get_severity_score_new(
        next(
            finding for finding in findings if finding.id == finding_id
        ).severity
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str, loaders: Dataloaders) -> Counter[str]:
    if FI_API_STATUS == "migration":
        group_findings_new_loader = loaders.group_findings_new
        group_findings_new: Tuple[
            FindingNew, ...
        ] = await group_findings_new_loader.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
        finding_vulns = await loaders.finding_vulns_nzr.load_many(finding_ids)
        counter: Counter[str] = Counter(
            [
                f"{finding.id}/{finding.title}"
                for finding, vulnerabilities in zip(
                    group_findings_new, finding_vulns
                )
                for vulnerability in vulnerabilities
                if vulnerability["current_state"] == "open"
            ]
        )
        counter_tuple = counter.most_common()
        for key, value in counter_tuple:
            counter.update(
                {
                    key: Decimal(
                        utils.get_cvssf(
                            get_finding_severity_new(
                                group_findings_new, key.split("/")[0]
                            )
                        )
                        * value
                    ).quantize(Decimal("0.001"))
                    - value
                }
            )
    else:
        group_findings = await loaders.group_findings.load(group.lower())
        finding_ids = [finding["finding_id"] for finding in group_findings]
        finding_vulns = await loaders.finding_vulns_nzr.load_many(finding_ids)
        counter = Counter(
            [
                f'{finding["finding_id"]}/{finding["title"]}'
                for finding, vulnerabilities in zip(
                    group_findings, finding_vulns
                )
                for vulnerability in vulnerabilities
                if vulnerability["current_state"] == "open"
            ]
        )
        counter_tuple = counter.most_common()
        for key, value in counter_tuple:
            counter.update(
                {
                    key: Decimal(
                        utils.get_cvssf(
                            get_finding_severity(
                                group_findings, key.split("/")[0]
                            )
                        )
                        * value
                    ).quantize(Decimal("0.001"))
                    - value
                }
            )

    return counter


async def get_data_many_groups(
    groups: List[str], loaders: Dataloaders
) -> Counter[str]:
    groups_data = await collect(
        [get_data_one_group(group, loaders) for group in groups]
    )

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data: List[Tuple[str, int]] = counters.most_common()
    merged_data: List[List[Union[int, str]]] = []
    for axis, columns in groupby(
        sorted(data, key=lambda x: utils.get_finding_name([x[0]])),
        key=lambda x: utils.get_finding_name([x[0]]),
    ):
        merged_data.append([axis, sum([value for _, value in columns])])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)[:10]

    return dict(
        data=dict(
            columns=[
                [
                    "Open Severity (CVSSF)",
                    *[
                        Decimal(value).quantize(Decimal("0.1"))
                        for _, value in merged_data
                    ],
                ],
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
                categories=[
                    utils.get_finding_name([str(key)])
                    for key, _ in merged_data
                ],
                type="category",
                tick=dict(
                    outer=False,
                    rotate=12,
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
    loaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                counters=await get_data_one_group(group, loaders)
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups), loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(list(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
