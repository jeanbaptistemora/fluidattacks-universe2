from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from collections.abc import (
    Iterator,
    Set,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.utilities.xml import (
    get_attribute_line,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)


def get_insecure_attr(tag: Tag, insecure_names: Set[str]) -> str | None:
    for insecure_name in insecure_names:
        if (
            insecure_conf := tag.attrs.get(insecure_name)
        ) and insecure_conf.lower() == "true":
            return insecure_name

    if (
        tag.name == "preferance"
        and (attr_name := tag.attrs.get("name"))
        and attr_name.lower() == "android-usescleartexttraffic"
        and (attr_value := tag.attrs.get("value"))
        and attr_value.lower() == "true"
    ):
        return "android-usescleartexttraffic"
    return None


def insecure_configuration(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
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
            if isinstance(tag, Tag) and (
                danger_attr := get_insecure_attr(tag, insecure_configurations)
            ):
                if attr_line := get_attribute_line(tag, content, danger_attr):
                    line_no = attr_line
                else:
                    line_no = tag.sourceline
                col_no: int = tag.sourcepos

                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f403.insecure_configuration",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_INSECURE_CONFIGURATION,
    )
