# -*- coding: utf-8 -*-

"""This module allows to check HTTP-specific vulnerabilities."""

# standard imports
import re
from time import sleep
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# 3rd party imports
from difflib import SequenceMatcher
from urllib.parse import parse_qsl
from pytz import timezone
from bs4 import BeautifulSoup
from viewstate import ViewState, ViewStateException
import ntplib

# local imports
from fluidasserts import Unit, OPEN, CLOSED, UNKNOWN, LOW, MEDIUM, HIGH, DAST
from fluidasserts.helper import http, banner
from fluidasserts.utils.decorators import api, unknown_if

# pylint: disable=too-many-lines

# Constants
DEFAULT_FIELD: str = 'HTTP/Implementation'

# This dictionary maps the header to a regex in which the value is secure
HDR_RGX: Dict[str, str] = {
    'access-control-allow-origin': '^https?:\\/\\/.*$',
    'cache-control': '(?=.*must-revalidate)(?=.*no-cache)(?=.*no-store)',
    'content-security-policy': '^([a-zA-Z]+\\-[a-zA-Z]+|sandbox).*$',
    'content-type': '^(\\s)*.+(\\/|-).+(\\s)*;(\\s)*charset.*$',
    'expires': '^\\s*0\\s*$',
    'pragma': '^\\s*no-cache\\s*$',
    'strict-transport-security': (r'^\s*max-age\s*=\s*'
                                  # 123 or "123" as a capture group
                                  r'"?((?<!")\d+(?!")|(?<=")\d+(?="))"?'
                                  r'\s*;\s*includeSubDomains'),
    'x-content-type-options': '^\\s*nosniff\\s*$',
    'x-frame-options': '^\\s*(deny|allow-from|sameorigin).*$',
    'server': '^[^0-9]*$',
    'x-permitted-cross-domain-policies': '^((?!all).)*$',
    'x-xss-protection': '^1(\\s*;\\s*mode=block)?$',
    'www-authenticate': '^((?!Basic).)*$',
    'x-powered-by': '^ASP.NET'
}

# Regex taken from SQLmap project
SQLI_ERROR_MSG: Set[str] = {
    r'SQL syntax.*MySQL',  # MySQL
    r'Warning.*mysql_.*',  # MySQL
    r'MySqlException \(0x',  # MySQL
    r'valid MySQL result',  # MySQL
    r'check the manual that corresponds to your (MySQL|MariaDB)',  # MySQL
    r'MySqlClient.',  # MySQL
    r'com.mysql.jdbc.exceptions',  # MySQL
    r'PostgreSQL.*ERROR',  # PostgreSQL
    r'Warning.*Wpg_.*',  # PostgreSQL
    r'valid PostgreSQL result',  # PostgreSQL
    r'Npgsql.',  # PostgreSQL
    r'PG::SyntaxError:',  # PostgreSQL
    r'org.postgresql.util.PSQLException',  # PostgreSQL
    r'ERROR:sssyntax error at or near ',  # PostgreSQL, MS SQL Server
    r'Driver.* SQL[-_ ]*Server',  # MS SQL Server
    r'OLE DB.* SQL Server',  # MS SQL Server
    r'\bSQL Server[^&lt;&quot;]+Driver',  # MS SQL Server
    r'Warning.*(mssql|sqlsrv)_',  # MS SQL Server
    r'\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}',  # MS SQL Server
    r'System.Data.SqlClient.SqlException',  # MS SQL Server
    r'(?s)Exception.*WRoadhouse.Cms.',  # MS SQL Server
    r'Microsoft SQL Native Client error \'[0-9a-fA-F]{8}',  # MS SQL Server
    r'com.microsoft.sqlserver.jdbc.SQLServerException',  # MS SQL Server
    r'ODBC SQL Server Driver',  # MS SQL Server
    r'SQLServer JDBC Driver',  # MS SQL Server
    r'macromedia.jdbc.sqlserver',  # MS SQL Server
    r'com.jnetdirect.jsql',  # MS SQL Server, Microsoft Access
    r'Microsoft Access (d+ )?Driver',  # Microsoft Access
    r'JET Database Engine',  # Microsoft Access
    r'Access Database Engine',  # Microsoft Access
    r'ODBC Microsoft Access',  # Microsoft Access
    r'Syntax error (missing operator) in query expression',  # MSAccess, Oracle
    r'\bORA-d{5}',  # Oracle
    r'Oracle error',  # Oracle
    r'Oracle.*Driver',  # Oracle
    r'Warning.*Woci_.*',  # Oracle
    r'Warning.*Wora_.*',  # Oracle
    r'oracle.jdbc.driver',  # Oracle
    r'quoted string not properly terminated',  # Oracle, IBM DB2
    r'CLI Driver.*DB2',  # IBM DB2
    r'DB2 SQL error',  # IBM DB2
    r'\bdb2_w+\(',  # IBM DB2
    r'SQLSTATE.+SQLCODE',  # IBM DB2, Informix
    r'Exception.*Informix',  # Informix
    r'Informix ODBC Driver',  # Informix
    r'com.informix.jdbc',  # Informix
    r'weblogic.jdbc.informix',  # Informix
    r'Dynamic SQL Error',  # Firebird
    r'Warning.*ibase_.*',  # Firebird, SQLite
    r'SQLite/JDBCDriver',  # SQLite
    r'SQLite.Exception',  # SQLite
    r'System.Data.SQLite.SQLiteException',  # SQLite
    r'Warning.*sqlite_.*',  # SQLite
    r'Warning.*SQLite3::',  # SQLite
    r'\[SQLITE_ERROR\]',  # SQLite
    r'SQL error.*POS([0-9]+).*',  # SAP MaxDB
    r'Warning.*maxdb.*',  # SAP MaxDB
    r'Warning.*sybase.*',  # Sybase
    r'Sybase message',  # Sybase
    r'Sybase.*Server message.*',  # Sybase
    r'SybSQLException',  # Sybase
    r'com.sybase.jdbc',  # Sybase
    r'Warning.*ingres_',  # Ingres
    r'Ingres SQLSTATE',  # Ingres
    r'IngresW.*Driver',  # Ingres
    r'Exception (condition )?d+. Transaction rollback.',  # Frontbase
    r'org.hsqldb.jdbc',  # HSQLDB
    r'Unexpected end of command in statement \[',  # HSQLDB
    r'Unexpected token.*in statement \[',  # HSQLDB
}


