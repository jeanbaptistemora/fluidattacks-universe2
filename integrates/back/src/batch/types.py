from typing import (
    NamedTuple,
)


class BatchProcessing(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    key: str
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str
    queue: str
