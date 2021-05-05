from operator import (
    methodcaller,
)
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
)


def parse_key_value(
    is_header: Callable[[str], bool],
    line: str,
) -> Optional[Tuple[str, str]]:
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not is_header(name):
        return None

    if len(portions) != 2:
        return None

    return name, value
