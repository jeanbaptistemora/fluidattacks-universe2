import contextlib
from datetime import (
    datetime,
    timezone,
)
from http_headers.common import (
    parse_key_value,
)
from http_headers.types import (
    DateHeader,
)

# Date: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
FORMAT: str = "%a, %d %b %Y %H:%M:%S GMT"


def _is_date(name: str) -> bool:
    return name.lower() == "date"


def parse(line: str) -> DateHeader | None:
    if data := parse_key_value(
        is_header=_is_date,
        line=line,
    ):
        with contextlib.suppress(ValueError):
            return DateHeader(
                name=data[0],
                date=datetime.strptime(data[1], FORMAT).replace(
                    tzinfo=timezone.utc,
                ),
            )

    return None
