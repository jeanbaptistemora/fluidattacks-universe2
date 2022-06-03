from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
import os


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


def has_not_autocomplete(filename: str) -> tuple:
    """
    Check if *input* or *form* tags have *autocomplete* attribute set to *off*.

    It's known that *form* tags may have the *autocomplete* attribute set
    to *on* and specific *input* tags have it set to *off*. However, this
    check enforces a defensive and explicit approach,
    forcing every *input* and *form* tag to have the *autocomplete* attribute
    set to *off* in order to mark the result as CLOSED.

    :param filename: Path to the *HTML* source.
    :returns: True if ALL tags *form* and *input* have attribute
              *autocomplete* set to *off* (*on* is de default value),
              False otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(filename):
        return "UNKNOWN", "File does not exist"

    with open(filename, "r", encoding="latin-1") as file_desc:
        html_obj = BeautifulSoup(file_desc.read(), features="html.parser")

    vulnerabilities: list = []
    for obj in html_obj("input"):
        autocomplete_enabled: bool = obj.get("autocomplete", "on") != "off"
        is_input_enabled: bool = obj.get("disabled", "") != ""
        is_input_type_sensitive: bool = obj.get("type", "text") in (
            # autocomplete only works with these:
            #   https://www.w3schools.com/tags/att_input_autocomplete.asp
            "checkbox",
            "date",
            "datetime-local",
            "email",
            "month",
            "password",
            "search",
            "tel",
            "text",
            "time",
            "url",
            "week",
        )
        if (
            autocomplete_enabled
            and is_input_enabled
            and is_input_type_sensitive
        ):
            vulnerabilities.append(_get_xpath(obj))

    for obj in html_obj("form"):
        if obj.attrs.get("autocomplete", "on") != "off":
            vulnerabilities.append(_get_xpath(obj))

    return "Null", "Testing"
