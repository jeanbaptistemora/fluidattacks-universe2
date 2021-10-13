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
from charts.generators.pie_chart.utils import (
    generate_all,
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
    get_severity_score,
)
from typing import (
    Counter,
    Dict,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: Tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
        for finding in group_findings
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


async def get_data_many_groups(groups: Tuple[str, ...]) -> Counter[str]:
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


if __name__ == "__main__":
    run(
        generate_all(
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            format_document=format_data,
        )
    )
