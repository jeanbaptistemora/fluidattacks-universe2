from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "settings": (
        "jwt",
        "uvicorn",
        "session",
        "logger",
        "various",
        "analytics",
        "api",
        "auth",
        "statics",
    ),
    "settings.auth": (
        "google",
        "bitbucket",
        "azure",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
