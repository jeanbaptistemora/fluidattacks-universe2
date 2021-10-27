import bugsnag
from bugsnag import (
    legacy as bugsnag_legacy,
)
from bugsnag.client import (
    Client,
)
from bugsnag.configuration import (
    RequestConfiguration,
)
from bugsnag.event import (
    Event,
)
import re
from typing import (
    Any,
    Dict,
    Optional,
)
from utils.env import (
    guess_environment,
)

# Constants
META: Dict[str, str] = {}


def remove_nix_hash(path: str) -> str:
    pattern = r"(\/nix\/store\/[a-z0-9]*-)"
    result = re.search(pattern, path)
    if not result:
        return path
    return path[result.end(0) :]


class CustomBugsnagClient(Client):
    def notify(
        self,
        exception: BaseException,
        asynchronous: Optional[bool] = None,
        **options: Any,
    ) -> None:
        event = Event(
            exception,
            self.configuration,
            RequestConfiguration.get_instance(),
            **options,
        )
        event.stacktrace = [
            {**trace, "file": remove_nix_hash(trace["file"])}
            for trace in event.stacktrace
        ]
        self.deliver(event, asynchronous=asynchronous)


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
