from enum import (
    Enum,
)
from io import (
    TextIOWrapper,
)
from typing import (
    NamedTuple,
    Optional,
)


class KindEnum(Enum):
    ALL: str = "all"
    DYNAMIC: str = "dynamic"
    STATIC: str = "static"


class ForcesConfig(NamedTuple):
    group: str
    kind: KindEnum = KindEnum.ALL
    output: Optional[TextIOWrapper] = None
    repository_path: Optional[str] = "."
    repository_name: Optional[str] = None
    strict: Optional[bool] = False
    verbose_level: int = 3
    breaking_severity: float = 0.0
