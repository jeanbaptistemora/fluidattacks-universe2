from os import (
    environ,
)
from typing import (
    Literal,
)


def guess_environment() -> Literal["development"] | Literal["production"]:
    return (
        "production"
        if environ.get("CI_COMMIT_REF_NAME", "trunk") == "trunk"
        else "development"
    )
