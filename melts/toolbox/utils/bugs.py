# Standard library
from contextvars import (
    ContextVar,
)
from typing import (
    Dict,
    Optional,
)

# Third party libraries
import bugsnag

# Local libraries
from toolbox.utils.env import (
    guess_environment,
)

# Constants
META: ContextVar[Optional[Dict[str, str]]] = (
    ContextVar('META', default=None)
)


def configure_bugsnag(**data: str) -> None:
    # Metadata configuration
    META.set(data)
    # Initialization
    bugsnag.configure(
        # There is no problem in making this key public
        #   it's intentional so we can monitor melts stability in remote users
        api_key="82614f2055d58e971fe1604e1c5781df",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
    bugsnag.send_sessions()
