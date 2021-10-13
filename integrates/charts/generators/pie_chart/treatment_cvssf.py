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
    TREATMENT,
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
    NamedTuple,
    Tuple,
)

Treatment = NamedTuple(
    "Treatment",
    [
        ("acceptedUndefined", int),
        ("accepted", int),
        ("inProgress", int),
        ("undefined", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Treatment:
    loaders = get_new_context()
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
        for finding in group_findings
    }

    vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    treatment: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        treatment.update(
            {
                str(
                    vulnerability["historic_treatment"][-1]["treatment"]
                ): Decimal(
                    finding_cvssf[str(vulnerability["finding_id"])]
                ).quantize(
                    Decimal("0.001")
                )
            }
        )

    return Treatment(
        acceptedUndefined=treatment["ACCEPTED_UNDEFINED"],
        accepted=treatment["ACCEPTED"],
        inProgress=treatment["IN PROGRESS"],
        undefined=treatment["NEW"],
    )


async def get_data_many_groups(groups: Tuple[str, ...]) -> Treatment:
    groups_data: Tuple[Treatment, ...] = await collect(
        map(get_data_one_group, groups)
    )

    return Treatment(
        acceptedUndefined=sum(
            [group.acceptedUndefined for group in groups_data]
        ),
        accepted=sum([group.accepted for group in groups_data]),
        inProgress=sum([group.inProgress for group in groups_data]),
        undefined=sum([group.undefined for group in groups_data]),
    )


def format_data(data: Treatment) -> dict:
    translations: Dict[str, str] = {
        "acceptedUndefined": "Permanently accepted",
        "accepted": "Temporarily Accepted",
        "inProgress": "In Progress",
        "undefined": "Not defined",
    }

    return {
        "data": {
            "columns": [
                [value, str(getattr(data, key))]
                for key, value in translations.items()
            ],
            "type": "pie",
            "colors": {
                "Permanently accepted": TREATMENT.more_passive,
                "Temporarily Accepted": TREATMENT.passive,
                "In Progress": TREATMENT.neutral,
                "Not defined": TREATMENT.more_agressive,
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
