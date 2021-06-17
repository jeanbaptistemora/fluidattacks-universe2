from model import (
    core_model,
)
from typing import (
    NamedTuple,
)


class SSLContext(NamedTuple):
    target: core_model.SkimsSslTarget

    def __str__(self) -> str:
        return f"{self.target.host}:{self.target.port}"
