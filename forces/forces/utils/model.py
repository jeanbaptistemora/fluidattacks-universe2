# Standard imports
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
    Optional,
)
from io import TextIOWrapper


class KindEnum(Enum):
    ALL: str = 'all'
    DYNAMIC: str = 'dynamic'
    STATIC: str = 'static'


class ForcesConfig(NamedTuple):
    group: str
    kind: KindEnum = KindEnum.ALL
    output: Optional[TextIOWrapper] = None
    repository_path: Optional[str] = '.'
    repository_name: Optional[str] = None
    strict: Optional[bool] = False
    verbose_level: int = 3
