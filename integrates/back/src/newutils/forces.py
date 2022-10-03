# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.forces.types import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
from dynamodb.types import (
    Item,
)


def format_forces_vulnerabilities_to_add(
    vulns: Item,
) -> ExecutionVulnerabilities:
    return ExecutionVulnerabilities(
        num_of_accepted_vulnerabilities=int(len(vulns["accepted"])),
        num_of_open_vulnerabilities=int(len(vulns["open"])),
        num_of_closed_vulnerabilities=int(len(vulns["closed"])),
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
        "date": execution.execution_date,
        "git_commit": execution.commit,
        "git_repo": execution.repo,
        "git_branch": execution.branch,
        "kind": execution.kind,
        "exit_code": execution.exit_code,
        "strictness": execution.strictness,
        "git_origin": execution.origin,
        "grace_period": int(execution.grace_period)
        if execution.grace_period
        else None,
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
