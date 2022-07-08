from schedulers.numerator_report_digest import (
    get_variation,
)


def test_get_variation() -> None:
    assert get_variation(10, 10) == 0.0
    assert get_variation(0, 10) == 0.0
    assert get_variation("0", 10) == 0.0
    assert get_variation(10, 0) == -100.0
    assert get_variation(10, 10.555) == 5.55
