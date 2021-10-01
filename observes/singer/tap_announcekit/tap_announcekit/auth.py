import base64
from cachetools import (
    cached,
    LRUCache,
)
from dataclasses import (
    dataclass,
)
from os import (
    environ,
)
from typing import (
    cast,
    Dict,
)

# maxsize can be float but int is inferred
_cache: LRUCache = LRUCache(maxsize=cast(int, float("inf")))


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


@cached(cache=_cache)
def get_creds() -> Creds:
    # environ returns IO type; inf. cache ensures purity
    return Creds(environ["ANNOUNCEKIT_USER"], environ["ANNOUNCEKIT_PASSWD"])
