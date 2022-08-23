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


def format_explotability(execution: Item) -> Item:
    for _, vulnerabilities in execution.get("vulnerabilities", {}).items():
        if not isinstance(vulnerabilities, list):
            continue

        for vuln in vulnerabilities:
            explot = {
                "0.91": "Unproven",
                "0.94": "Proof of concept",
                "0.97": "Functional",
                "1.0": "High",
                "1": "High",
            }.get(str(vuln.get("exploitability", 0)), "-")
            vuln["exploitability"] = explot
    return execution


def format_forces_to_resolve(execution: ForcesExecution) -> Item:
    item = {
        "execution_id": execution.id,
        "group_name": execution.group_name,
        "date": execution.date,
        "git_commit": execution.commit,
        "git_repo": execution.repo,
        "git_branch": execution.branch,
        "kind": execution.kind,
        "exit_code": execution.exit_code,
        "strictness": execution.strictness,
        "git_origin": execution.origin,
        "grace_period": execution.grace_period,
        "severity_threshold": execution.severity_threshold,
        "vulnerabilities": {
            "num_of_accepted_vulnerabilities": (
                execution.vulnerabilities.num_of_accepted_vulnerabilities
            ),
            "num_of_open_vulnerabilities": (
                execution.vulnerabilities.num_of_open_vulnerabilities
            ),
            "num_of_closed_vulnerabilities": (
                execution.vulnerabilities.num_of_closed_vulnerabilities
            ),
            "open": list(execution.vulnerabilities.open)
            if execution.vulnerabilities.open
            else [],
            "closed": list(execution.vulnerabilities.closed)
            if execution.vulnerabilities.closed
            else [],
            "accepted": list(execution.vulnerabilities.accepted)
            if execution.vulnerabilities.accepted
            else [],
        },
    }
    return format_explotability(item)
