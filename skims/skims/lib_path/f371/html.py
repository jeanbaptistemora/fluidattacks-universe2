from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    has_attributes,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    CaselessKeyword,
    Literal,
    Optional,
    Regex,
    SkipTo,
    stringEnd,
)


def is_header_content_type_missing(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """Check if Content-Type header is missing.

        Verifies if the file has the tags::
        <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">

        """
        tag = "meta"
        tk_content = CaselessKeyword("content")
        tk_type = CaselessKeyword("type")
        prs_cont_typ = tk_content + Literal("-") + tk_type

        tk_type = SkipTo(Literal("/"), include=True)  # type: ignore
        tk_subtype = Optional(SkipTo(Literal(";"), include=True))
        prs_mime = tk_type + tk_subtype

        tk_charset = CaselessKeyword("charset")
        tk_charset_value = SkipTo(stringEnd)
        prs_charset = tk_charset + Literal("=") + tk_charset_value

        prs_content_val = prs_mime + prs_charset

        attrs = {"http-equiv": prs_cont_typ, "content": prs_content_val}

        has_content_type = has_attributes(content, tag, attrs)

        if not has_content_type:
            attrs = {"http-equiv": prs_cont_typ, "content": prs_mime}
            valid = has_attributes(content, tag, attrs)
            if valid:
                attrs = {"charset": Regex(r"[A-Za-z_][A-Za-z_0-9]*")}
                has_content_type = has_attributes(content, tag, attrs)

        if not has_content_type:
            line: int = 0
            column: int = 0
            yield line, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f371.is_header_content_type_missing",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_IS_HEADER_CONTENT_TYPE_MISSING,
    )
