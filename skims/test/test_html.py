import pytest
from utils.html import (
    is_html,
)


@pytest.mark.skims_test_group("unittesting")
def test_is_html() -> None:
    assert not is_html("test")
    assert not is_html("{}")
    assert not is_html('{"json": true}')
    assert not is_html('\n\n\n\n\n {"json": "<html>test</html>"}')
    assert is_html("<html><title>asdf</title></html>")
    assert is_html("<html><title>asdf")
    assert is_html("<!DOCTYPE html><html><title>asdf")
