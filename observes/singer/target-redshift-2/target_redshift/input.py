from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_singer_io.singer import (
    SingerMessage,
)
from fa_singer_io.singer.deserializer import (
    from_file,
    from_file_ignore_failed,
)
from io import (
    TextIOWrapper,
)
import sys


@dataclass(frozen=True)
class InputEmitter:
    ignore_failed: bool

    @property
    def input_stream(self) -> Stream[SingerMessage]:
        deserializer = (
            from_file_ignore_failed if self.ignore_failed else from_file
        )
        cmd = Cmd.from_cmd(
            lambda: TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        )
        return unsafe_from_cmd(cmd.map(deserializer).map(lambda x: iter(x)))
