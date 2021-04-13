# Standard library
from typing import (
    List,
    NamedTuple,
    Optional,
    Union,
)


class StrictTransportSecurityHeader(NamedTuple):
    name: str

    include_sub_domains: Optional[bool]
    max_age: int
    preload: Optional[bool]


class ReferrerPolicyHeader(NamedTuple):
    name: str
    values: List[str]


Header = Optional[Union[
    StrictTransportSecurityHeader,
]]
