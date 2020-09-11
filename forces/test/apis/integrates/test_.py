# Third party libraries
import pytest

# Local libraries
from forces.apis.integrates import (
    set_api_token,
    get_api_token,
    get_api_token_email,
    get_api_token_group,
    INTEGRATES_API_TOKEN
)


@pytest.mark.first  # type: ignore
def test_get_api_token() -> None:
    try:
        get_api_token()
        assert False
    except LookupError:
        assert True


@pytest.mark.last  # type: ignore
def test_set_api_token(test_token: str) -> None:
    set_api_token(test_token)
    assert INTEGRATES_API_TOKEN.get() == test_token


@pytest.mark.last  # type: ignore
def test_get_api_token_email(test_token: str) -> None:
    set_api_token(test_token)
    assert get_api_token_email() == 'forces.herrin@fluidattacks.com'


@pytest.mark.last  # type: ignore
def test_get_api_token_group(test_token: str) -> None:
    set_api_token(test_token)
    assert get_api_token_group() == 'herrin'
