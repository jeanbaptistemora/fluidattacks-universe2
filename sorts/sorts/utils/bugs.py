import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from contextvars import (
    ContextVar,
)
import os
from typing import (
    Dict,
    Optional,
)

# Constants
META: ContextVar[Optional[Dict[str, str]]] = ContextVar("META", default=None)


def guess_environment() -> str:
    if any(
        (
            "product/" in os.path.dirname(__file__),
            os.environ.get("CI_COMMIT_REF_NAME", "master") != "master",
        )
    ):
        return "development"

    return "production"  # pragma: no cover


def configure_bugsnag(**data: str) -> None:
    # Metadata configuration
    META.set(data)
    # Initialization
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        # There is no problem in making this key public
        # it's intentional so we can monitor Sorts stability in remote users
        api_key="1d6da191337056ca6fa2c47f47be2a3a",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
    bugsnag.send_sessions()
