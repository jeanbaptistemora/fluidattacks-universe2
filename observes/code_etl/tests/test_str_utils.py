from code_etl.str_utils import (
    utf8_byte_truncate,
)


def test_multibyte_chars() -> None:
    raw = "🍉🍀🧙"
    assert utf8_byte_truncate(raw, 4 * 3) == raw
    assert utf8_byte_truncate(raw, 10) == "🍉🍀"
    assert utf8_byte_truncate(raw, 4 * 2) == "🍉🍀"
    assert utf8_byte_truncate(raw, 6) == "🍉"
    assert utf8_byte_truncate(raw, 2) == ""


def test_single_byte_chars() -> None:
    raw = "fooo"
    assert utf8_byte_truncate(raw, 4) == raw
    assert utf8_byte_truncate(raw, 2) == "fo"
    assert utf8_byte_truncate(raw, 0) == ""
