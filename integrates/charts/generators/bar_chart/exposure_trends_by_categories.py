from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    CRITERIA_VULNERABILITIES,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.text_box.utils_vulnerabilities_remediation import (
    had_state_by_then,
)
from charts.utils import (
    format_cvssf,
    format_cvssf_log,
    get_cvssf,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
    TICK_ROTATION,
)
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
)
from findings.domain.core import (
    get_severity_score,
)
from newutils.datetime import (
    get_now_minus_delta,
)
from ruamel import (
    yaml,
)
from typing import (
    Counter,
    NamedTuple,
)


class GroupInformation(NamedTuple):
    categories: dict[str, str]
    cvssf: dict[str, Decimal]
    vulnerabilities: tuple[Vulnerability, ...]


def get_categories() -> dict[str, str]:
    categories: dict[str, str] = {}
    with open(CRITERIA_VULNERABILITIES, encoding="utf-8") as handle:
        for code, data in yaml.safe_load(handle).items():
            categories[code] = data["category"]

    return categories


CATEGORIES: dict[str, str] = get_categories()


def get_category(*, finding_title: str, categories: dict[str, str]) -> str:
    with suppress(KeyError):
        return categories[finding_title.split(".")[0]]

    return ""


@alru_cache(maxsize=None, typed=True)
async def get_data_vulnerabilities(
    *,
    group: str,
    loaders: Dataloaders,
) -> GroupInformation:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    finding_cvssf: dict[str, Decimal] = {
        finding.id: get_cvssf(get_severity_score(finding.severity))
        for finding in findings
    }
    finding_category: dict[str, str] = {
        finding.id: get_category(
            finding_title=finding.title, categories=CATEGORIES
        )
        for finding in findings
    }

    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )

    return GroupInformation(
        categories=finding_category,
        cvssf=finding_cvssf,
        vulnerabilities=vulnerabilities,
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *,
    group: str,
    loaders: Dataloaders,
    days: int = 30,
) -> Counter[str]:
    last_day: datetime = get_now_minus_delta(days=days)
    data: GroupInformation = await get_data_vulnerabilities(
        group=group,
        loaders=loaders,
    )

    current_category: str
    counter: Counter[str] = Counter()

    for vulnerability in data.vulnerabilities:
        current_category = data.categories[vulnerability.finding_id]
        counter.update(
            {
                f"{current_category}/open": had_state_by_then(
                    last_day=last_day,
                    state=VulnerabilityStateStatus.OPEN,
                    vulnerabilities=[vulnerability],
                    findings_cvssf=data.cvssf,
                    sprint=True,
                ).quantize(Decimal("0.001")),
                f"{current_category}/closed": had_state_by_then(
                    last_day=last_day,
                    state=VulnerabilityStateStatus.CLOSED,
                    vulnerabilities=[vulnerability],
                    findings_cvssf=data.cvssf,
                    sprint=True,
                ).quantize(Decimal("0.001")),
            }
        )

    return counter


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> Counter[str]:
    groups_data: tuple[Counter[str], ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(data: Counter[str], categories: list[str]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["Exposure"]
                + [
                    format_cvssf_log(
                        Decimal(
                            data[f"{category}/open"]
                            - data[f"{category}/closed"]
                        )
                    )
                    for category in categories
                ],
            ],
            colors={
                "Exposure": RISK.more_agressive,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=categories,
                type="category",
                tick=dict(
                    rotate=TICK_ROTATION,
                    multiline=False,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="inner-top",
                ),
            ),
        ),
        maxValue=format_max_value(
            [
                (
                    category,
                    Decimal(
                        data[f"{category}/open"] - data[f"{category}/closed"]
                    ),
                )
                for category in categories
            ]
        ),
        maxValueLog=format_max_value(
            [
                (
                    category,
                    format_cvssf_log(
                        Decimal(
                            data[f"{category}/open"]
                            - data[f"{category}/closed"]
                        )
                    ),
                )
                for category in categories
            ]
        ),
        originalValues=[
            format_cvssf(
                Decimal(data[f"{category}/open"] - data[f"{category}/closed"])
            )
            for category in categories
        ],
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    unique_categories: list[str] = list(set(CATEGORIES.values()))
    async for group in iterate_groups():
        document = format_data(
            data=await get_data_one_group(group=group, loaders=loaders),
            categories=unique_categories,
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(
                groups=org_groups,
                loaders=loaders,
            ),
            categories=unique_categories,
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups),
                    loaders=loaders,
                ),
                categories=unique_categories,
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
