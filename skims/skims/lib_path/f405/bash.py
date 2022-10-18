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
    Tuple,
)


def not_suppress_vuln_header(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for lines in content.splitlines():
            if lines.startswith("chmod"):
                for index, item in enumerate(lines.split(" ")):
                    if re.match(r"^\d{3}$", item) and not item.endswith("0"):
                        yield index, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.dotnetconfig.not_suppress_vuln_header",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_NOT_SUPPRESS_VULN_HEADER,
    )
