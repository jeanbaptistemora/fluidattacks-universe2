# Standard libraries
import os
from contextvars import (
    ContextVar,
)
from typing import (
    Dict,
    Optional,
)

# Third-party libraries
import bugsnag


# Constants
META: ContextVar[Optional[Dict[str, str]]] = (
    ContextVar('META', default=None)
)


def guess_environment() -> str:
    if any((
        'product/' in os.path.dirname(__file__),
        os.environ.get('CI_COMMIT_REF_NAME', 'master') != 'master',
    )):
        return 'development'

    return 'production'  # pragma: no cover


def configure_bugsnag(**data: str) -> None:
    # Metadata configuration
    META.set(data)
    # Initialization
    bugsnag.configure(
        # There is no problem in making this key public
        # it's intentional so we can monitor Sorts stability in remote users
        api_key="1d6da191337056ca6fa2c47f47be2a3a",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
    bugsnag.send_sessions()