def _get_links(html_page: str) -> List:
    """Extract links from page."""
    soup = BeautifulSoup(html_page, features="html.parser")
    links = [x.get('href')
             for x in soup.findAll('a',
                                   attrs={'href':
                                          re.compile("^http(s)?://")})]
    return links


def _get_field(kwargs: Any) -> str:
    """Return the display field from kwargs or a default value."""
    kwargs = kwargs if isinstance(kwargs, dict) else {}
    return kwargs.pop('_field', DEFAULT_FIELD)


def _replace_dict_value(adict: dict, key: str, value: str) -> None:
    """
    Replace a `value` given a `key` in a complex dict.

    :param adict: Complex dict.
    :param key: Key of the value that is going to be replaced.
    :param value: Value to replace in dict where is the given key.
    """
    for rkey in adict.keys():
        if rkey == key:
            adict[rkey] = value
        elif isinstance(adict[rkey], dict):
            _replace_dict_value(adict[rkey], key, value)


def _create_dataset(field: str, value_list: List[str],
                    query_string: Union[str, dict]) -> List:
    """
    Create dataset from values in list.

    :param query_string: String or dict with query parameters.
    :param field: Field to be taken from each of the values.
    :param value_list: List of values from which fields are to be extracted.
    :return: A List containing incremental versions of a dict, which contains
             the data in the specified field from value_list.
    """
    dataset = []
    if isinstance(query_string, str):
        data_dict = dict(parse_qsl(query_string))
    else:
        data_dict = deepcopy(query_string)
    for value in value_list:
        _replace_dict_value(data_dict, field, value)
        dataset.append(deepcopy(data_dict))
    return dataset


def _request_dataset(url: str, dataset_list: List, *args, **kwargs) -> List:
    r"""
    Request datasets and gives the results in a list.

    :param url: URL to test.
    :param dataset_list: List of datasets. For each of these an ``HTTP``
       session is created and the response recorded in the returned list.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.

    Either ``params``, ``json`` or ``data`` must be present in ``kwargs``,
    if the request is ``GET`` or ``POST``, respectively.
    """
    kw_new = kwargs.copy()
    resp = list()
    qs_params = list(filter(kwargs.get,
                            ['data', 'json', 'params']))[0]
    for dataset in dataset_list:
        kw_new[qs_params] = dataset
        sess = http.HTTPSession(url, *args, **kw_new)
        resp.append((len(sess.response.text), sess.response.status_code))
    return resp


def _caseless_key_in_dict(index: str, dictionary: dict) -> bool:
    """Return True if index is a key of dictionary ignoring casing."""
    for key in dictionary:
        if isinstance(key, str) and index.lower() == key.lower():
            return True
    return False


def _caseless_indexing(index: str, dictionary: dict) -> Tuple[str, Any]:
    """Index a dicctionary by key without taking into account casing."""
    for key, val in dictionary.items():
        if isinstance(key, str) and index.lower() == key.lower():
            return key, val
    raise IndexError(f'{index} is not present on dictionary')


@unknown_if(http.ParameterError, http.ConnError)
def _has_method(url: str, method: str, *args, **kwargs) -> tuple:
    r"""
    Check if specific HTTP method is allowed in URL.

    :param url: URL to test.
    :param method: HTTP method to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    kwargs.update({'method': 'OPTIONS'})

    session = http.HTTPSession(url, *args, **kwargs)
    allow_header = session.response.headers.get('allow', '')

    method = method.upper()
    session.set_messages(
        source=f'HTTP/Request/{method}',
        msg_open=f'{method} method enabled',
        msg_closed=f'{method} method disabled')
    session.add_unit(
        is_vulnerable=method in allow_header)
    return session.get_tuple_result()


@unknown_if(http.ParameterError, http.ConnError)
def _is_header_present(url: str, header: str, *args, **kwargs) -> tuple:
    """
    Check if header is present in URL.

    :param url: URL to test.
    :param header: Header to test if present.
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'HTTP/Response/Headers/{header}',
        msg_open=f'Header {header} is present',
        msg_closed=f'Header {header} is not present')
    session.add_unit(
        is_vulnerable=header in session.response.headers)
    return session.get_tuple_result()


