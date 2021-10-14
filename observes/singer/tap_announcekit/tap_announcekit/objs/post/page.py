from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
)
from tap_announcekit.objs.id_objs import (
    PostId,
)


@dataclass(frozen=True)
class _PostIdPage:
    data: FrozenList[PostId]
    count: int
    page: int
    pages: int


class PostIdPage(_PostIdPage):
    # pylint: disable=too-few-public-methods
    def __init__(self, obj: _PostIdPage) -> None:
        super().__init__(
            obj.data,
            obj.count,
            obj.page,
            obj.pages,
        )
