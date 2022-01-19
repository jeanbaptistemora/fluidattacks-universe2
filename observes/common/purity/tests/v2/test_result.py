from purity.v2.result import (
    Result,
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
