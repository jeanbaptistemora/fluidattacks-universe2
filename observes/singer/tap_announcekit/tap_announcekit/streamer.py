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
    StreamEmitter,
)
from tap_announcekit.streams.project import (
    ProjectId,
    ProjectStreams,
)
from tap_announcekit.utils import (
    new_iter,
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
    selection: SupportedStream
    proj: ProjectId

    def start(self) -> IO[None]:
        client = ApiClient(self.creds)

        if self.selection == SupportedStream.PROJECTS:
            proj_stream = ProjectStreams.stream(
                client.endpoint, new_iter([self.proj])
            )
            emitter = StreamEmitter(
                SingerEmitter(),
                proj_stream,
            )
            return emitter.emit()
        return IO(None)
