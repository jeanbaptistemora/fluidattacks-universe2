from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
    ResultE,
)


class InvalidPage(Exception):
    pass


@dataclass(frozen=True)
class _Page:
    page_num: int
    per_page: int


@dataclass(frozen=True)
class Page(_Page):
    def __init__(self, obj: _Page) -> None:
        super().__init__(obj.page_num, obj.per_page)

    @staticmethod
    def new_page(page_num: int, per_page: int) -> ResultE[Page]:
        if page_num > 0 and per_page in range(1, 101):
            pag = Page(_Page(page_num, per_page))
            return Result.success(pag)
        return Result.failure(InvalidPage())
