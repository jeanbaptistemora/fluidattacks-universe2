from typing import (
    Any,
    NamedTuple,
)

Item = dict[str, Any]


class PrimaryKey(NamedTuple):
    partition_key: str
    sort_key: str


class Facet(NamedTuple):
    attrs: tuple[str, ...]
    pk_alias: str
    sk_alias: str


class Index(NamedTuple):
    name: str
    primary_key: PrimaryKey


class Table(NamedTuple):
    facets: dict[str, Facet]
    indexes: dict[str, Index]
    name: str
    primary_key: PrimaryKey


class PageInfo(NamedTuple):
    has_next_page: bool
    end_cursor: str


class QueryResponse(NamedTuple):
    items: tuple[Item, ...]
    page_info: PageInfo
