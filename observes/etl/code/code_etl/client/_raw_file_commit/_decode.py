from fa_purity import (
    FrozenList,
    Maybe,
    ResultE,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from redshift_client.sql_client import (
    RowData,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def get_index(items: FrozenList[_T], index: int) -> Maybe[_T]:
    try:
        return Maybe.from_value(items[index])
    except KeyError:
        return Maybe.empty()


def decode_file_path(raw: RowData) -> ResultE[str]:
    return (
        get_index(raw.data, 0)
        .to_result()
        .alt(Exception)
        .bind(lambda v: to_primitive(v, str).alt(Exception))
        .alt(
            lambda e: Exception(
                f"[Decode error] Cannot decode file path i.e. {e}"
            )
        )
    )
