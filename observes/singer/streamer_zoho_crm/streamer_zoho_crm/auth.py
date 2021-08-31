from getpass import (
    getpass,
)
import json
import logging
from postgres_client.connection import (
    Credentials as DbCredentials,
    DatabaseID,
)
import requests  # type: ignore
from typing import (
    Any,
    AnyStr,
    Dict,
    FrozenSet,
    IO,
    NamedTuple,
    Tuple,
)

ACCOUNTS_URL = "https://accounts.zoho.com"  # for US region
LOG = logging.getLogger(__name__)


class Credentials(NamedTuple):
    client_id: str
    client_secret: str
    refresh_token: str
    scopes: FrozenSet[str]


def to_credentials(auth_file: IO[AnyStr]) -> Credentials:
    auth = json.load(auth_file)
    auth["scopes"] = frozenset(auth["scopes"])
    return Credentials(**auth)


def generate_refresh_token(credentials: Credentials) -> Dict[str, str]:
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token"
    LOG.info(
        "Generating refresh token with scopes: %s",
        ",".join(credentials.scopes),
    )
    LOG.info("Paste grant token:")
    grant_token_code = getpass()
    data = {
        "grant_type": "authorization_code",
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "code": grant_token_code,
    }
    response = requests.post(url=endpoint, data=data)
    return dict(response.json())


def revoke_refresh_token() -> Dict[str, str]:
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token/revoke"
    refresh_token = getpass("Refresh token to revoke:")
    params = {"token": refresh_token}
    response = requests.post(url=endpoint, params=params)
    return dict(response.json())


def generate_token(credentials: Credentials) -> Dict[str, Any]:
    LOG.info("Generating access token")
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token"
    params = {
        "refresh_token": credentials.refresh_token,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "grant_type": "refresh_token",
    }
    response = requests.post(url=endpoint, params=params)
    return dict(response.json())


def to_db_credentials(
    auth_file: IO[AnyStr],
) -> Tuple[DatabaseID, DbCredentials]:
    auth = json.load(auth_file)
    auth["db_name"] = auth["dbname"]
    db_id_raw = dict(
        filter(lambda x: x[0] in DatabaseID._fields, auth.items())
    )
    creds_raw = dict(
        filter(lambda x: x[0] in DbCredentials._fields, auth.items())
    )
    return (DatabaseID(**db_id_raw), DbCredentials(**creds_raw))
