from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    user: str
    key: str
