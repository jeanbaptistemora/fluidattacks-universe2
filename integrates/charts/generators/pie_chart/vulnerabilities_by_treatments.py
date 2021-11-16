from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    OTHER,
)
from charts.generators.pie_chart.utils import (
    generate_all,
    MAX_GROUPS_DISPLAYED,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from operator import (
    itemgetter,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
)


async def get_treatment_changes(
    loaders: Dataloaders, vuln: Vulnerability
) -> int:
    historic: Tuple[
        VulnerabilityTreatment, ...
    ] = await loaders.vulnerability_historic_treatment.load(vuln.id)

    return len(historic)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    loaders = get_new_context()
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities = await loaders.finding_vulns_nzr_typed.load_many_chained(
        finding_ids
    )
    treatment_changes = await collect(
        tuple(
            get_treatment_changes(loaders, vulnerability)
            for vulnerability in vulnerabilities
        ),
        workers=16,
    )

    return Counter(filter(None, treatment_changes))


async def get_data_many_groups(groups: Tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> Dict[str, Any]:
    treatments_data: List[Tuple[str, int]] = counters.most_common()
    data = treatments_data[:MAX_GROUPS_DISPLAYED] + (
        [
            (
                "others",
                sum(
                    map(itemgetter(1), treatments_data[MAX_GROUPS_DISPLAYED:])
                ),
            )
        ]
        if len(treatments_data) > MAX_GROUPS_DISPLAYED
        else []
    )

    return {
        "data": {
            "columns": [
                [treatment_change, value] for treatment_change, value in data
            ],
            "type": "pie",
            "colors": {
                treatment_change[0]: column
                for treatment_change, column in zip(data, OTHER)
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
