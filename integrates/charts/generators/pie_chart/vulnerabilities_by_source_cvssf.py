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
    OTHER,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score_new,
)
from typing import (
    Counter,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings_new: Tuple[
        Finding, ...
    ] = await context.group_findings_new.load(group.lower())
    finding_ids = [finding.id for finding in group_findings_new]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score_new(finding.severity))
        for finding in group_findings_new
    }

    vulnerabilities = await context.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        counter.update(
            {
                str(vulnerability["vuln_type"]): Decimal(
                    finding_cvssf[str(vulnerability["finding_id"])]
                ).quantize(Decimal("0.001"))
            }
        )

    return counter


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> dict:
    translations = {
        "inputs": "app",
        "lines": "code",
        "ports": "infra",
    }

    return {
        "data": {
            "columns": [
                [value, counters[key]] for key, value in translations.items()
            ],
            "type": "pie",
            "colors": {
                "app": OTHER.more_passive,
                "code": OTHER.neutral,
                "infra": OTHER.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(counters=await get_data_one_group(group)),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups)),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
