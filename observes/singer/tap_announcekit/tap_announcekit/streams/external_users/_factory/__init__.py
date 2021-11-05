# pylint: disable=unnecessary-lambda
# for correct type checking lambda is necessary
from dataclasses import (
    dataclass,
)
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    PureIter,
    Transform,
)
from purity.v1.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from purity.v1.pure_iter.transform import (
    io as io_transform,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.ext_user import (
    ExternalUser,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.external_users._factory import (
    _from_raw,
    _queries,
)


@dataclass(frozen=True)
class ExtUserFactory:
    _client: ApiClient
    proj: ProjectId

    @staticmethod
    def _filter_empty(page: DataPage[ExtUserId]) -> Maybe[DataPage[ExtUserId]]:
        return Maybe.from_optional(page if len(page.items) > 0 else None)

    def get_page(self, page: int) -> IO[Maybe[DataPage[ExtUserId]]]:
        query = _queries.ExtUserIdsQuery(
            Transform(partial(_from_raw.to_page, self.proj)), self.proj, page
        ).query
        return self._client.get(query).map(self._filter_empty)

    def get_pages(self) -> PureIter[IO[DataPage[ExtUserId]]]:
        getter: IntIndexGetter[DataPage[ExtUserId]] = IntIndexGetter(
            self.get_page
        )
        pages = (
            infinite_range(0, 1)
            .chunked(10)
            .map(lambda i: tuple(i))
            .map(getter.get_pages)
        ).map(lambda io_items: io_items.map(lambda i: from_flist(i)))
        return io_transform.until_empty(io_transform.chain(pages))

    def get_ids(self) -> PureIter[IO[ExtUserId]]:
        return io_transform.chain(
            self.get_pages().map(
                lambda i: i.map(lambda p: from_flist(p.items))
            )
        )

    def get(self, user: ExtUserId) -> IO[ExternalUser]:
        query = _queries.ExtUserQuery(Transform(_from_raw.to_user), user).query
        return self._client.get(query)
