# -*- coding: utf-8 -*-

"""This module allows to check HTML vulnerabilities."""


from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from fluidasserts import (
    CLOSED,
    LOW,
    MEDIUM,
    OPEN,
    SAST,
    Unit,
    UNKNOWN,
)
from fluidasserts.utils.decorators import (
    api,
)
from fluidasserts.utils.generic import (
    get_paths,
    get_sha256,
)
import os
from pyparsing import (
    CaselessKeyword,
    Literal,
    makeHTMLTags,
    Optional,
    ParseException,
    Regex,
    SkipTo,
    stringEnd,
)
import re
from typing import (
    List,
)


def _has_attributes(filename: str, tag: str, attrs: dict) -> bool:
    """
    Check ``HTML`` attributes` values.

    This method checks whether the tag (``tag``) inside the code file
    (``filename``) has attributes (``attr``) with the specific values.

    :param filename: Path to the ``HTML`` source.
    :param tag: ``HTML`` tag to search.
    :param attrs: Attributes with values to search.
    :returns: True if attribute set as specified, False otherwise.
    """
    with open(filename, "r", encoding="latin-1") as handle:
        html_doc = handle.read()

        tag_s, _ = makeHTMLTags(tag)
        tag_expr = tag_s

        result = False

        for expr in tag_expr.searchString(html_doc):
            for attr, value in attrs.items():
                try:
                    value.parseString(getattr(expr, attr))
                    result = True
                except ParseException:
                    result = False
                    break
            if result:
                break
        return result


def _get_xpath(tag: Tag) -> str:
    """Return the xpath of a BeautifulSoup Tag."""
    # Inspiration from https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
    components = []
    child = tag if tag.name else tag.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        if len(siblings) == 1:
            components.append(child.name)
        else:
            for sibling_no, sibling in enumerate(siblings, 1):
                if sibling is child:
                    components.append(sibling_no)
                    break
        child = parent
    components.reverse()
    return "/" + "/".join(components)


@api(risk=LOW, kind=SAST)
def is_header_content_type_missing(filename: str) -> tuple:
    """Check if Content-Type header is missing.

    Verifies if the file has the tags::
       <META HTTP-EQUIV="Content-Type" CONTENT="no-cache">

    :param filename: Path to the ``HTML`` source.
    :returns: True if tag ``meta`` have attributes ``http-equiv``
              and ``content`` set as specified, False otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(filename):
        return UNKNOWN, "File does not exist"

    msg_open: str = "HTML file has a bad configured Content-Type meta tag"
    msg_closed: str = "HTML file has a well configured Content-Type meta tag"

    tag = "meta"
    tk_content = CaselessKeyword("content")
    tk_type = CaselessKeyword("type")
    prs_cont_typ = tk_content + Literal("-") + tk_type

    tk_type = SkipTo(Literal("/"), include=True)
    tk_subtype = Optional(SkipTo(Literal(";"), include=True))
    prs_mime = tk_type + tk_subtype

    tk_charset = CaselessKeyword("charset")
    tk_charset_value = SkipTo(stringEnd)
    prs_charset = tk_charset + Literal("=") + tk_charset_value

    prs_content_val = prs_mime + prs_charset

    attrs = {"http-equiv": prs_cont_typ, "content": prs_content_val}

    has_content_type = _has_attributes(filename, tag, attrs)

    if not has_content_type:
        attrs = {"http-equiv": prs_cont_typ, "content": prs_mime}

        valid = _has_attributes(filename, tag, attrs)
        if valid:
            attrs = {"charset": Regex(r"[A-Za-z_][A-Za-z_0-9]*")}
            has_content_type = _has_attributes(filename, tag, attrs)

    units: List[Unit] = [
        Unit(
            where=filename,
            source="HTML/Meta/Content-Type",
            specific=[msg_closed if has_content_type else msg_open],
            fingerprint=get_sha256(filename),
        )
    ]

    if not has_content_type:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=MEDIUM, kind=SAST)
def has_not_subresource_integrity(path: str) -> tuple:
    r"""
    Check if elements fetched by the provided HTML have `SRI`.

    See: `Documentation <https://developer.mozilla.org/en-US/
    docs/Web/Security/Subresource_Integrity>`_.

    :param path: Path to the ``HTML`` source.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(path):
        return UNKNOWN, "File does not exist"

    msg_open = "HTML file does not implement Subresource Integrity Checks"
    msg_closed = "HTML file does implement Subresource Integrity Checks"

    units: List[Unit] = []
    vulnerabilities: list = []
    for file_path in get_paths(path, endswith=(".html",)):
        with open(file_path, "r", encoding="latin-1") as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="html.parser")

        for elem_types in ("link", "script"):
            for elem in soup(elem_types):
                does_not_have_integrity: bool = elem.get("integrity") is None

                if elem_types == "link":
                    references_external_resource: bool = elem.get(
                        "href", ""
                    ).startswith("http")
                elif elem_types == "script":
                    references_external_resource = elem.get(
                        "src", ""
                    ).startswith("http")

                if does_not_have_integrity and references_external_resource:
                    vulnerabilities.append(_get_xpath(elem))

        units.append(
            Unit(
                where=file_path,
                source="XPath",
                specific=vulnerabilities,
                fingerprint=get_sha256(file_path),
            )
        )

    if vulnerabilities:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units
