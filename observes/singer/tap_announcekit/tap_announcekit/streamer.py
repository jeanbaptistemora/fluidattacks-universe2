from dataclasses import (
    dataclass,
)
from enum import (
    auto,
    Enum,
)
from purity.v1 import (
    Flattener,
    FrozenDict,
)
from purity.v1.pure_iter.factory import (
    from_flist,
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
    Stream,
    StreamEmitter,
    StreamEmitterFactory,
)
from tap_announcekit.streams import (
    ActivitiesStreams,
    ExtUsersStream,
    FeedbackStreams,
    PostContentStreams,
    PostStreams,
    ProjectStreams,
    WidgetStreams,
)
from tap_announcekit.streams.feeds import (
    FeedStreams,
)
from tap_announcekit.streams.labels import (
    LabelStreams,
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
    ACTIVITIES = auto()
    PROJECTS = auto()
    POSTS = auto()
    POST_CONTENTS = auto()
    FEEDS = auto()
    FEEDBACKS = auto()
    EXT_USERS = auto()
    WIDGETS = auto()
    LABELS = auto()
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

    @property
    def stream_map(self) -> FrozenDict[SupportedStream, Stream[Any]]:
        streams = {
            SupportedStream.PROJECTS: ProjectStreams(
                self.client, SupportedStream.PROJECTS.value
            ).stream(from_flist((self.proj,))),
            SupportedStream.FEEDBACKS: FeedbackStreams(
                self.client, SupportedStream.FEEDBACKS.value
            ).proj_feedbacks(self.proj),
            SupportedStream.ACTIVITIES: ActivitiesStreams(
                self.client, SupportedStream.ACTIVITIES.value
            ).stream(
                self.proj,
            ),
            SupportedStream.EXT_USERS: ExtUsersStream(
                self.client, SupportedStream.EXT_USERS.value
            ).stream(self.proj),
            SupportedStream.FEEDS: FeedStreams(
                self.client, SupportedStream.FEEDS.value
            ).stream(self.proj),
            SupportedStream.WIDGETS: WidgetStreams(
                self.client, SupportedStream.WIDGETS.value
            ).stream(self.proj),
            SupportedStream.LABELS: LabelStreams(
                self.client, SupportedStream.LABELS.value
            ).stream(self.proj),
        }
        return FrozenDict(streams)

    def start(self) -> IO[None]:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        if self.selection in (
            SupportedStream.POSTS,
            SupportedStream.POST_CONTENTS,
            SupportedStream.ALL,
        ):
            ids_io = Flattener.list_io(
                tuple(PostStreams.ids(self.client, self.proj))
            ).map(lambda i: from_flist(i))
            if self.selection in (SupportedStream.POSTS, SupportedStream.ALL):
                ids_io.map(
                    PostStreams(
                        self.client, SupportedStream.POSTS.value
                    ).stream
                ).bind(lambda s: self.emitter.emit(s))
            if self.selection in (
                SupportedStream.POST_CONTENTS,
                SupportedStream.ALL,
            ):
                ids_io.map(
                    PostContentStreams(
                        self.client,
                        SupportedStream.POST_CONTENTS.value,
                    ).stream
                ).bind(lambda s: self.emitter.emit(s))
        if self.selection == SupportedStream.ALL:
            for _, stream in self.stream_map.items():
                self.emitter.emit(stream)
        elif self.selection in self.stream_map:
            self.emitter.emit(self.stream_map[self.selection])
        return IO(None)
