# Standard libraries
import json
from getpass import getpass
from typing import (
    Any,
    AnyStr,
    Dict,
    IO,
    NamedTuple,
)
# Third party libraries
import requests
# Local libraries
from postgres_client.connection import ConnectionID

ACCOUNTS_URL = 'https://accounts.zoho.com'  # for US region


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


def generate_token(credentials: Credentials) -> Dict[str, Any]:
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
) -> ConnectionID:
    auth = json.load(auth_file)
    return ConnectionID(**auth)
