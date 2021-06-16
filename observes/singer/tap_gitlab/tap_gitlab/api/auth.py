from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    api_key: str

    def __repr__(self) -> str:
        return "Creds(api_key=[masked])"
