from dataclasses import (
    dataclass,
)
from enum import (
    auto,
    Enum,
)
from purity.v1 import (
    PureIter,
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
from tap_announcekit.objs.id_objs import (
    PostId,
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
class _Streamer:
    client: ApiClient
    selection: SupportedStream
    proj: ProjectId


class Streamer(_Streamer):
    def __init__(
        self,
        creds: Creds,
        selection: SupportedStream,
        proj: ProjectId,
    ) -> None:
        super().__init__(ApiClient(creds), selection, proj)

    def stream_posts(self, ids: PureIter[PostId]) -> IO[None]:
        streams = PostsStreams(self.client)
        stream = streams.stream(ids)
        emitter = StreamEmitter(
            SingerEmitter(),
            stream,
        )
        return emitter.emit()

    def stream_proj(self) -> IO[None]:
        stream = ProjectStreams.stream(
            self.client, PureIterFactory.from_flist((self.proj,))
        )
        emitter = StreamEmitter(
            SingerEmitter(),
            stream,
        )
        return emitter.emit()

    def start(self) -> IO[None]:
        if self.selection in (SupportedStream.PROJECTS, SupportedStream.ALL):
            self.stream_proj()
        if self.selection in (SupportedStream.POSTS, SupportedStream.ALL):
            streams = PostsStreams(self.client)
            ids_io = streams.ids(self.proj)
            ids_io.map(self.stream_posts)
        return IO(None)
