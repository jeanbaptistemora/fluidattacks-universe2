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


def bash_using_sshpass(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.match(r"(\s+|^)sshpass -p", line):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f176.common",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.BASH_USING_SSHPASS,
    )