@unknown_if(http.ParameterError, http.ConnError)
def _has_insecure_value(url: str,
                        header: str,
                        vulnerable_if_missing: bool,
                        *args, **kwargs) -> tuple:
    """
    Check if header value is insecure.

    :param url: URL to test.
    :param header: Header to test if present and insecure.
    """
    session = http.HTTPSession(url, *args, **kwargs)
    missing: bool = True
    insecure: bool = True
    header_lower: str = header.lower()

    if _caseless_key_in_dict(header, session.response.headers):
        missing = False
        _, header_value = _caseless_indexing(header, session.response.headers)
        insecure = not re.match(
            pattern=HDR_RGX[header_lower],
            string=header_value,
            flags=re.IGNORECASE)

    if vulnerable_if_missing:
        if missing:
            session.set_messages(
                source=f'HTTP/Response/Headers/{header}',
                msg_open=f'{header} header is missing which is insecure',
                msg_closed=f'{header} header is present which is secure')
        else:
            session.set_messages(
                source=f'HTTP/Response/Headers/{header}',
                msg_open=f'{header} header is insecure',
                msg_closed=f'{header} header is secure')
        session.add_unit(
            is_vulnerable=missing or insecure)
        return session.get_tuple_result()

    session.set_messages(
        source=f'HTTP/Response/Headers/{header}',
        msg_open=f'{header} header has an insecure value',
        msg_closed=f'{header} header has a secure value')
    session.add_unit(
        is_vulnerable=not missing and insecure)
    return session.get_tuple_result()


@unknown_if(http.ParameterError, http.ConnError)
def _generic_has_multiple_text(url: str, regex_list: List[str],
                               *args, **kwargs) -> tuple:
    r"""
    Check if one of a list of bad texts is present.

    :param url: URL to test.
    :param regex_list: List of regexes to search.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    field: str = _get_field(kwargs)
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Response/Body',
        msg_open='Bad text is present in response',
        msg_closed='Bad text is not present in response')

    if session.response.status_code >= 500:
        return UNKNOWN, f'We got a {session.response.status_code} status code'

    is_vulnerable: bool = any(
        re.search(regex, session.response.text, re.IGNORECASE)
        for regex in regex_list)

    session.add_unit(
        is_vulnerable=is_vulnerable,
        specific=[field])
    return session.get_tuple_result()


@unknown_if(http.ParameterError, http.ConnError)
def _generic_has_text(url: str, text: str,
                      *args: Any, **kwargs: Any) -> tuple:
    r"""
    Check if a bad text is present.

    :param url: URL to test.
    :param text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    field: str = _get_field(kwargs)
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Response/Body',
        msg_open='Bad text is present in response',
        msg_closed='Bad text is not present in response')
    session.add_unit(
        is_vulnerable=re.search(text, session.response.text, re.IGNORECASE),
        specific=[field])
    return session.get_tuple_result()


@unknown_if(http.ParameterError, http.ConnError)
def _generic_has_not_text(url: str, text: str,
                          *args: Any, **kwargs: Any) -> tuple:
    r"""
    Check if a bad text is present.

    :param url: URL to test.
    :param text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    field: str = _get_field(kwargs)
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Response/Body',
        msg_open='Bad text is not present in response',
        msg_closed='Bad text is present in response')
    session.add_unit(
        is_vulnerable=not re.search(
            text, session.response.text, re.IGNORECASE),
        specific=[field])
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
def has_multiple_text(url: str, regex_list: List[str],
                      *args, **kwargs) -> tuple:
    r"""
    Check if one of a list of bad texts is present in URL response.

    :param url: URL to test.
    :param regex_list: List of regexes to search.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_multiple_text(url, regex_list, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def has_text(url: str, expected_text: str, *args: Any, **kwargs: Any) -> tuple:
    r"""
    Check if a bad text is present in URL response.

    :param url: URL to test.
    :param expected_text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expected_text, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def has_not_text(url: str, expected_text: str, *args, **kwargs) -> tuple:
    r"""
    Check if a required text is not present in URL response.

    :param url: URL to test.
    :param expected_text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_not_text(url, expected_text, *args, **kwargs)


@api(risk=LOW,
     kind=DAST,
     references=[
         ('https://blog.insiderattack.net/configuring-secure-iis'
          '-response-headers-in-asp-net-mvc-b38369030728'),
         'https://www.troyhunt.com/shhh-dont-let-your-response-headers/',
     ],
     standards={
         'CWE': '200',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N': 5.3,
     })
def is_header_x_asp_net_version_present(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-AspNet-Version header is missing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_header_present(url, 'X-AspNet-Version', *args, **kwargs)


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://www.troyhunt.com/shhh-dont-let-your-response-headers/',
     ],
     standards={
         'CWE': '200',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N': 5.3,
     })
