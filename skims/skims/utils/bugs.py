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
from utils.env import (
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
        #   it's intentional so we can monitor Skims stability in remote users
        api_key="f990c9a571de4cb44c96050ff0d50ddb",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
    bugsnag.send_sessions()
