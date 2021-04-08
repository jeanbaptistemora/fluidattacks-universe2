# Standard library
from typing import (
    NamedTuple,
    Optional,
    Union,
)


class StrictTransportSecurityHeader(NamedTuple):
    name: str

    include_sub_domains: Optional[bool]
    max_age: int
    preload: Optional[bool]


Header = Optional[Union[
    StrictTransportSecurityHeader,
]]
