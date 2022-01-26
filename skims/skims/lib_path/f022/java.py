from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_java_properties import (
    load as load_java_properties,
)
from typing import (
    Iterator,
    Tuple,
)


#  developer: drestrepo@fluidattacks.com
def java_properties_unencrypted_transport(
    content: str, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        data = load_java_properties(
            content,
            include_comments=False,
            exclude_protected_values=True,
        )
        for line_no, (key, val) in data.items():
            val = val.lower()
            if (
                key
                and (val.startswith("http://") or val.startswith("ftp://"))
                and not (
                    "localhost" in val
                    or "127.0.0.1" in val
                    or "0.0.0.0" in val  # nosec
                )
            ):
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"319"},
        description_key="src.lib_path.f022.unencrypted_channel",
        finding=FindingEnum.F022,
        iterator=iterator(),
        path=path,
    )
