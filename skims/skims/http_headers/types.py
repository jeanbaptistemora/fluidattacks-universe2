from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class AcceptHeader(NamedTuple):
    name: str
    value: str


class ContentEncodingHeader(NamedTuple):
    name: str
    value: str


class ContentSecurityPolicyHeader(NamedTuple):
    name: str

    directives: dict[str, list[str]]


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

    include_sub_domains: bool | None
    max_age: int
    preload: bool | None


class ReferrerPolicyHeader(NamedTuple):
    name: str
    values: list[str]


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


class XCacheHeader(NamedTuple):
    name: str
    value: str


class XContentTypeOptionsHeader(NamedTuple):
    name: str
    value: str


class XFrameOptionsHeader(NamedTuple):
    name: str
    value: str


Header = (
    AcceptHeader
    | ContentEncodingHeader
    | ContentSecurityPolicyHeader
    | DateHeader
    | ReferrerPolicyHeader
    | StrictTransportSecurityHeader
    | UpgradeInsecureRequestsHeader
    | XXSSProtectionHeader
    | XCacheHeader
    | XContentTypeOptionsHeader
    | XFrameOptionsHeader
    | SetCookieHeader
    | None
)
