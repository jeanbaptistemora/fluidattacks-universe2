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
import logging
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Dict,
    IO,
    Tuple,
)

LOG = logging.getLogger(__name__)


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
        LOG.info("Grouping records...")
        schemas: Dict[str, SingerSchema] = {}
        files: Dict[str, IO[str]] = {}
        file_paths: Dict[str, str] = {}  # stream - file_path dict
        for s in act.unwrap(data.unsafe_to_iter()):
            if isinstance(s, SingerSchema):
                LOG.debug("Saving SingerSchema of stream %s", s.stream)
                schemas[s.stream] = s
            elif isinstance(s, SingerRecord):
                if files.get(s.stream) is None:
                    LOG.debug("Creating file for stream %s", s.stream)
                    files[s.stream] = NamedTemporaryFile(
                        "w+", delete=False
                    )  # implicit cmd
                act.unwrap(emit(files[s.stream], s))
        for k, f in files.items():
            LOG.debug("Closing file of stream %s", k)
            f.close()  # for getting data flushed
            LOG.debug("Closed file of stream %s!", k)
            file_paths[k] = f.name
        LOG.debug("Generating GroupedRecords objs...")
        groups = tuple(
            GroupedRecords(s, act.unwrap(TempReadOnlyFile.freeze(f)))
            for s, f in file_paths.items()
        )
        LOG.debug("GroupedRecords generated!")
        LOG.debug("Freezing schema")
        _schema = freeze(schemas)
        LOG.debug("Schema frozen!")
        return (_schema, groups)

    end = Cmd.from_cmd(lambda: LOG.info("Records grouping completed!"))
    return new_cmd(_action).bind(lambda i: end.map(lambda _: i))
