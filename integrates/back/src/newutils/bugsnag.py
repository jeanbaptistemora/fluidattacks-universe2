import bugsnag
from bugsnag import (
    legacy as bugsnag_legacy,
)
from bugsnag_client import (
    CustomBugsnagClient,
)
from context import (
    BASE_URL,
    FI_BUGSNAG_API_KEY_SCHEDULER,
    FI_ENVIRONMENT,
)


def start_scheduler_session() -> None:
    bugsnag.configure(
        api_key=FI_BUGSNAG_API_KEY_SCHEDULER,
        project_root=BASE_URL,
        release_stage=FI_ENVIRONMENT,
    )
    bugsnag.start_session()
    bugsnag_legacy.default_client = CustomBugsnagClient()
