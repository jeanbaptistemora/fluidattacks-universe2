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
)
from purity.v1.pure_iter.transform import (
    chain,
    until_empty,
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
from tap_announcekit.objs.post.feedback import (
    FeedbackObj,
    FeedbackPage,
)
from tap_announcekit.streams.feedback._factory._query import (
    FeedbackPageQuery,
)


@dataclass(frozen=True)
class FeedbackFactory:
    client: ApiClient

    @staticmethod
    def _filter_empty(page: FeedbackPage) -> Maybe[FeedbackPage]:
        return Maybe.from_optional(page if len(page.items) > 0 else None)

    def get_page(self, proj: ProjectId, page: int) -> IO[Maybe[FeedbackPage]]:
        query = FeedbackPageQuery(page).query(proj)
        return self.client.get(query).map(self._filter_empty)

    def get_feedbacks(
        self, proj: ProjectId, p_range: IO[range]
    ) -> IO[PureIter[FeedbackObj]]:
        getter: IntIndexGetter[FeedbackPage] = IntIndexGetter(
            partial(self.get_page, proj)
        )
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        id_pages = (
            p_range.bind(getter.get_pages)
            .map(lambda x: from_flist(x))
            .map(lambda x: until_empty(x))
            .map(lambda p: p.map(lambda i: i.items))
            .map(lambda x: chain(x.map(lambda i: from_flist(i))))
        )
        return id_pages
