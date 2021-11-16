from dataclasses import (
    dataclass,
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
from tap_announcekit.streams.external_users import (
    _encode,
    _factory,
)


@dataclass(frozen=True)
class ExtUsersStream:
    _client: ApiClient
    _name: str

    def stream(
        self,
        proj: ProjectId,
    ) -> StreamIO:
        factory = _factory.ExtUserFactory(self._client, proj)
        data = factory.get_ids().map(
            lambda i: i.bind(
                lambda uid: factory.get(uid).map(lambda u: IndexedObj(uid, u))
            )
        )
        encoder = _encode.ExtUserObjEncoders(self._name)
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
