from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from purity.v1 import (
    JsonFactory,
)


def creds_from_str(raw: str) -> Credentials:
    data = JsonFactory.loads(raw)
    return Credentials(
        data["user"].to_primitive(str),
        data["password"].to_primitive(str),
    )


def id_from_str(raw: str) -> DatabaseID:
    data = JsonFactory.loads(raw)
    return DatabaseID(
        data["name"].to_primitive(str),
        data["host"].to_primitive(str),
        int(data["port"].to_primitive(str)),
    )
