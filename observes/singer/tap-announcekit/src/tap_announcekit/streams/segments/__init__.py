from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
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
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.segments._encode import (
    SegmentFieldEncoder,
    SegmentProfileEncoder,
)
from tap_announcekit.streams.segments._factory import (
    SegmentFactory,
)


@dataclass(frozen=True)
class SegmentStreams:
    _client: ApiClient
    _name: str

    def stream_fields(
        self,
        ids: PureIter[ProjectId],
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        factory = SegmentFactory(self._client)
        encoder = SegmentFieldEncoder(self._name)
        data = io_transform.chain(
            ids.map(factory.get_segments).map(
                lambda i: i.map(lambda l: from_flist(l))
            )
        )
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)

    def stream_profiles(
        self,
        ids: PureIter[ProjectId],
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        factory = SegmentFactory(self._client)
        encoder = SegmentProfileEncoder(self._name)
        data = io_transform.chain(
            ids.map(factory.get_profiles).map(
                lambda i: i.map(lambda l: from_flist(l))
            )
        )
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
