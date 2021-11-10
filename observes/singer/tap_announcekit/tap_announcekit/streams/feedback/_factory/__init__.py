from dataclasses import (
    dataclass,
)
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    PureIter,
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
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.objs.post.feedback import (
    FeedbackObj,
)
from tap_announcekit.streams.feedback._factory._query import (
    FeedbackPageQuery,
)


@dataclass(frozen=True)
class FeedbackFactory:
    client: ApiClient

    @staticmethod
    def _filter_empty(
        page: DataPage[FeedbackObj],
    ) -> Maybe[DataPage[FeedbackObj]]:
        return Maybe.from_optional(page if len(page.items) > 0 else None)

    def get_page(
        self, proj: ProjectId, page: int
    ) -> IO[Maybe[DataPage[FeedbackObj]]]:
        query = FeedbackPageQuery(page).query(proj)
        return self.client.get(query).map(self._filter_empty)

    def get_feedbacks(self, proj: ProjectId) -> PureIter[IO[FeedbackObj]]:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        getter: IntIndexGetter[DataPage[FeedbackObj]] = IntIndexGetter(
            partial(self.get_page, proj)
        )
        pages = (
            infinite_range(0, 1)
            .chunked(10)
            .map(lambda i: tuple(i))
            .map(getter.get_pages)
        ).map(
            lambda io_items: io_items.map(
                lambda i: from_flist(i).map(lambda p: p.map(lambda x: x.items))
            )
        )
        result = io_transform.until_empty(io_transform.chain(pages)).map(
            lambda i: i.map(lambda j: from_flist(j))
        )
        return io_transform.chain(result)
