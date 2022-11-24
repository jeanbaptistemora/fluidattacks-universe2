from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)


def iter_with_next(
    values: List[str], last: Optional[str]
) -> Iterable[Tuple[str, Optional[str]]]:
    for value, next_value in zip(values, values[1:]):
        yield value, next_value
    yield values[-1], last
