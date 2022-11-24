from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    OTHER,
)
from charts.generators.pie_chart.utils import (
    generate_all,
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
    NamedTuple,
)


class AssignedVulnerabilities(NamedTuple):
    assigned: int
    not_assigned: int


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> AssignedVulnerabilities:
    loaders: Dataloaders = get_new_context()
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        finding_ids
    )

    return AssignedVulnerabilities(
        assigned=sum(
            [
                1
                for vulnerability in vulnerabilities
                if vulnerability.state.status == VulnerabilityStateStatus.OPEN
                and vulnerability.treatment
                and vulnerability.treatment.assigned
            ]
        ),
        not_assigned=sum(
            [
                1
                for vulnerability in vulnerabilities
                if vulnerability.state.status == VulnerabilityStateStatus.OPEN
                and (
                    (
                        vulnerability.treatment
                        and not vulnerability.treatment.assigned
                    )
                    or vulnerability.treatment is None
                )
            ]
        ),
    )


async def get_data_many_groups(
    groups: tuple[str, ...]
) -> AssignedVulnerabilities:
    groups_data: tuple[AssignedVulnerabilities, ...] = await collect(
        map(get_data_one_group, groups), workers=32
    )

    return AssignedVulnerabilities(
        assigned=sum([group.assigned for group in groups_data]),
        not_assigned=sum([group.not_assigned for group in groups_data]),
    )


def format_data(data: AssignedVulnerabilities) -> dict:

    return {
        "data": {
            "columns": [
                ["Assigned", data.assigned],
                ["Not assigned", data.not_assigned],
            ],
            "type": "pie",
            "colors": {
                "Assigned": OTHER.more_agressive,
                "Not assigned": OTHER.more_passive,
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
            header=["Assignment", "Occurrences"],
        )
    )
