from os import (
    environ,
)
from typing import (
    Literal,
    Union,
)


def guess_environment() -> Union[
    Literal["development"],
    Literal["production"],
]:
    return (
        "production"
        if environ.get("CI_COMMIT_REF_NAME", "trunk") == "trunk"
        else "development"
    )
