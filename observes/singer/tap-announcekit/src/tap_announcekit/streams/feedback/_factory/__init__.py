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
    Query,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.objs.post.feedback import (
    FeedbackObj,
)
from tap_announcekit.streams.feedback._factory import (
    _from_raw,
    _queries,
)
from typing import (
    Union,
)


def _feedback_page_query(
    id_obj: Union[ProjectId, PostId], page: int
) -> Query[DataPage[FeedbackObj]]:
    return _queries.FeedbackPageQuery(
        Transform(partial(_from_raw.to_page, id_obj)), id_obj, page
    ).query


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
        query = _feedback_page_query(proj, page)
        return self.client.get(query).map(self._filter_empty)

    def get_feedbacks(self, proj: ProjectId) -> PureIter[IO[FeedbackObj]]:
        getter: IntIndexGetter[DataPage[FeedbackObj]] = IntIndexGetter(
            partial(self.get_page, proj)
        )
        return io_transform.chain(
            getter.get_until_end(0, 10).map(
                lambda i: i.map(lambda x: from_flist(x.items))
            )
        )