def is_header_x_powered_by_present(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-Powered-By header is missing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_header_present(url, 'X-Powered-By', *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_access_control_allow_origin_missing(url: str,
                                                  *args, **kwargs) -> tuple:
    r"""
    Check if Access-Control-Allow-Origin HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    if 'headers' in kwargs:
        kwargs['headers'].update({'Origin':
                                  'https://www.malicious.com'})
    else:
        kwargs = {'headers': {'Origin': 'https://www.malicious.com'}}

    return _has_insecure_value(
        url, 'Access-Control-Allow-Origin', False, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_cache_control_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Cache-Control HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'Cache-Control', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def is_header_content_security_policy_missing(url: str,
                                              *args, **kwargs) -> tuple:
    r"""
    Check if Content-Security-Policy HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(
        url, 'Content-Security-Policy', True, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_content_type_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Content-Type HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'Content-Type', True, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_expires_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Expires HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'Expires', False, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_pragma_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Pragma HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'Pragma', True, *args, **kwargs)


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://www.troyhunt.com/shhh-dont-let-your-response-headers/',
     ],
     standards={
         'CWE': '200',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N': 5.3,
     })
def is_header_server_present(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Server HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_header_present(url, 'Server', *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_x_content_type_options_missing(url: str, *args,
                                             **kwargs) -> tuple:
    r"""
    Check if X-Content-Type-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(
        url, 'X-Content-Type-Options', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def is_header_x_frame_options_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-Frame-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'X-Frame-Options', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def is_header_perm_cross_dom_pol_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-Permitted-Cross-Domain-Policies HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(
        url, 'X-Permitted-Cross-Domain-Policies', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def is_header_x_xxs_protection_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-XSS-Protection HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'X-XSS-Protection', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def is_header_hsts_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Strict-Transport-Security HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    header = 'Strict-Transport-Security'
    session = http.HTTPSession(url, *args, **kwargs)

    is_vulnerable: bool = True
    if header in session.response.headers:
        re_match = re.search(
            pattern=HDR_RGX[header.lower()],
            string=session.response.headers[header],
            flags=re.IGNORECASE)
        if re_match:
            max_age_val = re_match.groups()[0]
            if int(max_age_val) >= 31536000:
                is_vulnerable = False

    session.set_messages(
        source=f'HTTP/Response/Headers/{header}',
        msg_open=f'{header} is secure',
        msg_closed=f'{header} is insecure')
    session.add_unit(
        is_vulnerable=is_vulnerable)
    return session.get_tuple_result()


@api(risk=MEDIUM, kind=DAST)
def is_basic_auth_enabled(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if BASIC authentication is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    if url.startswith('https'):
        return CLOSED, f'URL uses HTTPS: {url}'
    return _has_insecure_value(url, 'WWW-Authenticate', False, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def has_trace_method(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if HTTP TRACE method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_method(url, 'TRACE', *args, **kwargs)


@api(risk=LOW, kind=DAST)
def has_delete_method(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if HTTP DELETE method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_method(url, 'DELETE', *args, **kwargs)


@api(risk=LOW, kind=DAST)
def has_put_method(url: str, *args, **kwargs) -> tuple:
    r"""
    Check is HTTP PUT method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_method(url, 'PUT', *args, **kwargs)


@api(risk=HIGH,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/SQL_Injection',
         'https://www.acunetix.com/websitesecurity/sql-injection/'
     ],
     standards={
         'CWE': '89',
         'WASC': '19',
         'CAPEC': '66',
     },
     examples=[
         'https://www.w3schools.com/sql/sql_injection.asp',
     ],
     score={})
def has_sqli(url: str, *args, **kwargs) -> tuple:
    r"""
    Check SQLi vulnerability by checking common SQL strings in response.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_multiple_text(url, SQLI_ERROR_MSG, *args, **kwargs)


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)',
         'https://www.cgisecurity.com/xss-faq.html',
         'https://cheatsheetseries.owasp.org/cheatsheets/' +
         'Cross_Site_Scripting_Prevention_Cheat_Sheet.html',
     ],
     standards={
         'CWE': '79',
         'WASC': '8',
         'CAPEC': '63',
     },
     examples=[
         'https://excess-xss.com/',
     ],
     score={})
def has_xss(url: str, expect: str, *args: Any, **kwargs: Any) -> tuple:
    r"""
    Check XSS vulnerability by checking injected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Command_Injection',
         'https://www.netsparker.com/blog/web-security/' +
         'command-injection-vulnerability/',
     ],
     standards={
         'CWE': ['77', '78'],
         'CAPEC': '152',
         'WASC': '31',
     },
     examples=[
         'https://portswigger.net/web-security/os-command-injection',
     ],
     score={})
def has_command_injection(url: str, expect: str,
                          *args: Any, **kwargs: Any) -> tuple:
    r"""
    Check command injection vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Command_Injection',
         'https://www.netsparker.com/blog/web-security/' +
         'command-injection-vulnerability/',
     ],
     standards={
         'CWE': ['77', '78'],
         'CAPEC': '152',
         'WASC': '31',
     },
     examples=[
         'https://portswigger.net/web-security/os-command-injection',
     ],
     score={})
def has_php_command_injection(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check PHP command injection vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Session_fixation',
         'https://en.wikipedia.org/wiki/Session_fixation',
     ],
     standards={
         'CWE': '384',
         'CAPEC': '61',
     },
     examples=[
         'https://portswigger.net/web-security/os-command-injection',
     ],
     score={})
def has_session_fixation(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check session fixation by not passing cookies and having authenticated.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/' +
         'Top_10_2007-Insecure_Direct_Object_Reference',
     ],
     standards={
         'CWE': '639',
     },
     examples=[
         'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-0329',
         'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-4369',
         'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2005-0229',
     ],
     score={})
def has_insecure_dor(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check insecure direct object reference vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH, kind=DAST)
def has_dirtraversal(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check directory traversal vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH, kind=DAST)
def has_csrf(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check Cross-Site Request Forgery vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH, kind=DAST)
def has_lfi(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check local file inclusion vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def has_hpp(url: str, expect: str, *args, **kwargs) -> tuple:
    r"""
    Check HTTP Parameter Pollution vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerability .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@api(risk=HIGH, kind=DAST)
