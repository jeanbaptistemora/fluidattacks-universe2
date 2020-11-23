# Standard libraries
import json
import tempfile
# Third party libraries
import pytest
from zoho_crm_etl import auth
from zoho_crm_etl.auth import Credentials
# Local libraries


def test_to_credentials():
    file = tempfile.TemporaryFile('w+')
    test_file_data = {
        'client_id': 'client_1',
        'client_secret': 'the_secret',
        'refresh_token': 'super_rtoken',
    }
    file.write(json.dumps(test_file_data))
    file.seek(0)
    result = auth.to_credentials(file)
    expected = Credentials('client_1', 'the_secret', 'super_rtoken')
    assert result == expected


@pytest.mark.skip(
    reason="need manual intervention to retrieve the access code"
)
def test_generate_refresh_token():
    pass


@pytest.mark.skip(
    reason="need real credentials and can invalidate other tokens"
)
def test_generate_token():
    pass
