from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CheckId:
    id_str: str