def has_insecure_upload(url: str, expect: str, file_param: str,
                        file_path: str, *args, **kwargs) -> tuple:
    r"""
    Check insecure upload vulnerability.

    :param url: URL to test.
    :param file_param: Name of a file to try to upload.
    :param file_path: Path to the actual file.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    exploit_file = {file_param: open(file_path)}
    return _generic_has_text(url, expect, files=exploit_file, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def has_xsleak_by_frames_discrepancy(url_a: str,
                                     url_b: str,
                                     need_samesite_strict_cookies: bool,
                                     *request_args,
                                     **request_kwargs) -> tuple:
    r"""
    Check if a view is vulnerable to a XSLeak by counting the number of frames.

    See: `CWE-204 <https://cwe.mitre.org/data/definitions/204.html`_.
    See: `Browser Side Channels research <https://github.com/xsleaks/
    xsleaks/wiki/Browser-Side-Channels#frame-count>`_.
    See: `Real life exploitation <https://www.imperva.com/blog/
    mapping-communication-between-facebook-accounts
    -using-a-browser-based-side-channel-attack/>`_.

    If the same view of a website renders a different number of frames and is
    using cookie-based authentication and is not using cookies with the
    `SameSite` attribute set to `Strict`, then an attacker can exploit the
    cross-origin access to the window.frames.length object to ask binary
    questions about the contents displayed to the user in order to violate
    his/her privacy.

    :param url_a: URL for a view.
    :param url_b: URL for another view.
    :param need_samesite_strict_cookies: True if at least one of the cookies
                                         needed to load either `url_a` or
                                         `url_b` have set the `SameSite`
                                         attribute to Strict.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    if need_samesite_strict_cookies:
        return CLOSED, ('Site is not vulnerable to XSLeaks by abusing '
                        'cross-origin window.frames.length property')

    session_a = http.HTTPSession(url_a, *request_args, **request_kwargs)
    session_b = http.HTTPSession(url_b, *request_args, **request_kwargs)

    content_a, content_b = session_a.response.text, session_b.response.text

    fingerprint_a, fingerprint_b = \
        session_a.get_fingerprint(), session_b.get_fingerprint()

    html_obj_a = BeautifulSoup(content_a, "html.parser")
    html_obj_b = BeautifulSoup(content_b, "html.parser")

    frames_a = len(html_obj_a('frame') + html_obj_a('iframe'))
    frames_b = len(html_obj_b('frame') + html_obj_b('iframe'))

    if frames_a != frames_b:
        vulns = [
            Unit(where=url,
                 source='HTTP/Cookies/SameSite',
                 specific=[f'window.frames.length is leaking information'],
                 fingerprint=fp)
            for url, fp in ((url_a, fingerprint_a), (url_b, fingerprint_b))]
        return OPEN, ('Site is vulnerable to XSLeak due to discrepancies '
                      'in the frame count for different resources and the use '
                      'of cookies with the SameSite attribute not set to '
                      '"Strict"'), vulns
    return CLOSED, 'Site is not vulnerable to XSLeak by frame counting'


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def has_not_subresource_integrity(
        url: str, *request_args, **request_kwargs) -> tuple:
    r"""
    Check if elements fetched by the provided url have `SRI`.

    See: `Documentation <https://developer.mozilla.org/en-US/docs/Web/
    Security/Subresource_Integrity>`_.

    :param url: URL to test.
    :param \*request_args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*request_kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *request_args, **request_kwargs)
    html = session.response.text
    fingerprint = session.get_fingerprint()

    soup = BeautifulSoup(html, features="html.parser")

    vulns: List[Unit] = []
    safes: List[Unit] = []

    for elem_types in ('link', 'script'):
        vulnerable: bool = any(
            elem.get('integrity') is None for elem in soup(elem_types))
        asserts: str = 'has not' if vulnerable else 'has'

        unit: Unit = Unit(
            where=url,
            source=f'HTTP/Response/HTML/Tag/{elem_types}',
            specific=[f'{elem_types} element {asserts} integrity attributes'],
            fingerprint=fingerprint)

        if vulnerable:
            vulns.append(unit)
        else:
            safes.append(unit)

    if vulns:
        msg = 'Site does not implement Subresource Integrity Checks'
        return OPEN, msg, vulns, safes
    msg = 'Site does implement Subresource Integrity Checks'
    return CLOSED, msg, vulns, safes


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/' +
         'Information_exposure_through_query_strings_in_url',
     ],
     standards={
         'CWE': '598',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N': 6.5,
     })  # pylint: disable=keyword-arg-before-vararg
@unknown_if(http.ParameterError, http.ConnError)
def is_sessionid_exposed(url: str, argument: str = 'sessionid',
                         *args, **kwargs) -> tuple:
    r"""
    Check if resulting URL has an exposed session ID.

    :param url: URL to test.
    :argument: Name of argument to search. Defaults to ``sessionid``.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    regex: str = rf'\b({argument})\b=([a-zA-Z0-9_-]+)'

    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'HTTP/Request/GET/params/{argument}',
        msg_open='Session ID is exposed',
        msg_closed='Session ID is not exposed')
    session.add_unit(
        is_vulnerable=re.search(regex, session.response.url, re.IGNORECASE),
        specific=[f'{argument} is exposed'])
    return session.get_tuple_result()


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://www.troyhunt.com/shhh-dont-let-your-response-headers/',
     ],
     standards={
         'CWE': '200',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N': 5.3,
     })
