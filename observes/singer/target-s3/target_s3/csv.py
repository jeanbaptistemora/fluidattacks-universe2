from . import (
    _utils,
)
import csv
from fa_purity import (
    Cmd,
    FrozenList,
    PureIter,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
import logging
from target_s3.core import (
    CompletePlainRecord,
    RecordGroup,
    TempReadOnlyFile,
)
from typing import (
    IO,
    Tuple,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _save(data: PureIter[FrozenList[Primitive]]) -> Cmd[TempReadOnlyFile]:
    def write_cmd(file: IO[str]) -> Cmd[None]:
        def _action() -> None:
            writer = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows(data)

        return Cmd.from_cmd(_action)

    return TempReadOnlyFile.from_cmd(write_cmd)


def _ordered_data(record: CompletePlainRecord) -> FrozenList[Primitive]:
    def _key(item: Tuple[str, Primitive]) -> str:
        return item[0]

    items = tuple(record.record.record.items())
    ordered = sorted(items, key=_key)
    return tuple(i[1] for i in ordered)


def save(
    group: RecordGroup,
) -> Cmd[TempReadOnlyFile]:
    msg = _utils.log_cmd(
        lambda: LOG.info(
            "Saving stream `%s` data into temp", group.schema.stream
        ),
        None,
    )
    return msg + group.records.map(_ordered_data).transform(
        lambda x: _save(x)
    ).bind(
        lambda t: _utils.log_cmd(
            lambda: LOG.info(
                "Stream `%s` saved into temp file!", group.schema.stream
            ),
            t,
        )
    )
