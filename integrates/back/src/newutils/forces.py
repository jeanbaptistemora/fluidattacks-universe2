from db_model.forces.types import (
    ExecutionVulnerabilities,
    ExploitResult,
    ForcesExecution,
)
from dynamodb.types import (
    Item,
)


def format_exploit_result(result: list[Item]) -> list[ExploitResult]:
    exploit = [
        ExploitResult(
            exploitability=item["exploitability"],
            kind=item["kind"],
            state=item["state"],
            where=item["where"],
            who=item["who"],
        )
        for item in result
    ]
    return exploit


def format_forces_vulnerabilities(
    vulenrabilities: Item,
) -> ExecutionVulnerabilities:
    return ExecutionVulnerabilities(
        num_of_accepted_vulnerabilities=int(
            vulenrabilities["num_of_accepted_vulnerabilities"]
        ),
        num_of_open_vulnerabilities=int(
            vulenrabilities["num_of_open_vulnerabilities"]
        ),
        num_of_closed_vulnerabilities=int(
            vulenrabilities["num_of_closed_vulnerabilities"]
        ),
        open=format_exploit_result(vulenrabilities["open"])
        if vulenrabilities.get("open")
        else [],
        closed=format_exploit_result(vulenrabilities["closed"])
        if vulenrabilities.get("closed")
        else [],
        accepted=format_exploit_result(vulenrabilities["accepted"])
        if vulenrabilities.get("accepted")
        else [],
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
