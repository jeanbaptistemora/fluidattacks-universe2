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
        if environ.get("CI_COMMIT_REF_NAME", "master") == "master"
        else "development"
    )
