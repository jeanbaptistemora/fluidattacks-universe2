from datetime import (
    datetime,
)
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


class DateHeader(NamedTuple):
    name: str
    date: datetime


class SetCookieHeader(NamedTuple):
    name: str

    raw_content: str
    cookie_name: str
    cookie_value: str
    secure: bool
    httponly: bool
    samesite: str


class StrictTransportSecurityHeader(NamedTuple):
    name: str

    include_sub_domains: Optional[bool]
    max_age: int
    preload: Optional[bool]


class ReferrerPolicyHeader(NamedTuple):
    name: str
    values: List[str]


class UpgradeInsecureRequestsHeader(NamedTuple):
    name: str
    value: str


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
        DateHeader,
        ReferrerPolicyHeader,
        StrictTransportSecurityHeader,
        UpgradeInsecureRequestsHeader,
        XXSSProtectionHeader,
        XContentTypeOptionsHeader,
        XFrameOptionsHeader,
    ]
]
