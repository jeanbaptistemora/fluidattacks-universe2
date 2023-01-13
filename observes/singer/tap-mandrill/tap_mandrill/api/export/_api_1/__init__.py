from . import (
    _activity,
    _download,
    _get_job,
)
from .._core import (
    ExportApi,
)
from mailchimp_transactional import (
    Client,
)


def export_api_1(client: Client) -> ExportApi:  # type: ignore[no-any-unimported]
    get_jobs = _get_job.get_jobs(client)  # type: ignore[misc]
    return ExportApi.new(
        get_jobs,
        _activity.export_activity(client),  # type: ignore[misc]
        lambda j, interval, retries: _download.until_finish(
            get_jobs, j, interval, retries
        ),
        _download.download,
    )
