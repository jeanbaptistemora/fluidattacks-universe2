import pytest
from schedulers.update_sca_table.repositories.advisories_community import (
    format_range,
    RE_RANGES,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "ranges,expected",
    [
        ("[5.0.0,6.0.0)[6.0.0,6.0.4]", ["[5.0.0,6.0.0)", "[6.0.0,6.0.4]"]),
        ("(,0.3.13]", ["(,0.3.13]"]),
        ("[1.1.4]", ["[1.1.4]"]),
        ("12345]", []),
    ],
)
def test_re_ranges_pattern(ranges: str, expected: list[str]) -> None:
    match_ranges: list[str] = RE_RANGES.findall(ranges)
    assert match_ranges == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str,expected",
    [
        ("[5.0.0,6.0.0)", ">=5.0.0 <6.0.0"),
        ("(,0.3.13]", ">=0 <=0.3.13"),
        ("[1.1.4]", "=1.1.4"),
    ],
)
def test_advs_format_range(range_str: str, expected: str) -> None:
    formated_range: str = format_range(range_str)
    assert formated_range == expected
