from datetime import (
    datetime,
)
from db_model.forces.types import (
    ExecutionVulnerabilities,
    ExploitResult,
    ForcesExecution,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from decimal import (
    Decimal,
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
        num_of_vulns_in_exploits=vulenrabilities.get(
            "num_of_vulnerabilities_in_exploits"
        ),
        num_of_vulns_in_integrates_exploits=vulenrabilities.get(
            "num_of_vulnerabilities_in_integrates_exploits"
        ),
        num_of_vulns_in_accepted_exploits=vulenrabilities.get(
            "num_of_vulnerabilities_in_accepted_exploits"
        ),
    )


def format_forces_execution(item: Item) -> ForcesExecution:
    return ForcesExecution(
        id=item["id"],
        group_name=item["group_name"],
        execution_date=datetime.fromisoformat(item["execution_date"]),
        commit=item["commit"],
        repo=item["repo"],
        branch=item["branch"],
        kind=item["kind"],
        exit_code=item["exit_code"],
        strictness=item["strictness"],
        origin=item["origin"],
        grace_period=item["grace_period"] if item.get("grace_period") else 0,
        severity_threshold=Decimal(item["severity_threshold"])
        if item.get("severity_threshold")
        else Decimal("0.0"),
        vulnerabilities=format_forces_vulnerabilities(item["vulnerabilities"]),
    )


def format_forces_item(execution: ForcesExecution) -> Item:
    return {
        "id": execution.id,
        "group_name": execution.group_name,
        "execution_date": get_as_utc_iso_format(execution.execution_date),
        "commit": execution.commit,
        "repo": execution.repo,
        "branch": execution.branch,
        "kind": execution.kind,
        "exit_code": execution.exit_code,
        "strictness": execution.strictness,
        "origin": execution.origin,
        "grace_period": execution.grace_period
        if execution.grace_period
        else 0,
        "severity_threshold": execution.severity_threshold
        if execution.severity_threshold
        else Decimal("0.0"),
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
        },
    }
