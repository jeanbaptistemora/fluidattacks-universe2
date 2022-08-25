from db_model.forces.types import (
    ForcesExecution,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)


def format_forces_item(execution: ForcesExecution) -> Item:
    return {
        "id": execution.id,
        "group_name": execution.group_name,
        "execution_date": execution.execution_date,
        "commit": execution.commit,
        "repo": execution.repo,
        "branch": execution.branch,
        "kind": execution.kind,
        "exit_code": execution.exit_code,
        "strictness": execution.strictness,
        "git_origin": execution.origin,
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
