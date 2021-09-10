from dataclasses import (
    dataclass,
)
from enum import (
    auto,
    Enum,
)
from returns.io import (
    IO,
)
from singer_io.singer2 import (
    SingerEmitter,
)
from tap_announcekit.api import (
    ApiClient,
    Creds,
)
from tap_announcekit.stream import (
    ProjectStream,
)
from typing import (
    Any,
    List,
)


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, _start: int, _count: int, _last_values: List[Any]
    ) -> str:
        return name


class SupportedStream(AutoName):
    PROJECTS = auto()
    ALL = auto()


@dataclass(frozen=True)
class StreamSelector:
    stream: SupportedStream


@dataclass(frozen=True)
class Streamer:
    creds: Creds
    selection: StreamSelector

    def start(self) -> IO[None]:
        emitter = SingerEmitter()
        client = ApiClient(self.creds)

        if self.selection.stream == SupportedStream.PROJECTS:
            proj_stream = ProjectStream(client, emitter)
            proj_stream.emit_schema()
        return IO(None)
