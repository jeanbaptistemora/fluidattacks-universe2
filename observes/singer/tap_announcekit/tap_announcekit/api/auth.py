import base64
from cachetools import (  # type: ignore
    cached,
)
from dataclasses import (
    dataclass,
)
from os import (
    environ,
)
from typing import (
    Callable,
    cast,
    Dict,
)

USER_ENV_VAR = "ANNOUNCEKIT_USER"
PASSWD_ENV_VAR = "ANNOUNCEKIT_PASSWD"


@dataclass(frozen=True)
class Creds:
    user: str
    passwd: str

    def __str__(self) -> str:
        return "__masked__"

    def basic_auth_header(self) -> Dict[str, str]:
        encoding = "UTF-8"
        payload = ":".join([self.user, self.passwd])
        b64_payload = base64.b64encode(payload.encode(encoding)).decode(
            encoding
        )
        return {"Authorization": f"Basic {b64_payload}"}


@cached(cache={})
def _get_creds() -> Creds:
    # environ returns IO type; inf. cache ensures purity
    return Creds(environ[USER_ENV_VAR], environ[PASSWD_ENV_VAR])


get_creds = cast(Callable[[], Creds], _get_creds)
