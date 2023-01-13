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
from tap_mandrill.api._api_key import (
    ApiKey,
    KeyAccess,
)


def export_api_1(key: ApiKey) -> ExportApi:
    client = Client(key.extract(KeyAccess()))  # type: ignore[misc]
    get_jobs = _get_job.get_jobs(client)  # type: ignore[misc]
    return ExportApi.new(
        get_jobs,
        _activity.export_activity_2(key),
        lambda j, interval, retries: _download.until_finish(
            get_jobs, j, interval, retries
        ),
        _download.download,
    )
