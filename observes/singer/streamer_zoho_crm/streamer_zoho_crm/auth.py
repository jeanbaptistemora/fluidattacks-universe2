# Standard libraries
import json
from getpass import getpass
from typing import (
    Any,
    AnyStr,
    Dict,
    IO,
    NamedTuple,
    Tuple,
)
# Third party libraries
import requests
# Local libraries
from postgres_client.connection import (
    DatabaseID,
    Credentials as DbCredentials,
)
from streamer_zoho_crm import utils


ACCOUNTS_URL = 'https://accounts.zoho.com'  # for US region
LOG = utils.get_log(__name__)


class Credentials(NamedTuple):
    client_id: str
    client_secret: str
    refresh_token: str


def to_credentials(
    auth_file: IO[AnyStr]
) -> Credentials:
    auth = json.load(auth_file)
    return Credentials(**auth)


def generate_refresh_token(
    credentials: Credentials
) -> Dict[str, str]:
    endpoint = f'{ACCOUNTS_URL}/oauth/v2/token'
    grant_token_code = getpass('Grant token:')
    data = {
        'grant_type': 'authorization_code',
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'code': grant_token_code
    }
    response = requests.post(url=endpoint, data=data)
    return dict(response.json())


def revoke_refresh_token() -> Dict[str, str]:
    endpoint = f'{ACCOUNTS_URL}/oauth/v2/token/revoke'
    refresh_token = getpass('Refresh token to revoke:')
    params = {'token': refresh_token}
    response = requests.post(url=endpoint, params=params)
    return dict(response.json())


def generate_token(credentials: Credentials) -> Dict[str, Any]:
    LOG.info('Generating access token')
    endpoint = f'{ACCOUNTS_URL}/oauth/v2/token'
    params = {
        'refresh_token': credentials.refresh_token,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url=endpoint, params=params)
    return dict(response.json())


def to_db_credentials(
    auth_file: IO[AnyStr]
) -> Tuple[DatabaseID, DbCredentials]:
    auth = json.load(auth_file)
    auth['db_name'] = auth['dbname']
    db_id_raw = dict(
        filter(lambda x: x[0] in DatabaseID._fields, auth.items())
    )
    creds_raw = dict(
        filter(lambda x: x[0] in DbCredentials._fields, auth.items())
    )
    return (DatabaseID(**db_id_raw), DbCredentials(**creds_raw))
