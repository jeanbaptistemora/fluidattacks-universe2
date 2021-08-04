import base64
from dataclasses import (
    dataclass,
)
from typing import (
    Dict,
)


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
        return {"Authorization": f"Bearer {b64_payload}"}
