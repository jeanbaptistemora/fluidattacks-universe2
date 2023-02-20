from collections.abc import (
    Iterator,
)


def iter_with_next(
    values: list[str], last: str | None
) -> Iterator[tuple[str, str | None]]:
    for value, next_value in zip(values, values[1:]):
        yield value, next_value
    yield values[-1], last
