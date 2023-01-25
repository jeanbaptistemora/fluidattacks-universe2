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
    "vulnerabilities": ("domain", "types"),
    "vulnerabilities.domain": (
        "treatment",
        "core",
        "rebase",
        "verification",
        "snippet",
        "validations",
        "utils",
    ),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
