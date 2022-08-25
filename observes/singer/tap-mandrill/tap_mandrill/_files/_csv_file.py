from ._str_file import (
    StrFile,
)
import csv
from csv import (
    Error,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    JsonValue,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.json.factory import (
    from_any,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter import (
    factory as PIterFactory,
)
from typing import (
    cast,
    Dict,
    Iterable,
    List,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


def _assert_dict(raw: _T) -> FrozenDict[str, str]:
    return (
        from_any(raw)
        .bind(lambda x: Unfolder(JsonValue(x)).to_dict_of(str))
        .unwrap()
    )


@dataclass(frozen=True)
class CsvFile:
    @staticmethod
    def read_dicts(file: StrFile) -> PureIter[ResultE[FrozenDict[str, str]]]:
        def _generator() -> Iterable[ResultE[FrozenDict[str, str]]]:
            end = False
            rows = csv.DictReader(file.read(), restval="")
            # `restval=""` ensures that dict values (except for restkey)
            # are `str`` and not `Optional[str]` (default)
            while not end:
                try:
                    row = cast(
                        Dict[Optional[str], str | List[str]],
                        next(rows),
                    )  # yield type of DictReader is incorrect, casted to the correct one.
                    data = row.copy()
                    if None in data:
                        # since the `None` key maps to `List[str]`, deleting it should
                        # result in the expected `data: Dict[str, str]`
                        data.pop(None)
                    final_val = _assert_dict(data)  # ensure data expected type
                    yield Result.success(final_val)
                except Error as err:
                    yield Result.failure(err)
                except StopIteration:
                    end = True

        return PIterFactory.unsafe_from_cmd(Cmd.from_cmd(_generator))
