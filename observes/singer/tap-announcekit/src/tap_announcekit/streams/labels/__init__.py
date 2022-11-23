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
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.labels._encode import (
    LabelObjEncoders,
)
from tap_announcekit.streams.labels._factory import (
    LabelFactory,
)


@dataclass(frozen=True)
class LabelStreams:
    _client: ApiClient
    _name: str

    def stream(
        self,
        proj: ProjectId,
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        factory = LabelFactory(self._client)
        encoder = LabelObjEncoders(self._name)
        data = io_transform.chain(
            from_flist((factory.get(proj).map(lambda i: from_flist(i)),))
        )
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
