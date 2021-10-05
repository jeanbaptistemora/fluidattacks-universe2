from paginator.v2 import (
    IntIndexGetter,
)
import pytest
from random import (
    randint,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)

max_pages = 10


def mock_page(page: int) -> IO[Maybe[int]]:
    print(f"called {page}")
    item = randint(0, 10) if page <= max_pages else None
    return IO(Maybe.from_optional(item))


@pytest.mark.timeout(1)
def test_until_end() -> None:
    getter = IntIndexGetter(mock_page)
    data = getter.get_until_end(1, 5)
    assert sum(1 for _ in data) == sum(1 for _ in data)
    assert sum(1 for _ in data) == max_pages
