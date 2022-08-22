from db_model.forces.types import (
    ForcesExecution,
    ForcesVulnerabilities,
)
from dynamodb.types import (
    Item,
)


def format_forces_vulnerabilities(
    vulenrabilities: Item,
) -> ForcesVulnerabilities:
    return ForcesVulnerabilities(
        num_of_accepted_vulnerabilities=int(
            vulenrabilities["num_of_accepted_vulnerabilities"]
        ),
        num_of_open_vulnerabilities=int(
            vulenrabilities["num_of_open_vulnerabilities"]
        ),
        num_of_closed_vulnerabilities=int(
            vulenrabilities["num_of_closed_vulnerabilities"]
        ),
    )


def format_forces(item: Item) -> ForcesExecution:
    return ForcesExecution(
        id=item["execution_id"],
        group_name=item["group_name"],
        date=item["date"],
        commit=item["git_commit"],
        repo=item["git_repo"],
        branch=item["git_branch"],
        kind=item["kind"],
        exit_code=item["exit_code"],
        strictness=item["strictness"],
        origin=item["git_origin"],
        grace_period=int(item["grace_period"]),
        severity_threshold=int(item["severity_threshold"]),
        vulnerabilities=format_forces_vulnerabilities(item["vulnerabilities"]),
    )
