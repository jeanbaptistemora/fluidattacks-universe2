# Standard libraries
import json
import tempfile
# Third party libraries
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
