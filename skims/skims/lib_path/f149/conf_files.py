# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Iterator,
    Tuple,
)


def network_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("network"):
            if (
                isinstance(tag, Tag)
                and (tag_value := tag.attrs.get("enablessl"))
                and tag_value.lower() == "false"
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f149.xml_network_ssl_disabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_NETWORK_SSL_DISABLED,
    )
