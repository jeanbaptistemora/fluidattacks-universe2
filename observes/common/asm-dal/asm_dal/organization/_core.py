from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity.result import (
    Result,
    ResultE,
)
import re


@dataclass(frozen=True)
class _OrganizationId:
    uuid: str
    name: str


@dataclass(frozen=True)
class OrganizationId:
    _inner: _OrganizationId

    @property
    def uuid(self) -> str:
        return self._inner.uuid

    @property
    def name(self) -> str:
        return self._inner.name

    @staticmethod
    def new(uuid: str, name: str) -> ResultE[OrganizationId]:
        _name = name.removeprefix("ORG#")
        _uuid = uuid.removeprefix("ORG#")
        if not _name.isalnum():
            err = ValueError(f"Org name is not alphanum i.e. {_name}")
            return Result.failure(err)
        UUIDv4 = "^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"
        if re.match(UUIDv4, _uuid, re.I) is None:
            err = ValueError(f"Org id is not an UUIDv4 i.e. {_uuid}")
            return Result.failure(err)

        return Result.success(_OrganizationId(_uuid, _name), Exception).map(
            OrganizationId
        )
