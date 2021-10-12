from dataclasses import (
    dataclass,
)
from enum import (
    auto,
    Enum,
)
from purity.v1 import (
    PureIterFactory,
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
from tap_announcekit.streams.posts import (
    PostsStreams,
)
from tap_announcekit.streams.project import (
    ProjectId,
    ProjectStreams,
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
        # pylint: disable=arguments-differ
        # pylint false positive
        return name


class SupportedStream(AutoName):
    PROJECTS = auto()
    POSTS = auto()
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

        if self.selection in (SupportedStream.PROJECTS, SupportedStream.ALL):
            proj_stream = ProjectStreams.stream(
                client, PureIterFactory.from_flist((self.proj,))
            )
            emitter = StreamEmitter(
                SingerEmitter(),
                proj_stream,
            )
            emitter.emit()
        if self.selection in (SupportedStream.POSTS, SupportedStream.ALL):
            stream_io = PostsStreams(client).stream_all(self.proj)
            emitter_io = stream_io.map(
                lambda stream: StreamEmitter(
                    SingerEmitter(),
                    stream,
                )
            )
            emitter_io.bind(lambda e: e.emit())
        return IO(None)
