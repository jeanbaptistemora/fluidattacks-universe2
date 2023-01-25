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
    "settings": (
        "gunicorn",
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
    return cast(DagMap, DagMap.new(_dag))
