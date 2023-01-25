from arch_lint.dag import (
    DagMap,
)
from typing import (
    cast,
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "mailer": (
        "analytics",
        "findings",
        "forms",
        "vulnerabilities",
        "groups",
        "types",
        "events",
        "deprecations",
        "common",
        "utils",
    ),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
