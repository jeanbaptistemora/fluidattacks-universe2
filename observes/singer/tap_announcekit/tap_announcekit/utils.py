import json
from returns.io import (
    IO,
)
from sgqlc import (
    introspection,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
import sys
from tap_announcekit.api import (
    API_ENDPOINT,
)
from tap_announcekit.auth import (
    Creds,
)
from typing import (
    IO as IO_FILE,
)


def get_api_schema(creds: Creds, target: IO_FILE[str]) -> IO[None]:
    endpoint = HTTPEndpoint(API_ENDPOINT, creds.basic_auth_header)
    data = endpoint(
        introspection.query,
        introspection.variables(
            include_description=False,
            include_deprecated=False,
        ),
    )
    json.dump(data, target, sort_keys=True, indent=4, default=str)
    target.write("\n")
    if data.get("errors"):
        sys.exit(1)
    return IO(None)
