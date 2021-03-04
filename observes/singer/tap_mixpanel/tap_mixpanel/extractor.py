# Standard libraries
from typing import (
    Any,
    Callable,
    IO,
    Iterator,
    NamedTuple,
)

# Third party libraries
import botocore
# Local libraries


BUCKET_NAME = 'fluidanalytics'
BACKUP_FOLDER = 'backup_mixpanel'


class SingerFile(NamedTuple):
    file: Iterator[IO[str]]


class Extractor(NamedTuple):
    get_singer: Callable[[int, int], SingerFile]


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
