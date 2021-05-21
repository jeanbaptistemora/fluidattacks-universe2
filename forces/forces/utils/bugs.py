# Standard library
import os
from contextvars import (
    ContextVar,
)
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
import bugsnag
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientResponseError,
)

# Local libraries
from forces.utils.env import guess_environment, BASE_DIR

# Constants
META: ContextVar[Optional[Dict[str, str]]] = ContextVar("META", default=None)


def customize_bugsnag_error_reports(
    notification: Any,
) -> None:  # pragma: no cover
    # Customize Login required error
    environment = dict()
    if os.environ.get("CI_JOB_ID", None):
        environment["PIPELINE"] = "GITLAB_CI"
        environment["CI_JOB_ID"] = os.environ.get("CI_JOB_ID", "unknown")
        environment["CI_JOB_URL"] = os.environ.get("CI_JOB_URL", "unknown")
    elif os.environ.get("CIRCLECI", None):
        environment["PIPELINE"] = "CIRCLECI"
        environment["CIRCLE_BUILD_NUM"] = os.environ.get(
            "CIRCLE_BUILD_NUM", "unknown"
        )
        environment["CIRCLE_BUILD_URL"] = os.environ.get(
            "CIRCLE_BUILD_URL", "unknown"
        )
    elif os.environ.get("System.JobId", None):
        environment["PIPELINE"] = "AZURE_DEVOPS"
        environment["System.JobId"] = os.environ.get("System.JobId", "unknown")
    elif os.environ.get("BUILD_NUMBER", None):
        environment["PIPELINE"] = "JENKINS"
        os.environ["BUILD_NUMBER"] = os.environ.get("BUILD_NUMBER", "unknown")
        os.environ["BUILD_ID"] = os.environ.get("BUILD_ID", "unknown")
        os.environ["BUILD_URL"] = os.environ.get("BUILD_URL", "unknown")
    notification.add_tab("environment", environment)

    if isinstance(
        notification.exception,
        (
            ClientConnectorError,
            ClientResponseError,
        ),
    ):
        login_error = any(
            [
                err in str(notification.exception)
                for err in ("Login required", "Access denied")
            ]
        )
        if login_error:
            notification.severity = "info"
            notification.unhandled = False


def configure_bugsnag(**data: str) -> None:
    # Metadata configuration
    META.set(data)
    # Add before handler
    bugsnag.before_notify(customize_bugsnag_error_reports)
    # Initialization
    bugsnag.configure(
        # There is no problem in making this key public
        #   it's intentional so we can monitor Skims stability in remote users
        api_key="3625546064ad4b5b78aa0c0c93919fc5",
        # Assume development stage if this source file is within repository
        release_stage=guess_environment(),
        project_root=BASE_DIR,
    )
    bugsnag.start_session()
    bugsnag.send_sessions()
