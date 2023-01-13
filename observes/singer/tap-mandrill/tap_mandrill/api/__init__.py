from ._api_key import (
    ApiKey,
)
from .export import (
    export_api_1,
    ExportApi,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class ApiClient:
    _key: ApiKey

    def export_api(self) -> ExportApi:
        return export_api_1(self._key)


__all__ = ["ApiKey"]
