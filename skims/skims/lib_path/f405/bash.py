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


def excessive_privileges_for_others(
    content: str, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        for index, lines in enumerate(content.splitlines(), 1):
            if "chmod" in lines:
                for item in lines.split(" "):
                    if re.match(r"^\d{3}$", item) and not item.endswith("0"):
                        yield index, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_root.f405.excessive_privileges_for_others",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.BASH_EXCESSIVE_PRIVILEGES_FOR_OTHERS,
    )
