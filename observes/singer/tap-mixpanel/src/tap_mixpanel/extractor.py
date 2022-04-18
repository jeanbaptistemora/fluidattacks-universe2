import botocore
import pandas
from pandas import (
    Timestamp,
)
from singer_io.file import (
    DataFile,
)
import tempfile
from typing import (
    Any,
    cast,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

BUCKET_NAME = "fluidanalytics"
BACKUP_FOLDER = "backup_mixpanel"


Interval = Union[pandas.Interval]


def _get_extremes(date_range: Interval) -> Tuple[Timestamp, Timestamp]:
    start = (
        date_range.left
        if date_range.closed == "left" or date_range.closed == "both"
        else date_range.left + pandas.DateOffset(days=1)
    )
    end = (
        date_range.right
        if date_range.closed == "right" or date_range.closed == "both"
        else date_range.right - pandas.DateOffset(days=1)
    )
    return (start, end)


class BackupId(NamedTuple):
    event: str
    month: int
    year: int

    @classmethod
    def new(cls, event: str, date_range: Interval) -> "BackupId":
        start, end = _get_extremes(date_range)
        assert start.is_month_start
        assert end.is_month_end
        return BackupId(event=event, month=start.month, year=start.year)

    @classmethod
    def try_new(cls, event: str, date_range: Interval) -> Optional["BackupId"]:
        try:
            return BackupId.new(event, date_range)
        except AssertionError:
            return None


class ResourceId(NamedTuple):
    event: str
    date_range: Interval
    backup_id: Optional[BackupId]

    @classmethod
    def new(cls, event: str, date_range: Interval) -> "ResourceId":
        return ResourceId(
            event=event,
            date_range=date_range,
            backup_id=BackupId.try_new(event, date_range),
        )


def _backup_path(bkup_id: BackupId) -> str:
    return f"{BACKUP_FOLDER}/{bkup_id.year}-{bkup_id.month}.singer"


def _in_backup(s3_client: Any, bkup_id: BackupId) -> bool:
    try:
        s3_client.Object(BUCKET_NAME, _backup_path(bkup_id)).load()
        return True
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            return False
        raise error


def _get_backup(s3_client: Any, bkup_id: BackupId) -> DataFile:
    with tempfile.NamedTemporaryFile("w+") as tmp:
        s3_client.meta.client.download_file(
            BUCKET_NAME, _backup_path(bkup_id), tmp.name
        )
        return DataFile.from_file(tmp)


def _date_to_str(date: Timestamp) -> str:
    return pandas.to_datetime(date).strftime("%Y-%m-%d")


def _get_str_extremes(date_range: Interval) -> Tuple[str, str]:
    endpoints = _get_extremes(date_range)
    transformed = cast(Tuple[str, str], tuple(map(_date_to_str, endpoints)))
    return transformed


def _get_from_api(
    api_client: Any,
    resource: ResourceId,
) -> DataFile:
    with tempfile.NamedTemporaryFile("w+") as tmp:
        tmp.write(
            api_client.load_data(
                resource.event, _get_str_extremes(resource.date_range)
            )
        )
        return DataFile.from_file(tmp)
