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
