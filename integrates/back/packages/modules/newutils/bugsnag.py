# Third party libraries
import bugsnag

# Local libraries
from __init__ import (
    BASE_URL,
    FI_ENVIRONMENT,
    FI_BUGSNAG_API_KEY_SCHEDULER
)


def start_scheduler_session() -> None:
    bugsnag.configure(
        api_key=FI_BUGSNAG_API_KEY_SCHEDULER,
        project_root=BASE_URL,
        release_stage=FI_ENVIRONMENT,
    )
    bugsnag.start_session()
