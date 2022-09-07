# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

import paginator
from paginator import (
    PageId,
)
from typing import (
    Callable,
    Iterator,
    Type,
    TypeVar,
)

ResultPage = TypeVar("ResultPage")


def get_all_pages(
    _type: Type[ResultPage],
    get_page: Callable[[PageId], ResultPage],
    is_empty: Callable[[ResultPage], bool],
) -> Iterator[ResultPage]:
    getter = paginator.build_getter(_type, get_page, is_empty)
    pages: Iterator[ResultPage] = paginator.get_until_end(
        _type, PageId(1, 100), getter, 10
    )
    return pages
