# Standard library
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)

from http_headers.types import (
    XXSSProtectionHeader,
)


def _is_x_xss_protection(name: str) -> bool:
    return name.lower() == 'x-xss-protection'


def _parse_mode(token: str) -> str:
    portions = token.split('=', maxsplit=1)

    if len(portions) == 2:
        return portions[1].strip()
    return ''


def parse(line: str) -> Optional[XXSSProtectionHeader]:
    # X-XSS-Protection: 0
    # X-XSS-Protection: 1
    # X-XSS-Protection: 1; mode=block
    # X-XSS-Protection: 1; report=<reporting-uri>
    portions: List[str] = line.split(':', maxsplit=1)
    portions = list(map(methodcaller('strip'), portions))

    if len(portions) != 2:
        return None

    name, value = portions

    if not _is_x_xss_protection(name):
        return None

    enabled: bool = False
    mode: str = ''

    portions = value.split(';')
    portions = list(map(methodcaller('strip'), portions))
    portions = list(map(methodcaller('lower'), portions))

    for portion in portions:
        if portion == '0':
            enabled = False
        elif portion == '1':
            enabled = True
        elif portion.startswith('mode'):
            mode = _parse_mode(portion)

    return XXSSProtectionHeader(
        name=name,
        enabled=enabled,
        mode=mode,
    )