@unknown_if(http.ParameterError, http.ConnError)
def is_version_visible(url, *args, **kwargs) -> tuple:
    r"""
    Check if product version is visible on HTTP response headers.

    :param url: IP address to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    service = banner.HTTPService(url, *args, **kwargs)
    service.sess.set_messages(
        source=f'HTTP/Response/Header/Server',
        msg_open='Version visible in Server header',
        msg_closed='Version is not visible in Server header')
    service.sess.add_unit(
        is_vulnerable=service.get_version())
    return service.sess.get_tuple_result()


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Insecure_Transport',
     ],
     standards={
         'CWE': '319',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N': 3.5,
     })
@unknown_if(AssertionError, http.ParameterError, http.ConnError)
def is_not_https_required(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if HTTPS is always forced on a given URL.

    :param url: URL to test.
    :rtype: :class:`fluidasserts.Result`
    """
    if not url.startswith('http://'):
        raise AssertionError('URL should start with http://')

    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'HTTP/SSL/Disabled',
        msg_open='HTTPS is not forced on URL',
        msg_closed='HTTPS is forced on URL')
    session.add_unit(
        is_vulnerable=not session.url.startswith('https'))
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
def has_dirlisting(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if the given URL has directory listing enabled.

    Looks for the text "Index of" to test if directories can be listed.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_has_text(url, 'Index of', *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def is_resource_accessible(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if URL is available by checking response code.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Response/StatusCode',
        msg_open='Resource is available',
        msg_closed='Resource is not available')
    session.add_unit(
        is_vulnerable=re.search(
            r'[2-3]\d\d', str(session.response.status_code)))
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def is_response_delayed(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if the response time is acceptable.

    Values taken from:
    https://www.nngroup.com/articles/response-times-3-important-limits/

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    max_response_time = 1
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Server/Configuration/Date',
        msg_open='Long response time',
        msg_closed='Response time is acceptable')
    current_response_time: float = session.response.elapsed.total_seconds()
    session.add_unit(
        is_vulnerable=current_response_time > max_response_time)
    return session.get_tuple_result()


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://blog.rapid7.com/2017/06/15/about-user-enumeration/',
         'https://www.hacksplaining.com/prevention/user-enumeration',
     ],
     standards={
         'CWE': '203',
     },
     examples=[
         'https://www.cvedetails.com/cve/CVE-2018-15473/',
     ],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N': 7.5,
     })  # pylint: disable=keyword-arg-before-vararg
@unknown_if(AssertionError, http.ParameterError, http.ConnError)
def has_user_enumeration(url: str, user_field: str,
                         user_list: Optional[List] = None,
                         fake_users: Optional[List] = None,
                         *args, **kwargs) -> tuple:
    r"""
    Check if URL has user enumeration.

    :param url: URL to test.
    :param user_field: Field corresponding to the username.
    :param user_list: List of users.
    :param fake_users: List of fake users.
    :param \*args: Optional arguments for :func:`~_request_dataset`.
    :param \*\*kwargs: Optional arguments for :func:`~_request_dataset`.
    :rtype: :class:`fluidasserts.Result`

    Either ``params`` or ``data`` must be present in ``kwargs``,
    if the request is ``GET`` or ``POST``, respectively.
    They must be strings as they would appear in the request.
    """
    needed_params: tuple = ('data', 'json', 'params')
    if not any(map(kwargs.get, needed_params)):
        raise AssertionError('No params were given')

    query_string = kwargs[next(filter(kwargs.get, needed_params))]

    if 'json' not in kwargs and user_field not in query_string:
        raise AssertionError('Given user_field not in query string')

    session = http.HTTPSession(url, *args, **kwargs)

    user_list = user_list or ['admin', 'administrator', 'guest', 'test']
    fake_users = fake_users or ['iuaksiuiadbuqywdaskj1234', 'ajahdsjahdjhbaj',
                                'aksjdads@asd.com', 'osvtxodahihiis@gmail.com',
                                'something@example.com', '12312314511231']

    # Evaluate the response with non-existant users
    fake_datasets = _create_dataset(user_field, fake_users, query_string)
    true_datasets = _create_dataset(user_field, user_list, query_string)

    fake_responses = _request_dataset(url, fake_datasets, *args, **kwargs)
    true_responses = _request_dataset(url, true_datasets, *args, **kwargs)

    sum_ratios: float = sum(
        SequenceMatcher(None, fake_response, true_response).ratio()
        for fake_response in fake_responses
        for true_response in true_responses)

    avg_ratio: float = sum_ratios / len(fake_responses) / len(true_responses)

    session.set_messages(
        source='HTTP/Response/Discrepancy',
        msg_open='User enumeration is possible',
        msg_closed='User enumeration not possible')
    session.add_unit(
        is_vulnerable=avg_ratio <= 0.95,
        specific=[user_field])
    return session.get_tuple_result()


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Brute_force_attack',
     ],
     standards={
         'CWE': ['307', '799'],
         'CAPEC': ['49', '112'],
     },
     examples=[
         'https://nvd.nist.gov/vuln/detail/CVE-2019-6524',
     ],
     score={
         'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N': 5.3,
     })  # pylint: disable=keyword-arg-before-vararg
