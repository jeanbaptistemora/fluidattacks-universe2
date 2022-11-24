import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from contextvars import (
    ContextVar,
)
from toolbox.utils.env import (
    guess_environment,
)
from typing import (
    Dict,
    Optional,
)

# Constants
META: ContextVar[Optional[Dict[str, str]]] = ContextVar("META", default=None)


def configure_bugsnag(**data: str) -> None:
    # Metadata configuration
    META.set(data)

    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    # Initialization
    bugsnag.configure(
        # There is no problem in making this key public
        #   it's intentional so we can monitor melts stability in remote users
        api_key="82614f2055d58e971fe1604e1c5781df",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
