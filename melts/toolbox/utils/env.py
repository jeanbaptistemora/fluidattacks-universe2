from os import (
    environ,
)
from toolbox.constants import (
    BASE_DIR,
)


def guess_environment() -> str:
    if any(
        (
            "product/" in BASE_DIR,
            environ.get("CI_COMMIT_REF_NAME", "trunk") != "trunk",
        )
    ):
        return "development"

    return "production"  # pragma: no cover
