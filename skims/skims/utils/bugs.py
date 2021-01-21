# Standard library
from typing import (
    Dict,
)

# Third party libraries
import bugsnag

# Local libraries
from utils.env import (
    guess_environment,
)

# Constants
META: Dict[str, str] = {}


def add_bugsnag_data(**data: str) -> None:
    META.update(data)


def initialize_bugsnag() -> None:
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