@unknown_if(AssertionError, http.ParameterError, http.ConnError)
def can_brute_force(url: str, ok_regex: str, user_field: str, pass_field: str,
                    user_list: List[str] = None, pass_list: List[str] = None,
                    *args, **kwargs) -> tuple:
    r"""
    Check if URL allows brute forcing.

    :param url: URL to test.
    :param ok_regex: Regex to search in response text.
    :param user_field: Name of the field for username.
    :param pass_field: Name of the field for password.
    :param user_list: List of users to create dataset.
    :param pass_list: List of passwords.
    :param \*args: Optional arguments for :func:`~_request_dataset`.
    :param \*\*kwargs: Optional arguments for :func:`~_request_dataset`.
    :rtype: :class:`fluidasserts.Result`

    Either ``params`` or ``data`` must be present in ``kwargs``,
    if the request is ``GET`` or ``POST``, respectively.
    They must be strings as they would appear in the request.
    """
    needed_params: tuple = ('data', 'json', 'params')
    if not any(map(kwargs.get, needed_params)):
        raise AssertionError('No params were given')

    query_param = next(filter(kwargs.get, needed_params))
    query_string = kwargs[query_param]

    users_dataset = _create_dataset(user_field, user_list, query_string)

    dataset = []
    for password in pass_list:
        for user_ds in users_dataset:
            _datas = _create_dataset(pass_field, [password], user_ds)
            dataset.append(_datas[0])

    session = http.HTTPSession(url, *args, **kwargs)

    is_vulnerable: bool = False
    for _datas in dataset:
        kwargs[query_param] = _datas

        sess = http.HTTPSession(url, *args, **kwargs)

        if ok_regex in sess.response.text:
            is_vulnerable = True

    session.set_messages(
        source='HTTP/Request/Limit',
        msg_open='Brute forcing is possible',
        msg_closed='Brute forcing is not possible')
    session.add_unit(
        is_vulnerable=is_vulnerable,
        specific=[user_field, pass_field])
    return session.get_tuple_result()


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def has_clear_viewstate(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if URL has encrypted ViewState by checking response.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Server/Configuration/Date',
        msg_open='View State is not encrypted',
        msg_closed='View State is encrypted')

    viewstate = session.get_html_value('input', '__VIEWSTATE')

    encrypted: bool = False
    if viewstate:
        try:
            ViewState(viewstate).decode()
        except ViewStateException:
            encrypted = True

    session.add_unit(is_vulnerable=viewstate and not encrypted)

    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
@unknown_if(KeyError, http.ParameterError, http.ConnError)
def is_date_unsyncd(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if server's date is not synchronized with NTP servers.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Server/Configuration/Date',
        msg_open='Server is not synced with NTP servers',
        msg_closed='Server is synced with NTP servers')

    server_date = datetime.strptime(
        session.response.headers['Date'], '%a, %d %b %Y %H:%M:%S GMT')

    for _ in range(5):
        try:
            ntpclient = ntplib.NTPClient()
            response = ntpclient.request('pool.ntp.org', port=123, version=3)
        except ntplib.NTPException:
            # Let's retry the request
            sleep(1.0)
        else:
            # Success, stop retrying
            break
    ntp_date = datetime.fromtimestamp(response.tx_time, tz=timezone('GMT'))
    ntp_ts = datetime.utcfromtimestamp(ntp_date.timestamp()).timestamp()

    delta_ts = ntp_ts - server_date.timestamp()

    session.add_unit(is_vulnerable=-3 < delta_ts > 3)

    return session.get_tuple_result()


@api(risk=MEDIUM,
     kind=DAST,
     references=[],
     standards={},
     examples=[],
     score={})
@unknown_if(http.ParameterError, http.ConnError)
def has_host_header_injection(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if server is vulnerable to 'Host' header injection.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    hostname = 'hackedbyfluidattacks.com'
    if 'headers' in kwargs:
        kwargs['headers'].update({'Host': hostname})
    else:
        kwargs['headers'] = {'Host': hostname}

    kwargs['redirect'] = False

    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Request/Headers/Host',
        msg_open='Server is vulnerable to host header injection',
        msg_closed='Server is not vulnerable to host header injection')
    session.add_unit(
        is_vulnerable=hostname in session.response.headers.get('Location', []))
    return session.get_tuple_result()


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://portswigger.net/kb/issues/01000400_mixed-content',
     ],
     standards={
         'CWE': '319',
     },
     examples=[],
     score={
         'CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N': 3.5,
     })
