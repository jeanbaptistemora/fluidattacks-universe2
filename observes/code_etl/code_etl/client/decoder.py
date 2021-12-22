from code_etl.objs import (
    CommitData,
    Deltas,
    User,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    FrozenList,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from typing import (
    Any,
    Union,
)


class RawDecodeError(Exception):
    def __init__(
        self,
        target: str,
        raw: Any,
    ):
        super().__init__(
            f"TypeError when trying to build `{target}` "
            f"from raw obj `{str(raw)}`"
        )


def _assert_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise TypeError("Not a datetime obj")


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise TypeError("Not a str obj")


def _assert_int(raw: Any) -> int:
    if isinstance(raw, int):
        return raw
    raise TypeError("Not a int obj")


def decode_commit_data(
    raw: FrozenList[Any],
) -> Result[CommitData, Union[KeyError, TypeError]]:
    try:
        data = CommitData(
            User(_assert_str(raw[0]), _assert_str(raw[1])),
            _assert_datetime(raw[2]),
            User(_assert_str(raw[3]), _assert_str(raw[4])),
            _assert_datetime(raw[5]),
            _assert_str(raw[6]),
            _assert_str(raw[7]),
            Deltas(
                _assert_int(raw[8]),
                _assert_int(raw[9]),
                _assert_int(raw[10]),
                _assert_int(raw[11]),
            ),
        )
        return Success(data)
    except KeyError as err:
        return Failure(err)
    except TypeError as err:
        return Failure(err)
