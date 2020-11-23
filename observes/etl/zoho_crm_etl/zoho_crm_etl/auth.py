# Standard libraries
import json
from getpass import getpass
from typing import (
    Any,
    Dict,
    NamedTuple,
)
# Third party libraries
import requests
# Local libraries


ACCOUNTS_URL = 'https://accounts.zoho.com'  # for US region


class Credentials(NamedTuple):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REFRESH_TOKEN: str


def to_credentials(auth_file) -> Credentials:
    auth = json.load(auth_file)
    return Credentials(
        CLIENT_ID=auth['client_id'],
        CLIENT_SECRET=auth['client_secret'],
        REFRESH_TOKEN=auth['refresh_token'],
    )


def generate_refresh_token(
    credentials: Credentials
) -> Dict[str, str]:
    endpoint = f'{ACCOUNTS_URL}/oauth/v2/token'
    grant_token_code = getpass('Grant token:')
    data = {
        'grant_type': 'authorization_code',
        'client_id': credentials.CLIENT_ID,
        'client_secret': credentials.CLIENT_SECRET,
        'code': grant_token_code
    }
    response = requests.post(url=endpoint, data=data)
    return response.json()


def generate_token(credentials: Credentials) -> Dict[str, Any]:
    endpoint = f'{ACCOUNTS_URL}/oauth/v2/token'
    params = {
        'refresh_token': credentials.REFRESH_TOKEN,
        'client_id': credentials.CLIENT_ID,
        'client_secret': credentials.CLIENT_SECRET,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url=endpoint, params=params)
    return response.json()