@unknown_if(http.ParameterError, http.ConnError)
def has_mixed_content(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if resource has mixed (HTTP and HTTPS) links.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTTP/Response/Body',
        msg_open='Resource has mixed content',
        msg_closed='Resource has not mixed content')

    links = _get_links(session.response.text)
    has_http: bool = any(x.startswith('http://') for x in links)
    has_https: bool = any(x.startswith('https://') for x in links)

    session.add_unit(is_vulnerable=has_http and has_https)

    return session.get_tuple_result()


@api(risk=LOW,
     kind=DAST,
     references=[
         'https://www.owasp.org/index.php/Reverse_Tabnabbing',
         'https://mathiasbynens.github.io/rel-noopener/',
     ],
     standards={
         'CWE': '1022',
     },
     examples=[
         'https://dev.to/ben/the-targetblank-vulnerability-by-example',
     ],
     score={
         'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N': 6.5,
     })
@unknown_if(http.ParameterError, http.ConnError)
def has_reverse_tabnabbing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if resource has links vulnerable to a reverse tabnabbing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source='HTML/href/rel/noopener',
        msg_open='There are a href tags susceptible to reverse tabnabbing',
        msg_closed=('There are no a href tags susceptible to '
                    'reverse tabnabbing'))

    http_re = re.compile("^http(s)?://")
    html_obj = BeautifulSoup(session.response.text, features="html.parser")

    for href in html_obj.findAll('a', attrs={'href': http_re}):
        parsed: dict = {
            'href': href.get('href'),
            'target': href.get('target'),
            'rel': href.get('rel'),
        }
        is_vulnerable: bool = parsed['href'] \
            and parsed['target'] == '_blank' \
            and (not parsed['rel'] or 'noopener' not in parsed['rel'])

        session.add_unit(is_vulnerable=is_vulnerable,
                         specific=[parsed['href']])

    return session.get_tuple_result()


@api(
    risk=HIGH,
    kind=DAST,
    references=[
        'https://www.owasp.org/index.php/SQL_Injection',
        'https://www.acunetix.com/websitesecurity/sql-injection/'
    ],
    standards={
        'CWE': '89',
        'WASC': '19',
        'CAPEC': '66',
    },
    examples=[
        'https://www.w3schools.com/sql/sql_injection.asp',
    ],
    score={})
@unknown_if(http.ConnError, http.ParameterError)
def has_sqli_time(url_safe: str,
                  url_break: str,
                  time: int,
                  args_safe: List = None,
                  kwargs_safe: Dict = None,
                  args_break: List = None,
                  kwargs_break: Dict = None) -> tuple:
    """
    Check SQLi vulnerability by checking the delay of response.

    Take an undamaged URL along with the optional parameters
    of the :class:`.HTTPSession`. and calculate the average response time.
    Take an exploited URL with optional parameters
    from :class:`.HTTPSession`. and calculate the response time and then
    compare the result with the average response time of the undamaged URL.

    ============
    Suggestions:
    ============

    * Use a `sleep <https://cutt.ly/deiKvd1>`_ method in your attack.
    * Use this method with stable connection network, a slow connection can
      generate a False Positive.

    * Use a perceptible time delay to prevent a False Positive.

    :param url_safe: URL to test without SQLi.
    :param url_break: URL to test with SQLi.
    :param time: Delay of response.
    :param args_safe: Optional arguments for :class:`.HTTPSession`.
    :param kwargs_safe: Optional arguments for :class:`.HTTPSession`.
    :param args_break: Optional arguments for :class:`.HTTPSession`.
    :param kwargs_break: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    field: str = _get_field(kwargs_break)

    is_vulnerable = False

    times = []

    last_exc = None

    for _ in range(6):
        try:
            req = http.HTTPSession(url_safe, *args_safe, **kwargs_safe)
        except (http.requests.HTTPError, http.ConnError,
                http.ParameterError) as exc:
            last_exc = exc
        else:
            times.append(req.response.elapsed.seconds)

    # we need at least 3 successful requests to measure the avg
    # if we are not able to collect them, mark the check as UNKNOWN
    if len(times) < 3:
        raise last_exc

    avg_time = sum(times) / len(times)

    if (not isinstance(kwargs_break, dict) and kwargs_break is not None) or (
            not isinstance(kwargs_safe, dict) and kwargs_safe is not None):
        raise TypeError('kwargs must be a Dict')

    kwargs_break = kwargs_break or {}
    kwargs_break.update({'timeout': time + (avg_time * 1.3)})

    session_break = http.HTTPSession(
        url_break, *args_break, **kwargs_break, request_at_instantiation=False)
    session_break.set_messages(
        source='HTTP/Response/Body',
        msg_open=('This endpoint is vulnerable to SQLi using '
                  'time delay technique'),
        msg_closed=('This endpoint is not vulnerable to SQLi using '
                    'time delay technique'))

    try:
        session_break.do_request()
    except http.ConnError as exc:
        if 'timed out' not in str(exc):
            raise exc
        is_vulnerable = True
    else:
        time_end = session_break.response.elapsed.seconds
        is_vulnerable = time_end >= time and time_end > avg_time

        if session_break.response.status_code >= 500:
            return UNKNOWN, f'We got a {session_break.response.status_code} \
                status code'

    session_break.add_unit(is_vulnerable=is_vulnerable, specific=[field])

    return session_break.get_tuple_result()
