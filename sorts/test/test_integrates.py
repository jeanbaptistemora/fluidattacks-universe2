# Third-party libraries
import pytest
from _pytest.logging import LogCaptureFixture

# Local libraries
from integrates.domain import get_vulnerable_lines
from integrates.graphql import client as graphql_client


def test_bad_client() -> None:
    with pytest.raises(RuntimeError):
        with graphql_client():
            pass  # pragma: no cover


@pytest.mark.usefixtures("test_integrates_session")
def test_client(test_integrates_api_token: str) -> None:
    with graphql_client() as client:
        assert client.transport.headers == {
            "Authorization": f"Bearer {test_integrates_api_token}"
        }


@pytest.mark.usefixtures(
    "test_integrates_api_token", "test_integrates_session"
)
def test_get_vulnerable_lines() -> None:
    vulnerabilities = get_vulnerable_lines("oneshottest")
    assert len(vulnerabilities) > 0


@pytest.mark.usefixtures(
    "test_integrates_api_token", "test_integrates_session"
)
def test_bad_query(caplog: LogCaptureFixture) -> None:
    vulnerabilities = get_vulnerable_lines("")
    assert vulnerabilities == []
    assert "Exception: TransportQueryError" in caplog.text
