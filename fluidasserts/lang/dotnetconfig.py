# -*- coding: utf-8 -*-

"""This module allows to check Web.config code vulnerabilities."""

# standard imports
import os
from copy import copy
from typing import List

# 3rd party imports
from bs4 import BeautifulSoup
from bs4.element import Tag
from pyparsing import makeXMLTags, withAttribute, htmlComment

# local imports
from fluidasserts import Unit, LOW, OPEN, CLOSED, UNKNOWN, SAST
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256, get_paths
from fluidasserts.utils.decorators import notify, level, track, api


LANGUAGE_SPECS = {
    'extensions': ('config',),
    'block_comment_start': '<!--',
    'block_comment_end': '-->',
}  # type: dict


def _get_block(file_lines, line) -> str:
    """
    Return a DotNetConfig block of code beginning in line.

    :param file_lines: Lines of code
    :param line: First line of block
    """
    return "".join(file_lines[line - 1:])


@api(risk=LOW, kind=SAST)
def is_header_x_powered_by_present(webconf_dest: str,
                                   exclude: list = None) -> tuple:
    """
    Search for X-Powered-By headers in a Web.config source file or package.

    :param webconf_dest: Path to a Web.config source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(webconf_dest):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'XML has not a tag to remove X-Powered-By'
    msg_closed: str = 'XML has a tag to remove X-Powered-By'

    vulns: List[Unit] = []
    safes: List[Unit] = []

    endswith = LANGUAGE_SPECS['extensions']
    exclude = tuple(exclude) if exclude else tuple()
    for path in get_paths(webconf_dest, endswith=endswith, exclude=exclude):
        with open(path, 'r', encoding='latin-1') as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="xml")

        has_remove_banner: bool = False

        for custom_headers in soup('customHeaders'):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get('name')
                    if tag_name == 'remove' and tag_value == 'X-Powered-By':
                        has_remove_banner = True

        vulnerable: bool = not has_remove_banner

        unit: Unit = Unit(
            where=path,
            source=f'XML/Tag/customHeaders/remove/X-Powered-By',
            specific=[msg_open if vulnerable else msg_closed],
            fingerprint=get_sha256(path))

        (vulns if vulnerable else safes).append(unit)

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@notify
@level('medium')
@track
def has_ssl_disabled(apphostconf_dest: str, exclude: list = None) -> bool:
    """
    Check if SSL is disabled in ``ApplicationHost.config``.

    Search for access tag in security section in an ``ApplicationHost.config``
    source file or package.

    :param apphostconf_dest: Path to an ``ApplicationHost.config``
                             source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_tag_s, _ = makeXMLTags('security')
    tk_access, _ = makeXMLTags('access')
    tag_no_comm = tk_access.ignore(htmlComment)
    tk_access_none = copy(tag_no_comm)
    tk_access_none.setParseAction(withAttribute(sslFlags='None'))
    result = False
    try:
        sec_tag = lang.check_grammar(tk_tag_s, apphostconf_dest,
                                     LANGUAGE_SPECS, exclude)
        if not sec_tag:
            show_unknown('Not files matched',
                         details=dict(code_dest=apphostconf_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=apphostconf_dest))
        return False
    access_tags = {}
    none_sslflags = {}
    for code_file, val in sec_tag.items():
        access_tags.update(lang.block_contains_grammar(tk_access,
                                                       code_file,
                                                       val['lines'],
                                                       _get_block))

        none_sslflags.update(lang.block_contains_grammar(tk_access_none,
                                                         code_file,
                                                         val['lines'],
                                                         _get_block))
    if not access_tags or none_sslflags:
        show_open('SSL is disabled',
                  details=dict(matched=access_tags if
                               access_tags else none_sslflags))
        result = True
    else:
        show_close('SSL is enabled',
                   details=dict(file=apphostconf_dest,
                                fingerprint=get_sha256(apphostconf_dest)))
    return result


@notify
@level('low')
@track
def has_debug_enabled(webconf_dest: str, exclude: list = None) -> bool:
    """
    Check if debug flag is enabled in Web.config.

    Search for debug tag in compilation section in a Web.config source file
    or package.

    :param webconf_dest: Path to a Web.config source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_tag_s, _ = makeXMLTags('system.web')
    tk_compilation, _ = makeXMLTags('compilation')
    tag_no_comm = tk_compilation.ignore(htmlComment)
    tk_comp_debug = copy(tag_no_comm)
    tk_comp_debug.setParseAction(withAttribute(debug='true'))
    result = False
    try:
        sysweb_tag = lang.check_grammar(tk_tag_s, webconf_dest,
                                        LANGUAGE_SPECS, exclude)
        if not sysweb_tag:
            show_unknown('Not files matched',
                         details=dict(code_dest=webconf_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=webconf_dest))
        return False

    debug_tags = {}
    for code_file, val in sysweb_tag.items():
        debug_tags.update(lang.block_contains_grammar(tk_comp_debug,
                                                      code_file,
                                                      val['lines'],
                                                      _get_block))
    if debug_tags:
        show_open('Debug is enabled',
                  details=dict(matched=debug_tags,
                               total_lines=len(sysweb_tag)))
        result = True
    else:
        show_close('Debug is disabled',
                   details=dict(file=webconf_dest,
                                fingerprint=get_sha256(webconf_dest)))
    return result


@notify
@level('low')
@track
def not_custom_errors(webconf_dest: str, exclude: list = None) -> bool:
    """
    Check if customErrors flag is set to off in Web.config.

    CWE-12: ASP.NET Misconfiguration: Missing Custom Error Page

    :param webconf_dest: Path to a Web.config source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_tag_s, _ = makeXMLTags('system.web')
    tk_custom_errors, _ = makeXMLTags('customErrors')
    tag_no_comm = tk_custom_errors.ignore(htmlComment)
    tk_comp_custom_errors = copy(tag_no_comm)
    tk_comp_custom_errors.setParseAction(withAttribute(mode='Off'))
    result = False
    try:
        sysweb_tag = lang.check_grammar(tk_tag_s, webconf_dest,
                                        LANGUAGE_SPECS, exclude)
        if not sysweb_tag:
            show_unknown('Not files matched',
                         details=dict(code_dest=webconf_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=webconf_dest))
        return False

    vulns = {}
    for code_file, val in sysweb_tag.items():
        vulns.update(lang.block_contains_grammar(tk_comp_custom_errors,
                                                 code_file,
                                                 val['lines'],
                                                 _get_block))
    if vulns:
        show_open('Custom errors are not enabled',
                  details=dict(matches=vulns,
                               total_lines=len(sysweb_tag)))
        result = True
    else:
        show_close('Custom errors are enabled',
                   details=dict(file=webconf_dest,
                                fingerprint=get_sha256(webconf_dest)))
    return result
