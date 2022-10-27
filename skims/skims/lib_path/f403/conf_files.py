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
    Set,
    Tuple,
)


def check_insecure_configuration(tag: Tag, insecure_names: Set[str]) -> bool:
    for insecure_name in insecure_names:
        if (
            insecure_conf := tag.attrs.get(insecure_name)
        ) and insecure_conf.lower() == "true":
            return True

    if (
        tag.name == "preferance"
        and (attr_name := tag.attrs.get("name"))
        and attr_name.lower() == "android-usescleartexttraffic"
        and (attr_value := tag.attrs.get("value"))
        and attr_value.lower() == "true"
    ):
        return True
    return False


def insecure_configuration(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        vulnerable_tags = {
            "application",
            "domain-config",
            "base-config",
            "preferance",
        }
        insecure_configurations = {
            "cleartexttrafficpermitted",
            "android:usescleartexttraffic",
        }
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all(vulnerable_tags):
            if isinstance(tag, Tag) and check_insecure_configuration(
                tag, insecure_configurations
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos

                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f403.insecure_configuration",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_INSECURE_CONFIGURATION,
    )
