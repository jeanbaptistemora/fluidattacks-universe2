from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class Dashboard:
    checks_per_page: int
    custom_domain: str
    custom_url: str
    description: str
    favicon: str
    header: str
    hide_tags: bool
    link: str
    logo: str
    paginate: bool
    pagination_rate: int
    refresh_rate: int
    use_tags_and_operator: bool
    width: str
