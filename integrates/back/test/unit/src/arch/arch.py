from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "integrates": (
        "cli",
        "app",
        "schedulers",
        "api",
        "batch_dispatch",
        "companies",
        "remove_stakeholder",
        "unreliable_indicators",
        "azure_repositories",
        "billing",
        "forces",
        "reports",
        "toe",
        "groups",
        "group_comments",
        "events",
        "vulnerability_files",
        "findings",
        "organizations_finding_policies",
        "vulnerabilities",
        "roots",
        "notifications",
        "event_comments",
        "finding_comments",
        "subscriptions",
        "analytics",
        "tags",
        "decorators",
        "organizations",
        "mailer",
        "stakeholders",
        "group_access",
        "authz",
        "batch",
        "newutils",
        "sessions",
        "dataloaders",
        "db_model",
        "dynamodb",
        "s3",
        "verify",
        "settings",
        "custom_exceptions",
        "context",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result  # pylint: disable=raising-bad-type
    return result
