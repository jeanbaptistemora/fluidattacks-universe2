# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    Pattern,
    Tuple,
)

WS = r"\s*"
WSM = r"\s+"
HEADER_BASIC: Pattern[str] = re.compile(
    r"\<stringProp\sname\=\"Header.value\"\>Basic\s.+\<\/stringProp\>"
)


def jmx_header_basic(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.search(
                HEADER_BASIC,
                line,
            ):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f015.jmx_header_basic",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.JMX_HEADER_BASIC,
    )
