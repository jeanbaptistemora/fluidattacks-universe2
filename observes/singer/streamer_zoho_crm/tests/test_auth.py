# Standard libraries
import json
import tempfile
# Third party libraries
import pytest
from streamer_zoho_crm import auth
from streamer_zoho_crm.auth import Credentials
# Local libraries


def test_to_credentials() -> None:
    file = tempfile.TemporaryFile('w+')
    test_file_data = {
        'client_id': 'client_1',
        'client_secret': 'the_secret',
        'refresh_token': 'super_rtoken',
        'scopes': ['s1', 's2']
    }
    file.write(json.dumps(test_file_data))
    file.seek(0)
    result = auth.to_credentials(file)
    expected = Credentials(
        'client_1',
        'the_secret',
        'super_rtoken',
        frozenset(['s1', 's2'])
    )
    assert result == expected


@pytest.mark.skip(
    reason="need manual intervention to retrieve the access code"
)  # type: ignore
def test_generate_refresh_token() -> None:
    pass


@pytest.mark.skip(
    reason="need real credentials and can invalidate other tokens"
)  # type: ignore
def test_generate_token() -> None:
    pass
