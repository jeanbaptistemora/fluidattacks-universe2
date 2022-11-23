from purity.v2.result import (
    Result,
)
from purity.v2.union import (
    inl,
    inr,
)
from typing import (
    Union,
)


def test_use_case_1() -> None:
    value = 245
    some: Result[int, str] = Result.success(value)
    result = (
        some.map(lambda i: i + 1)
        .bind(lambda i: Result.failure(f"fail {i}", int))
        .map(lambda i: i + 1)
        .alt(lambda x: f"{x} alt")
    )
    assert result.unwrap_fail() == f"fail {value + 1} alt"


def test_result_with_union() -> None:
    value = "hi"
    result: Result[Union[str, int], None] = Result.failure(None, int).map(inl)
    result_2 = result.lash(
        lambda _: Result.success(value, type(None)).map(inr)
    )
    assert result_2.unwrap() == value
