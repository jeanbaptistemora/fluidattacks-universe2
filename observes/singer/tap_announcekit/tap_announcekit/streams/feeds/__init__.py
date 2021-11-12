from dataclasses import (
    dataclass,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from purity.v1.pure_iter.transform import (
    io as io_transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.feeds._encode import (
    FeedObjEncoders,
)
from tap_announcekit.streams.feeds._factory import (
    FeedFactory,
)


@dataclass(frozen=True)
class FeedStreams:
    client: ApiClient
    _name: str = "feed"

    def stream(
        self,
        proj: ProjectId,
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        factory = FeedFactory(self.client)
        encoder = FeedObjEncoders(self._name)
        data = io_transform.chain(
            from_flist((factory.get_ids(proj).map(lambda i: from_flist(i)),))
        ).map(
            lambda i: i.bind(
                lambda f_id: factory.get(f_id).map(
                    lambda f: IndexedObj(f_id, f)
                )
            )
        )
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
