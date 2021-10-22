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
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.stream import (
    StreamEmitter,
    StreamEmitterFactory,
)
from tap_announcekit.streams import (
    PostContentStreams,
    PostStreams,
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
    POST_CONTENTS = auto()
    ALL = auto()


@dataclass(frozen=True)
class StreamSelector:
    stream: SupportedStream


@dataclass(frozen=True)
class _Streamer:
    client: ApiClient
    selection: SupportedStream
    proj: ProjectId
    emitter: StreamEmitter


@dataclass(frozen=True)
class Streamer(_Streamer):
    def __init__(
        self,
        creds: Creds,
        selection: SupportedStream,
        proj: ProjectId,
    ) -> None:
        factory = StreamEmitterFactory(SingerEmitter())
        super().__init__(
            ApiClient(creds), selection, proj, factory.new_emitter()
        )

    def start(self) -> IO[None]:
        if self.selection in (SupportedStream.PROJECTS, SupportedStream.ALL):
            ProjectStreams(self.client, self.emitter).emit(
                PureIterFactory.from_flist((self.proj,))
            )
        if self.selection in (
            SupportedStream.POSTS,
            SupportedStream.POST_CONTENTS,
            SupportedStream.ALL,
        ):
            ids_io = PostStreams.ids(self.client, self.proj)
            if self.selection in (SupportedStream.POSTS, SupportedStream.ALL):
                ids_io.bind(PostStreams(self.client, self.emitter).emit)
            if self.selection in (
                SupportedStream.POST_CONTENTS,
                SupportedStream.ALL,
            ):
                ids_io.bind(PostContentStreams(self.client, self.emitter).emit)
        return IO(None)
