# Standard library
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Union,
)


class ContentSecurityPolicyHeader(NamedTuple):
    name: str

    directives: Dict[str, List[str]]


class StrictTransportSecurityHeader(NamedTuple):
    name: str

    include_sub_domains: Optional[bool]
    max_age: int
    preload: Optional[bool]


class ReferrerPolicyHeader(NamedTuple):
    name: str
    values: List[str]


Header = Optional[Union[
    ContentSecurityPolicyHeader,
    ReferrerPolicyHeader,
    StrictTransportSecurityHeader,
]]
