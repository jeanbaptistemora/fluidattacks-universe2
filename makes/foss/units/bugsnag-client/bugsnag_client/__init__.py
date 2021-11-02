from bugsnag.client import (
    Client,
)
from bugsnag.configuration import (
    RequestConfiguration,
)
from bugsnag.event import (
    Event,
)
import os
import re
from typing import (
    Any,
    Optional,
)


def remove_nix_hash(path: str) -> str:
    pattern = r"(\/nix\/store\/[a-z0-9]{32}-)"
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
        if "metadata" in options:
            if batch_job_id := os.environ.get("AWS_BATCH_JOB_ID"):
                options["meta_data"]["batch_job_id"] = batch_job_id
            if job_queue_name := os.environ.get("AWS_BATCH_JQ_NAME"):
                options["meta_data"]["batch_job_queue"] = job_queue_name

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
