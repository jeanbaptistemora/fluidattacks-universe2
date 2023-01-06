from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "newutils": (
        "organization_access",
        "finding_comments",
        "env",
        "forms",
        "compliance",
        "string",
        "encodings",
        "requests",
        "event_comments",
        "group_comments",
        "stakeholders",
        "subscriptions",
        "validations",
        "organizations",
        "vulnerabilities",
        "templates",
        "resources",
        "reports",
        "bugsnag",
        "analytics",
        "deprecations",
        "logs",
        "group_access",
        "files",
        "groups",
        "utils",
        "findings",
        "forces",
        "cvss",
        "datetime",
    ),
    "newutils.deprecations": ("ast", "filters", "types"),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
