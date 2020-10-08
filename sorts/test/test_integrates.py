# Third-party libraries
import pytest
from gql import gql

# Local libraries
from integrates.graphql import client as graphql_client


def test_bad_client() -> None:
    with pytest.raises(RuntimeError):
        with graphql_client():
            pass  # pragma: no cover


def test_client(
    test_integrates_api_token: str,
    test_integrates_session: None,
) -> None:
    with graphql_client() as client:
        assert client.transport.headers == {
            'Authorization': f'Bearer {test_integrates_api_token}'
        }
