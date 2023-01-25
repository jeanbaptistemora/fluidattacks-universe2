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
    "event_comments": (),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
