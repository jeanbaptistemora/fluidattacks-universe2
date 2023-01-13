from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from mailchimp_transactional import (
    Client,
)
from tap_mandrill.api.export import (
    export_api_1,
    ExportApi,
)


@dataclass(frozen=True)
class ApiKey:
    _raw: str

    def __repr__(self) -> str:
        return "[masked-api-key]"


def _new_raw_client(key: ApiKey) -> Client:  # type: ignore[no-any-unimported]
    return Client(key._raw)  # type: ignore[misc]


@dataclass(frozen=True)  # type: ignore[misc]
class _ApiClient:  # type: ignore[no-any-unimported]
    client: Client  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ApiClient:
    _inner: _ApiClient

    @staticmethod
    def new(key: ApiKey) -> ApiClient:
        return ApiClient(
            _ApiClient(_new_raw_client(key))  # type: ignore[misc]
        )

    def export_api(self) -> ExportApi:
        return export_api_1(self._inner.client)  # type: ignore[misc]
