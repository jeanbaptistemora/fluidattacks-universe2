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
from tap_announcekit.objs.activity import (
    ActivityObj,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.activities._factory._from_raw import (
    to_page,
)
from tap_announcekit.streams.activities._factory._queries import (
    ActivitiesQuery,
)


@dataclass(frozen=True)
class ActivityFactory:
    client: ApiClient
    proj: ProjectId

    def get_page(self, page: int) -> IO[Maybe[DataPage[ActivityObj]]]:
        query = ActivitiesQuery(
            Transform(partial(to_page, self.proj)), self.proj, page
        ).query
        return self.client.get(query).map(
            lambda page: Maybe.from_optional(
                page if len(page.items) > 0 else None
            )
        )

    def get_activities(self) -> PureIter[IO[ActivityObj]]:
        getter: IntIndexGetter[DataPage[ActivityObj]] = IntIndexGetter(
            self.get_page
        )
        return io_transform.chain(
            getter.get_until_end(0, 10).map(
                lambda i: i.map(lambda x: from_flist(x.items))
            )
        )
