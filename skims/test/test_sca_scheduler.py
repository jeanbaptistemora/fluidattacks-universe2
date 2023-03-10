import pytest
from schedulers.update_sca_table.repositories.advisories_community import (
    _format_ranges,
    fix_npm_gem_go_range,
    fix_pip_composer_range,
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


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str,expected",
    [
        (">=3.1.0 <3.1.6||>=3.2.0 <3.2.6", ">=3.1.0 <3.1.6 || >=3.2.0 <3.2.6"),
        ("<5.2.4.4||>=6.0.0.0 <6.0.3.3", "<5.2.4.4 || >=6.0.0.0 <6.0.3.3"),
        (
            ">=5.0.0.alpha <5.0.0.beta1.1||>=4.2.0.alpha <4.2.5.1",
            ">=5.0.0.alpha <5.0.0.beta1.1 || >=4.2.0.alpha <4.2.5.1",
        ),
    ],
)
def test_fix_npm_gem_go_range(range_str: str, expected: str) -> None:
    formated_range: str = fix_npm_gem_go_range(range_str)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str,expected",
    [
        (">=4.0,<4.3||>=5.0,<5.2", ">=4.0 <4.3 || >=5.0 <5.2"),
        ("==3.1||>=4.0.0,<=4.0.2", "=3.1 || >=4.0.0 <=4.0.2"),
        (">=1.0,<=1.0.1", ">=1.0 <=1.0.1"),
    ],
)
def test_fix_pip_composer_range(range_str: str, expected: str) -> None:
    formated_range: str = fix_pip_composer_range(range_str)
    print(formated_range)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "parameters,expected",
    [
        (("pypi", ">=1.0,<=1.0.1"), ">=1.0 <=1.0.1"),
        (
            ("npm", "<5.2.4.4||>=6.0.0.0 <6.0.3.3"),
            "<5.2.4.4 || >=6.0.0.0 <6.0.3.3",
        ),
        (("maven", "[1.1.4]"), "=1.1.4"),
    ],
)
def test_format_ranges_internal(
    parameters: tuple[str, str], expected: str
) -> None:
    formated_range: str = _format_ranges(*parameters)
    print(formated_range)
    assert formated_range == expected
