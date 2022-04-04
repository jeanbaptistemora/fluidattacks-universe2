from json import (
    loads,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)


def creds_from_str(raw: str) -> Credentials:
    data = loads(raw)
    return Credentials(
        str(data["user"]),
        str(data["password"]),
    )


def id_from_str(raw: str) -> DatabaseID:
    data = loads(raw)
    return DatabaseID(
        str(data["name"]),
        str(data["host"]),
        int(str(data["port"])),
    )
