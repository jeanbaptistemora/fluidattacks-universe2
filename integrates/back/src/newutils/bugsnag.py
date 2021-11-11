import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from context import (
    BASE_URL,
    FI_BUGSNAG_API_KEY_SCHEDULER,
    FI_ENVIRONMENT,
)


def start_scheduler_session() -> None:
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        api_key=FI_BUGSNAG_API_KEY_SCHEDULER,
        project_root=BASE_URL,
        release_stage=FI_ENVIRONMENT,
    )
    bugsnag.start_session()
