# -*- coding: utf-8 -*-

"""This module allows to check Web.config code vulnerabilities."""

# standard imports
import os
from typing import List, Tuple

# 3rd party imports
from bs4 import BeautifulSoup
from bs4.element import Tag

# local imports
from fluidasserts import Unit, LOW, MEDIUM, OPEN, CLOSED, UNKNOWN, SAST
from fluidasserts.utils.generic import get_sha256, get_paths
from fluidasserts.utils.decorators import api

# Constants
ENDSWITH: Tuple[str] = ('.config',)


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

    exclude = tuple(exclude) if exclude else tuple()
    for path in get_paths(webconf_dest, endswith=ENDSWITH, exclude=exclude):
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


@api(risk=MEDIUM, kind=SAST)
def has_ssl_disabled(apphostconf_dest: str, exclude: list = None) -> tuple:
    """
    Check if SSL is disabled in ``ApplicationHost.config``.

    Search for access tag in security section in an ``ApplicationHost.config``
    source file or package.

    :param apphostconf_dest: Path to an ``ApplicationHost.config``
                             source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(apphostconf_dest):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'XML has not a tag to enable SSL'
    msg_closed: str = 'XML has a tag to enable SSL'

    vulns: List[Unit] = []
    safes: List[Unit] = []

    exclude = tuple(exclude) if exclude else tuple()
    for path in get_paths(
            apphostconf_dest, endswith=ENDSWITH, exclude=exclude):
        with open(path, 'r', encoding='latin-1') as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="xml")

        vulnerable: bool = True

        for custom_headers in soup('security'):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get('sslFlags', 'None')
                    if tag_name == 'access' and tag_value != 'None':
                        vulnerable = False

        unit: Unit = Unit(
            where=path,
            source=f'XML/Tag/security/access/sslFlags',
            specific=[msg_open if vulnerable else msg_closed],
            fingerprint=get_sha256(path))

        (vulns if vulnerable else safes).append(unit)

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=LOW, kind=SAST)
def has_debug_enabled(webconf_dest: str, exclude: list = None) -> tuple:
    """
    Check if debug flag is enabled in Web.config.

    Search for debug tag in compilation section in a Web.config source file
    or package.

    :param webconf_dest: Path to a Web.config source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(webconf_dest):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'XML has a tag to enable debugging'
    msg_closed: str = 'XML has not a tag to enable debugging'

    vulns: List[Unit] = []
    safes: List[Unit] = []

    exclude = tuple(exclude) if exclude else tuple()
    for path in get_paths(webconf_dest, endswith=ENDSWITH, exclude=exclude):
        with open(path, 'r', encoding='latin-1') as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="xml")

        vulnerable: bool = False

        for custom_headers in soup('system.web'):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get('debug', 'false')
                    if tag_name == 'compilation' and tag_value == 'true':
                        vulnerable = True

        unit: Unit = Unit(
            where=path,
            source=f'XML/Tag/system.web/compilation/debug',
            specific=[msg_open if vulnerable else msg_closed],
            fingerprint=get_sha256(path))

        (vulns if vulnerable else safes).append(unit)

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=LOW, kind=SAST)
def not_custom_errors(webconf_dest: str, exclude: list = None) -> tuple:
    """
    Check if customErrors flag is set to off in Web.config.

    CWE-12: ASP.NET Misconfiguration: Missing Custom Error Page

    :param webconf_dest: Path to a Web.config source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(webconf_dest):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'XML has a tag to disable custom error pages'
    msg_closed: str = 'XML has not a tag to disable custom error pages'

    vulns: List[Unit] = []
    safes: List[Unit] = []

    exclude = tuple(exclude) if exclude else tuple()
    for path in get_paths(webconf_dest, endswith=ENDSWITH, exclude=exclude):
        with open(path, 'r', encoding='latin-1') as file_desc:
            soup = BeautifulSoup(file_desc.read(), features="xml")

        vulnerable: bool = False

        for custom_headers in soup('system.web'):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get('mode', 'RemoteOnly')
                    if tag_name == 'customErrors' and tag_value == 'Off':
                        vulnerable = True

        unit: Unit = Unit(
            where=path,
            source=f'XML/Tag/system.web/customErrors/mode',
            specific=[msg_open if vulnerable else msg_closed],
            fingerprint=get_sha256(path))

        (vulns if vulnerable else safes).append(unit)

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes
