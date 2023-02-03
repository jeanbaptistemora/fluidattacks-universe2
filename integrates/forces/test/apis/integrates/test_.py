from forces.apis.integrates import (
    get_api_token,
    INTEGRATES_API_TOKEN,
    set_api_token,
)
import pytest


@pytest.mark.first
def test_get_api_token() -> None:
    with pytest.raises(LookupError):
        get_api_token()


@pytest.mark.last
def test_set_api_token(test_token: str) -> None:
    set_api_token(test_token)
    assert INTEGRATES_API_TOKEN.get() == test_token
