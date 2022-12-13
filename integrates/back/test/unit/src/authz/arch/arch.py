from arch_lint.dag.core import (
    DAG,
    new_dag,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "authz": (
        "validations",
        "boundary",
        "enforcer",
        "policy",
        "model",
    ),
}


def project_dag() -> DAG:
    return new_dag(_dag)
