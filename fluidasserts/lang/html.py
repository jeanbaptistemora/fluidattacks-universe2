# -*- coding: utf-8 -*-

"""This module allows to check HTML vulnerabilities."""

# standard imports
import os
import re
from typing import List

# 3rd party imports
from bs4 import BeautifulSoup
from bs4.element import Tag
from pyparsing import (makeHTMLTags, CaselessKeyword, ParseException,
                       Literal, SkipTo, stringEnd)

# local imports
from fluidasserts import Unit, OPEN, CLOSED, UNKNOWN, LOW, MEDIUM, SAST
from fluidasserts.utils.generic import get_paths, get_sha256
from fluidasserts.utils.decorators import api


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
    with open(filename, 'r', encoding='latin-1') as handle:
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
    return '/' + '/'.join(components)


@api(risk=LOW, kind=SAST)
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
        return UNKNOWN, 'File does not exist'

    msg_open: str = 'HTML file has autocomplete enabled'
    msg_closed: str = 'HTML file has autocomplete disabled'

    with open(filename, 'r', encoding='latin-1') as file_desc:
        html_obj = BeautifulSoup(file_desc.read(), features="html.parser")

    vulnerabilities: list = []
    for obj in html_obj('input'):
        autocomplete_enabled: bool = obj.get('autocomplete', 'on') != 'off'
        is_input_enabled: bool = obj.get('disabled', '') != ''
        is_input_type_sensitive: bool = obj.get('type', 'text') in (
            # autocomplete only works with these:
            #   https://www.w3schools.com/tags/att_input_autocomplete.asp
            'checkbox', 'date', 'datetime-local', 'email', 'month',
            'password', 'search', 'tel', 'text', 'time', 'url', 'week')
        if autocomplete_enabled \
                and is_input_enabled \
                and is_input_type_sensitive:
            vulnerabilities.append(_get_xpath(obj))

    for obj in html_obj('form'):
        if obj.attrs.get('autocomplete', 'on') != 'off':
            vulnerabilities.append(_get_xpath(obj))

    units: List[Unit] = [
        Unit(where=filename,
             source='XPath',
             specific=vulnerabilities,
             fingerprint=get_sha256(filename))]

    if vulnerabilities:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=LOW, kind=SAST)
def is_cacheable(filename: str) -> tuple:
    """Check if cache is possible.

    Verifies if the file has the tags::
       <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> and
       <META HTTP-EQUIV="Expires" CONTENT="-1">

    :param filename: Path to the ``HTML`` source.
    :returns: True if tag ``meta`` have attributes ``http-equiv``
              and ``content`` set as specified, False otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(filename):
        return UNKNOWN, 'File does not exist'

    msg_open: str = 'HTML file has miss-configured Pragma/Expires meta tags'
    msg_closed: str = 'HTML file has well configured Pragma/Expires meta tags'

    tag = 'meta'
    tk_pragma = CaselessKeyword('pragma')
    tk_nocache = CaselessKeyword('no-cache')
    pragma_attrs = {'http-equiv': tk_pragma,
                    'content': tk_nocache}

    tk_expires = CaselessKeyword('expires')
    tk_minusone = CaselessKeyword('-1')
    expires_attrs = {'http-equiv': tk_expires,
                     'content': tk_minusone}

    has_pragma = _has_attributes(filename, tag, pragma_attrs)
    has_expires = _has_attributes(filename, tag, expires_attrs)

    vulnerable: bool = not has_pragma or not has_expires

    units: List[Unit] = [
        Unit(where=filename,
             source='HTML/Meta/Configuration',
             specific=[msg_open if vulnerable else msg_closed],
             fingerprint=get_sha256(filename))]

    if vulnerable:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


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
        return UNKNOWN, 'File does not exist'

    msg_open: str = 'HTML file has a bad configured Content-Type meta tag'
    msg_closed: str = 'HTML file has a well configured Content-Type meta tag'

    tag = 'meta'
    tk_content = CaselessKeyword('content')
    tk_type = CaselessKeyword('type')
    prs_cont_typ = tk_content + Literal('-') + tk_type

    tk_type = SkipTo(Literal('/'), include=True)
    tk_subtype = SkipTo(Literal(';'), include=True)
    prs_mime = tk_type + tk_subtype

    tk_charset = CaselessKeyword('charset')
    tk_charset_value = SkipTo(stringEnd)
    prs_charset = tk_charset + Literal('=') + tk_charset_value

    prs_content_val = prs_mime + prs_charset

    attrs = {'http-equiv': prs_cont_typ,
             'content': prs_content_val}

    has_content_type = _has_attributes(filename, tag, attrs)

    units: List[Unit] = [
        Unit(where=filename,
             source='HTML/Meta/Content-Type',
             specific=[msg_closed if has_content_type else msg_open],
             fingerprint=get_sha256(filename))]

    if not has_content_type:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=LOW, kind=SAST)
def has_reverse_tabnabbing(path: str) -> tuple:
    r"""
    Check if an HTML file has links vulnerable to a reverse tabnabbing.

    :param path: Path to the ``HTML`` source.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(path):
        return UNKNOWN, 'File does not exist'

    vulns, safes = [], []
    http_re = re.compile("^http(s)?://")

    for file_path in get_paths(path, endswith=('.html',)):
        with open(file_path, 'r', encoding='latin-1') as file_desc:
            html_obj = BeautifulSoup(file_desc.read(), features="html.parser")

        _vulns = Unit(where=file_path,
                      source='XPath',
                      specific=[],
                      fingerprint=get_sha256(file_path))
        _safes = Unit(where=file_path,
                      source='XPath',
                      specific=[],
                      fingerprint=get_sha256(file_path))

        for ahref in html_obj.findAll('a', attrs={'href': http_re}):
            parsed: dict = {
                'href': ahref.get('href'),
                'target': ahref.get('target'),
                'rel': ahref.get('rel'),
            }

            if parsed['href'] and parsed['target'] == '_blank' \
                    and (not parsed['rel'] or 'noopener' not in parsed['rel']):
                _vulns.specific.append(_get_xpath(ahref))
            else:
                _safes.specific.append(_get_xpath(ahref))

        if _vulns.specific:
            vulns.append(_vulns)
        if _safes.specific:
            safes.append(_safes)

    if vulns:
        msg = 'There are a href tags susceptible to reverse tabnabbing'
        return OPEN, msg, vulns, safes
    msg = 'No a href tags were found'
    if safes:
        msg = 'There are no a href tags susceptible to reverse tabnabbing'
    return CLOSED, msg, vulns, safes


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
        return UNKNOWN, 'File does not exist'

    msg_open = 'HTML file does not implement Subresource Integrity Checks'
    msg_closed = 'HTML file does implement Subresource Integrity Checks'

    units: List[Unit] = []
    vulnerabilities: list = []
    for file_path in get_paths(path, endswith=('.html',)):
        with open(file_path, 'r', encoding='latin-1') as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="html.parser")

        for elem_types in ('link', 'script'):
            for elem in soup(elem_types):
                does_not_have_integrity: bool = \
                    elem.get('integrity') is None

                if elem_types == 'link':
                    references_external_resource: bool = \
                        elem.get('href', '').startswith('http')
                elif elem_types == 'script':
                    references_external_resource = \
                        elem.get('src', '').startswith('http')

                if does_not_have_integrity and references_external_resource:
                    vulnerabilities.append(_get_xpath(elem))

        units.append(
            Unit(where=file_path,
                 source='XPath',
                 specific=vulnerabilities,
                 fingerprint=get_sha256(file_path)))

    if vulnerabilities:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units
