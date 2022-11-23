from paginator.int_index import (
    build_getter,
    get_pages,
    get_until_end,
    new_page_range,
    PageId,
    PageOrAll,
    PageRange,
)
from paginator.pages import (
    AllPages,
    Limits,
)

__version__ = "1.0.0"
__all__ = [
    "AllPages",
    "PageId",
    "PageOrAll",
    "PageRange",
    "Limits",
    "build_getter",
    "get_pages",
    "get_until_end",
    "new_page_range",
]
