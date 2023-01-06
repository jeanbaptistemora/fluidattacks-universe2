from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "batch_dispatch": (
        "dispatch",
        "report",
        "refresh_toe_inputs",
        "handle_finding_policy",
        "remove_group_resources",
        "move_root",
        "update_organization_repositories",
        "refresh_toe_ports",
        "update_organization_overview",
        "clone_roots",
        "rebase",
        "utils",
        "remove_roots",
        "refresh_toe_lines",
    ),
    "batch_dispatch.utils": (
        "git_self",
        "s3",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
