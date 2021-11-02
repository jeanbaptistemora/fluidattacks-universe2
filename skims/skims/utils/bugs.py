import bugsnag
from bugsnag import (
    legacy as bugsnag_legacy,
)
from bugsnag_client import (
    CustomBugsnagClient,
)
from typing import (
    Dict,
)
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
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
    )
    bugsnag.start_session()
    bugsnag_legacy.default_client = CustomBugsnagClient()
