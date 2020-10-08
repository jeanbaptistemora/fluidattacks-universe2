# Third-party libraries
import pytest
from _pytest.logging import LogCaptureFixture
from gql import gql

# Local libraries
from integrates.domain import get_vulnerable_lines
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


def test_get_vulnerable_lines(
    test_integrates_api_token: str,
    test_integrates_session: None,
) -> None:
    vulnerabilities = get_vulnerable_lines('unittesting')
    assert len(vulnerabilities) > 0


def test_bad_query(
    caplog: LogCaptureFixture,
    test_integrates_api_token: str,
    test_integrates_session: None
) -> None:
    vulnerabilities = get_vulnerable_lines('')
    assert vulnerabilities == []
    assert 'Exception: TransportQueryError' in caplog.text
