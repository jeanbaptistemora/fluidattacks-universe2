from .core import (
    TempReadOnlyFile,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Stream,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
)
from fa_singer_io.singer.emitter import (
    emit,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Dict,
    IO,
    Tuple,
)


@dataclass
class GroupedRecords:
    stream: str
    file: TempReadOnlyFile


def group_records(
    data: Stream[SingerMessage],
) -> Cmd[Tuple[FrozenDict[str, SingerSchema], FrozenList[GroupedRecords]]]:
    def _action(
        act: CmdUnwrapper,
    ) -> Tuple[FrozenDict[str, SingerSchema], FrozenList[GroupedRecords]]:
        schemas: Dict[str, SingerSchema] = {}
        files: Dict[str, IO[str]] = {}
        for s in act.unwrap(data.unsafe_to_iter()):
            if isinstance(s, SingerSchema):
                schemas[s.stream] = s
            elif isinstance(s, SingerRecord):
                if files.get(s.stream) is None:
                    files[s.stream] = NamedTemporaryFile(
                        "w+", delete=False
                    )  # implicit cmd
                act.unwrap(emit(files[s.stream], s))
        groups = tuple(
            GroupedRecords(s, act.unwrap(TempReadOnlyFile.freeze(f)))
            for s, f in files.items()
        )
        return (freeze(schemas), groups)

    return new_cmd(_action)
