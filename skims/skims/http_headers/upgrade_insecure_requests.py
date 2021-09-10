from http_headers.types import (
    UpgradeInsecureRequestsHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_upgrade_insecure_requests(name: str) -> bool:
    return name.lower() == "upgrade-insecure-requests"


def parse(line: str) -> Optional[UpgradeInsecureRequestsHeader]:
    # upgrade-insecure-requests: 1

    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name = portions.pop(0)

    if not _is_upgrade_insecure_requests(name) or not portions:
        return None

    value = portions.pop(0)

    if value != "1":
        return None

    return UpgradeInsecureRequestsHeader(
        name=name,
        value=value,
    )
