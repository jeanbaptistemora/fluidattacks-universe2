# Standard libraries
import tempfile
from contextlib import (
    contextmanager,
)
from typing import (
    Any,
    Callable,
    ContextManager,
    IO,
    Iterator,
    NamedTuple,
    Tuple,
    Union,
)

# Third party libraries
import botocore
import pandas

# Local libraries


BUCKET_NAME = 'fluidanalytics'
BACKUP_FOLDER = 'backup_mixpanel'


class SingerFile(NamedTuple):
    file_handler: Callable[[], ContextManager[IO[str]]]


class Extractor(NamedTuple):
    get_singer: Callable[[int, int], SingerFile]


Interval = Union[pandas.Interval]


def in_backup(s3_client: Any, year: int, month: int) -> bool:
    try:
        s3_client.Object(
            BUCKET_NAME,
            f'{BACKUP_FOLDER}/{year}-{month}.singer'
        ).load()
        return True
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == "404":
            return False
        raise error


def get_backup(s3_client: Any, year: int, month: int) -> SingerFile:
    @contextmanager
    def handler() -> Iterator[IO[str]]:
        with tempfile.NamedTemporaryFile('w+') as tmp:
            s3_client.meta.client.download_file(
                BUCKET_NAME,
                f'{BACKUP_FOLDER}/{year}-{month}.singer',
                tmp.name
            )
            yield tmp
    return SingerFile(file_handler=handler)


def get_extremes(date_range: Interval) -> Tuple[str, str]:
    start = date_range.left \
        if date_range.closed == 'left' or date_range.closed == 'both' \
        else date_range.left + pandas.DateOffset(days=1)
    end = date_range.right \
        if date_range.closed == 'right' or date_range.closed == 'both' \
        else date_range.right - pandas.DateOffset(days=1)
    start_date = pandas.to_datetime(start).strftime("%Y-%m-%d")
    end_date = pandas.to_datetime(end).strftime("%Y-%m-%d")
    return (start_date, end_date)


def get_from_api(
    api_client: Any,
    event: str,
    date_range: Interval,
) -> SingerFile:
    @contextmanager
    def handler() -> Iterator[IO[str]]:
        with tempfile.NamedTemporaryFile('w+') as tmp:
            tmp.write(api_client.load_data(event, get_extremes(date_range)))
            yield tmp
    return SingerFile(file_handler=handler)
