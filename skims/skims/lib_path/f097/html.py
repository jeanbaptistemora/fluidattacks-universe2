# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from bs4 import (
    BeautifulSoup,
)
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


def has_reverse_tabnabbing(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        r"""
        Check if an HTML file has links vulnerable to a reverse tabnabbing.

        :param path: Path to the ``HTML`` source.
        :rtype: :class:`fluidasserts.Result`
        """
        http_re = re.compile("^http(s)?://")

        html_obj = BeautifulSoup(content, features="html.parser")

        for ahref in html_obj.findAll("a", attrs={"href": http_re}):
            parsed: dict = {
                "href": ahref.get("href"),
                "target": ahref.get("target"),
                "rel": ahref.get("rel"),
            }

            if (
                parsed["href"]
                and parsed["target"] == "_blank"
                and (not parsed["rel"] or "noopener" not in parsed["rel"])
            ):
                yield ahref.sourceline, ahref.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f097.has_reverse_tabnabbing",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_HAS_REVERSE_TABNABBING,
    )
