from arch_lint.dag import (
    DagMap,
)
from typing import (
    Union,
)

_dag: dict[str, tuple[Union[tuple[str, ...], str], ...]] = {
    "db_model": (
        "companies",
        "compliance",
        "roots",
        "azure_repositories",
        "integration_repositories",
        "events",
        "groups",
        "toe_ports",
        "enrollment",
        "vulnerabilities",
        "findings",
        "event_comments",
        "credentials",
        "last_sync",
        "finding_comments",
        "subscriptions",
        "stakeholders",
        "enums",
        "group_access",
        "organization_finding_policies",
        "group_comments",
        "organization_access",
        "organizations",
        "toe_lines",
        "toe_inputs",
        "portfolios",
        "forces",
        "utils",
        "types",
        "constants",
    ),
    "db_model.vulnerabilities": (
        "add",
        "get",
        "update",
        "remove",
        "utils",
        "constants",
        "types",
        "enums",
    ),
    "db_model.group_comments": (
        "remove",
        "get",
        "add",
        "utils",
        "types",
    ),
    "db_model.companies": ("update", "add", "get", "utils", "types"),
    "db_model.groups": (
        "add",
        "update",
        "get",
        "remove",
        "utils",
        "types",
        "enums",
        "constants",
    ),
    "db_model.compliance": ("get", "update", "utils", "types"),
    "db_model.roots": (
        "add",
        "get",
        "update",
        "remove",
        "constants",
        "utils",
        "types",
        "enums",
    ),
    "db_model.azure_repositories": ("get", "utils", "types"),
    "db_model.integration_repositories": (
        "get",
        "update",
        "remove",
        "utils",
        "types",
    ),
    "db_model.events": (
        "remove",
        "get",
        "update",
        "add",
        "constants",
        "utils",
        "types",
        "enums",
    ),
    "db_model.toe_ports": (
        "remove",
        "update",
        "get",
        "add",
        "constants",
        "utils",
        "types",
    ),
    "db_model.enrollment": (
        "update",
        "get",
        "add",
        "utils",
        "types",
        "enums",
    ),
    "db_model.findings": (
        "add",
        "get",
        "update",
        "remove",
        "utils",
        "types",
        "constants",
        "enums",
    ),
    "db_model.event_comments": (
        "add",
        "get",
        "remove",
        "utils",
        "types",
    ),
    "db_model.credentials": (
        "remove",
        "update",
        "get",
        "add",
        "constants",
        "utils",
        "types",
    ),
    "db_model.finding_comments": (
        "remove",
        "get",
        "add",
        "utils",
        "types",
        "enums",
    ),
    "db_model.subscriptions": (
        "remove",
        "get",
        "add",
        "constants",
        "utils",
        "types",
        "enums",
    ),
    "db_model.stakeholders": (
        "remove",
        "get",
        "update",
        "utils",
        "types",
        "constants",
    ),
    "db_model.enums": (),
    "db_model.group_access": (
        "get",
        "remove",
        "update",
        "enums",
        "utils",
        "types",
        "constants",
    ),
    "db_model.organization_finding_policies": (
        "update",
        "get",
        "remove",
        "add",
        "utils",
        "types",
        "enums",
    ),
    "db_model.organization_access": (
        "update",
        "get",
        "utils",
        "enums",
        "remove",
        "types",
    ),
    "db_model.organizations": (
        "add",
        "remove",
        "update",
        "get",
        "utils",
        "types",
        "constants",
        "enums",
    ),
    "db_model.toe_lines": (
        "remove",
        "get",
        "add",
        "update",
        "constants",
        "utils",
        "types",
    ),
    "db_model.portfolios": ("update", "get", "remove", "utils", "types"),
    "db_model.utils": (),
    "db_model.types": (),
    "db_model.constants": (),
    "db_model.toe_inputs": (
        "remove",
        "get",
        "update",
        "add",
        "utils",
        "types",
        "constants",
    ),
    "db_model.last_sync": ("operations", "_queries"),
    "db_model.forces": (
        "add",
        "get",
        "remove",
        "constants",
        "utils",
        "types",
        "enums",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
