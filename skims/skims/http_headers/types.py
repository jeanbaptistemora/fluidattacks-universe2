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


class WWWAuthenticate(NamedTuple):
    name: str

    charset: str
    realm: str
    type: str


class XXSSProtectionHeader(NamedTuple):
    name: str
    enabled: bool
    mode: str


class XContentTypeOptionsHeader(NamedTuple):
    name: str
    value: str


class XFrameOptionsHeader(NamedTuple):
    name: str
    value: str


Header = Optional[
    Union[
        ContentSecurityPolicyHeader,
        ReferrerPolicyHeader,
        StrictTransportSecurityHeader,
        XXSSProtectionHeader,
        XContentTypeOptionsHeader,
        XFrameOptionsHeader,
    ]
]
