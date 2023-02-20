from app.app import (
    APP,
)


def test_should_intialize() -> None:
    assert APP is not None
