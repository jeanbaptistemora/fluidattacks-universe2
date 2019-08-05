# -*- coding: utf-8 -*-

"""This module allows to check HTTP-specific vulnerabilities."""

# standard imports
import re
from copy import deepcopy
from datetime import datetime
from typing import Optional, List, Union

# 3rd party imports
from bs4 import BeautifulSoup
from pytz import timezone
from viewstate import ViewState, ViewStateException
from urllib.parse import parse_qsl
import ntplib
import requests

# local imports
from fluidasserts.helper import banner
from fluidasserts.helper import http
from fluidasserts import Result
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import LOW, MEDIUM
from fluidasserts import DAST
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify, api

# pylint: disable=too-many-lines

# This dictionary maps the header to a regex in which the value is secure
HDR_RGX = {
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
}  # type: dict

# Regex taken from SQLmap project
SQLI_ERROR_MSG = {
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


def _options_request(url: str, *args, **kwargs) -> Optional[requests.Response]:
    r"""
    Send an``HTTP OPTIONS`` request.

    Tests what kind of ``HTTP`` methods are supported on the given ``url``.

    :param url: URL to test.
    :param \*args: Optional arguments for :py:func:`requests.options`.
    :param \*\*kwargs: Optional arguments for :py:func:`requests.options`.
    """
    try:
        return requests.options(url, verify=False, *args, **kwargs)
    except requests.ConnectionError as exc:
        raise http.ConnError(exc)
    except requests.exceptions.MissingSchema as exc:
        raise http.ParameterError(exc)


def _has_method(url: str, method: str, *args, **kwargs) -> bool:
    r"""
    Check if specific HTTP method is allowed in URL.

    :param url: URL to test.
    :param method: HTTP method to test.
    :param \*args: Optional arguments for :py:func:`requests.options`.
    :param \*\*kwargs: Optional arguments for :py:func:`requests.options`.
    """
    try:
        is_method_present = _options_request(url, *args, **kwargs).headers
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    result = True
    if 'allow' in is_method_present:
        if method in is_method_present['allow']:
            show_open(f'HTTP Method {method} enabled',
                      details=dict(url=url))
        else:
            show_close(f'HTTP Method {method} disabled',
                       details=dict(url=url))
            result = False
    else:
        show_close(f'HTTP Method {method} disabled',
                   details=dict(url=url))
        result = False
    return result


def _is_header_present(url: str, header: str, *args, **kwargs) -> Result:
    """
    Check if header is present in URL.

    :param url: URL to test.
    :param header: Header to test if present.
    """
    http_session = http.HTTPSession(url, *args, **kwargs)
    headers_info = http_session.response.headers
    return headers_info[header] if header in headers_info else None


def _has_insecure_value(url: str, header: str, *args, **kwargs) -> bool:
    """
    Check if header value is the.

    :param url: URL to test.
    :param header: Header to test if present.
    """
    expected = HDR_RGX[header.lower()]
    http_session = http.HTTPSession(url, *args, **kwargs)
    headers_info = http_session.response.headers
    if header in headers_info:
        value = headers_info[header]
        return not re.match(expected, value, re.IGNORECASE)
    return None


def _generic_has_multiple_text(url: str, regex_list: List[str],
                               *args, **kwargs) -> bool:
    r"""
    Check if one of a list of bad texts is present.

    :param url: URL to test.
    :param regex_list: List of regexes to search.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        response = http_session.response
        fingerprint = http_session.get_fingerprint()
        if response.status_code >= 500:
            show_unknown('There was an error',
                         details=dict(url=url, status=response.status_code,
                                      fingerprint=fingerprint))
            return False
        the_page = response.text
        for regex in regex_list:
            if re.search(regex, the_page, re.IGNORECASE):
                show_open('A bad text was present',
                          details=dict(url=url,
                                       bad_text=regex,
                                       fingerprint=fingerprint))
                return True
        show_close('No bad text was present',
                   details=dict(url=url, fingerprint=fingerprint))
        return False
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False


def _generic_has_text(url: str, expected_text: str, *args, **kwargs) -> bool:
    r"""
    Check if a bad text is present.

    :param url: URL to test.
    :param expected_text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        response = http_session.response
        fingerprint = http_session.get_fingerprint()
        the_page = response.text
        if response.status_code >= 500:
            show_unknown('There was an error',
                         details=dict(url=url,
                                      status=response.status_code,
                                      fingerprint=fingerprint))
            return False
        if re.search(str(expected_text), the_page, re.IGNORECASE):
            show_open('Bad text present',
                      details=dict(url=url,
                                   bad_text=expected_text,
                                   fingerprint=fingerprint))
            return True
        show_close('Bad text not present',
                   details=dict(url=url,
                                bad_text=expected_text,
                                fingerprint=fingerprint))
        return False
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False


@notify
@level('low')
@track
def has_multiple_text(url: str, regex_list: List[str],
                      *args, **kwargs) -> bool:
    r"""
    Check if one of a list of bad texts is present in URL response.

    :param url: URL to test.
    :param regex_list: List of regexes to search.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_multiple_text(url, regex_list, *args, **kwargs)


@notify
@level('low')
@track
def has_text(url: str, expected_text: str, *args, **kwargs) -> bool:
    r"""
    Check if a bad text is present in URL response.

    :param url: URL to test.
    :param expected_text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expected_text, *args, **kwargs)


@notify
@level('low')
@track
def has_not_text(url: str, expected_text: str, *args, **kwargs) -> bool:
    r"""
    Check if a required text is not present in URL response.

    :param url: URL to test.
    :param expected_text: Text to search. Can be regex.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        response = http_session.response
        fingerprint = http_session.get_fingerprint()
        the_page = response.text
        if not re.search(str(expected_text), the_page, re.IGNORECASE):
            show_open('Expected text not present',
                      details=dict(url=url,
                                   expected_text=expected_text,
                                   fingerprint=fingerprint))
            return True
        show_close('Expected text present',
                   details=dict(url=url,
                                expected_text=expected_text,
                                fingerprint=fingerprint))
        return False
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False


@api(risk=LOW, kind=DAST)
def is_header_x_asp_net_version_present(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-AspNet-Version header is missing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-AspNet-Version'
    try:
        if _is_header_present(url, header, *args, **kwargs):
            return OPEN, f'Insecure header {header} is present'
        return CLOSED, f'Insecure header {header} is not present'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_x_powered_by_present(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-Powered-By header is missing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Powered-By'
    try:
        if _is_header_present(url, header, *args, **kwargs):
            return OPEN, f'Insecure header {header} is present'
        return CLOSED, f'Insecure header {header} is not present'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_access_control_allow_origin_missing(url: str,
                                                  *args, **kwargs) -> Result:
    r"""
    Check if Access-Control-Allow-Origin HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Access-Control-Allow-Origin'
    if 'headers' in kwargs:
        kwargs['headers'].update({'Origin':
                                  'https://www.malicious.com'})
    else:
        kwargs = {'headers': {'Origin': 'https://www.malicious.com'}}

    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result:
            return OPEN, f'{header} HTTP header is insecure'
        if result is None:
            return CLOSED, (f'HTTP header {header} not present which is secure'
                            'by default')
        return CLOSED, f'{header} HTTP header is insecure'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_cache_control_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Cache-Control HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Cache-Control'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure on '
                          f'resources with sensible data as it could get '
                          f'cached and an attacker with local access '
                          f'could retrieve it')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_header_content_security_policy_missing(url: str,
                                              *args, **kwargs) -> Result:
    r"""
    Check if Content-Security-Policy HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Content-Security-Policy'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it increases the probability of an XSS Attack '
                          f'to succeed')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_content_type_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Content-Type HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Content-Type'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it leaves the type of the response open '
                          f'to interpretation (which may introduce '
                          f'vulnerabilities by an improper synchronization '
                          f'between the client and the server, or sniffing '
                          f'of the payload')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_expires_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Expires HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Expires'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result:
            return OPEN, f'Header {header} has insecure value'
        if result is None:
            return CLOSED, f'Header {header} is not set'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_pragma_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Pragma HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Pragma'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure on '
                          f'resources with sensible data')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_server_present(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Server HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Server'
    try:
        if _is_header_present(url, header, *args, **kwargs):
            return OPEN, f'Insecure header {header} is present'
        return CLOSED, f'Insecure header {header} is not present'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW, kind=DAST)
def is_header_x_content_type_options_missing(url: str, *args,
                                             **kwargs) -> Result:
    r"""
    Check if X-Content-Type-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Content-Type-Options'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it does not dissable MIME Sniffing')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_header_x_frame_options_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-Frame-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Frame-Options'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it allows for a Click Jacking attack')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_header_perm_cross_dom_pol_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-Permitted-Cross-Domain-Policies HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Permitted-Cross-Domain-Policies'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'on applications that use Flash or PDF')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_header_x_xxs_protection_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-XSS-Protection HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-XSS-Protection'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure as '
                          f'it aids an XSS attack to succeed')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_header_hsts_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Strict-Transport-Security HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Strict-Transport-Security'
    try:
        value = _is_header_present(url, header, *args, **kwargs)
        if not value:
            return OPEN, f'Header {header} not present'

        re_match = re.search(HDR_RGX[header.lower()], value, flags=re.I)
        if re_match:
            max_age_val = re_match.groups()[0]
            if int(max_age_val) >= 31536000:
                return CLOSED, f'HTTP header {header} is secure'
        return OPEN, f'{header} HTTP header is insecure'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=MEDIUM, kind=DAST)
def is_basic_auth_enabled(url: str, *args, **kwargs) -> Result:
    r"""
    Check if BASIC authentication is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    if url.startswith('https'):
        return CLOSED, f'URL uses HTTPS: {url}'
    header = 'WWW-Authenticate'
    try:
        if _has_insecure_value(url, header, *args, **kwargs):
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@notify
@level('low')
@track
def has_trace_method(url: str, *args, **kwargs) -> bool:
    r"""
    Check if HTTP TRACE method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _has_method(url, 'TRACE', *args, **kwargs)


@notify
@level('low')
@track
def has_delete_method(url: str, *args, **kwargs) -> bool:
    r"""
    Check if HTTP DELETE method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _has_method(url, 'DELETE', *args, **kwargs)


@notify
@level('low')
@track
def has_put_method(url: str, *args, **kwargs) -> bool:
    r"""
    Check is HTTP PUT method is enabled.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _has_method(url, 'PUT', *args, **kwargs)


@notify
@level('high')
@track
def has_sqli(url: str, *args, **kwargs) -> bool:
    r"""
    Check SQLi vulnerability by checking common SQL strings.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    expect = SQLI_ERROR_MSG

    return _generic_has_multiple_text(url, expect, *args, **kwargs)


@notify
@level('medium')
@track
def has_xss(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check XSS vulnerability by checking injected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_command_injection(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check command injection vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_php_command_injection(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check PHP command injection vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('medium')
@track
def has_session_fixation(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check session fixation by not passing cookies and having authenticated.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_insecure_dor(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check insecure direct object reference vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_dirtraversal(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check directory traversal vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_csrf(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check Cross-Site Request Forgery vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_lfi(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check local file inclusion vulnerability by checking a expected string.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('medium')
@track
def has_hpp(url: str, expect: str, *args, **kwargs) -> bool:
    r"""
    Check HTTP Parameter Pollution vulnerability.

    :param url: URL to test.
    :param expect: Text to search in potential vulnerabilty .
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    return _generic_has_text(url, expect, *args, **kwargs)


@notify
@level('high')
@track
def has_insecure_upload(url: str, expect: str, file_param: str,
                        file_path: str, *args, **kwargs) -> bool:
    r"""
    Check insecure upload vulnerability.

    :param url: URL to test.
    :param file_param: Name of a file to try to upload.
    :param file_path: Path to the actual file.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    exploit_file = {file_param: open(file_path)}
    return _generic_has_text(url, expect, files=exploit_file, *args, **kwargs)


# pylint: disable=keyword-arg-before-vararg
@notify
@level('medium')
@track
def is_sessionid_exposed(url: str, argument: str = 'sessionid',
                         *args, **kwargs) -> bool:
    r"""
    Check if resulting URL has an exposed session ID.

    :param url: URL to test.
    :argument: Name of argument to search. Defaults to ``sessionid``.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        response_url = http_session.response.url
        fingerprint = http_session.get_fingerprint()
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False

    regex = r'\b(' + argument + r')\b=([a-zA-Z0-9_-]+)'

    result = True
    match = re.search(regex, response_url)
    if match:
        result = True
        show_open('Session ID is exposed',
                  details=dict(url=response_url, session_id='{}: {}'.
                               format(argument, match.group(2)),
                               fingerprint=fingerprint))
    else:
        result = False
        show_close('Session ID is hidden',
                   details=dict(url=response_url, session_id=argument))
    return result


@notify
@level('low')
@track
def is_version_visible(url) -> bool:
    """
    Check if product version is visible on HTTP response headers.

    :param ip_address: IP address to test.
    :param ssl: Whether to use HTTP or HTTPS.
    :param port: If necessary, specify port to connect to.
    """
    try:
        service = banner.HTTPService(url)
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(url=url, error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    version = service.get_version()
    fingerprint = service.get_fingerprint()

    result = True
    if version:
        result = True
        show_open('HTTP version visible',
                  details=dict(url=url,
                               version=version, fingerprint=fingerprint))
    else:
        result = False
        show_close('HTTP version not visible',
                   details=dict(url=url,
                                fingerprint=fingerprint))
    return result


@notify
@level('medium')
@track
def is_not_https_required(url: str) -> bool:
    r"""
    Check if HTTPS is always forced on a given URL.

    :param url: URL to test.
    """
    if not url.startswith('http://'):
        show_unknown('URL should start with "http://"',
                     details=dict(url=url))
        return False
    try:
        http_session = http.HTTPSession(url)
        fingerprint = http_session.get_fingerprint()
        if http_session.url.startswith('https'):
            show_close('HTTPS is forced on URL',
                       details=dict(url=http_session.url,
                                    fingerprint=fingerprint))
            return False
        show_open('HTTPS is not forced on URL',
                  details=dict(url=http_session.url, fingerprint=fingerprint))
        return True
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False


@notify
@level('low')
@track
def has_dirlisting(url: str, *args, **kwargs) -> bool:
    r"""
    Check if the given URL has directory listing enabled.

    Looks for the text "Index of" to test if directories can be listed.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    bad_text = 'Index of'
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        response = http_session.response
        fingerprint = http_session.get_fingerprint()
        the_page = response.text

        if re.search(str(bad_text), the_page, re.IGNORECASE):
            show_open('Directory listing enabled',
                      details=dict(url=url, fingerprint=fingerprint))
            return True
        show_close('Directory listing not enabled',
                   details=dict(url=url, fingerprint=fingerprint))
        return False
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False


@notify
@level('medium')
@track
def is_resource_accessible(url: str, *args, **kwargs) -> bool:
    r"""
    Check if URL is available by checking response code.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        fingerprint = http_session.get_fingerprint()
    except http.ConnError as exc:
        show_close('Could not connnect to resource',
                   details=dict(url=url,
                                message=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    if re.search(r'[4-5]\d\d', str(http_session.response.status_code)):
        show_close('Resource not available',
                   details=dict(url=http_session.url,
                                status=http_session.response.status_code,
                                fingerprint=fingerprint))
        return False
    show_open('Resource available',
              details=dict(url=http_session.url,
                           status=http_session.response.status_code,
                           fingerprint=fingerprint))
    return True


@notify
@level('low')
@track
def is_response_delayed(url: str, *args, **kwargs) -> bool:
    r"""
    Check if the response time is acceptable.

    Values taken from:
    https://www.nngroup.com/articles/response-times-3-important-limits/

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    max_response_time = 1
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        fingerprint = http_session.get_fingerprint()
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False

    response_time = http_session.response.elapsed.total_seconds()
    delta = max_response_time - response_time

    if delta >= 0:
        show_close('Response time is acceptable',
                   details=dict(url=http_session.url,
                                response_time=response_time,
                                fingerprint=fingerprint))
        return False
    show_open('Response time not acceptable',
              details=dict(url=http_session.url,
                           response_time=response_time,
                           fingerprint=fingerprint))
    return True


# pylint: disable=too-many-locals
# pylint: disable=keyword-arg-before-vararg
@notify  # noqa
@level('medium')
@track
def has_user_enumeration(url: str, user_field: str,
                         user_list: Optional[List] = None,
                         fake_users: Optional[List] = None,
                         *args, **kwargs) -> bool:
    r"""
    Check if URL has user enumeration.

    :param url: URL to test.
    :param user_field: Field corresponding to the username.
    :param user_list: List of users.
    :param fake_users: List of fake users.
    :param \*args: Optional arguments for :func:`~_request_dataset`.
    :param \*\*kwargs: Optional arguments for :func:`~_request_dataset`.

    Either ``params`` or ``data`` must be present in ``kwargs``,
    if the request is ``GET`` or ``POST``, respectively.
    They must be strings as they would appear in the request.
    """
    qs_params = list(filter(kwargs.get,
                            ['data', 'json', 'params']))
    if not qs_params:
        show_unknown('No params were given', details=dict(url=url))
        return False

    query_string = kwargs.get(qs_params[0])

    if 'json' not in kwargs and user_field not in query_string:
        show_unknown('Given user_field not in query string',
                     details=dict(url=url,
                                  user_field=user_field,
                                  query_string=query_string))
        return False

    if not user_list:
        user_list = ['admin', 'administrator', 'guest', 'test']

    if not fake_users:
        fake_users = ['iuaksiuiadbuqywdaskj1234', 'ajahdsjahdjhbaj',
                      'aksjdads@asd.com', 'osvtxodahidhiis@gmail.com',
                      'something@example.com', '12312314511231']

    # Evaluate the response with non-existant users
    fake_datasets = _create_dataset(user_field, fake_users, query_string)

    try:
        fake_res = _request_dataset(url, fake_datasets, *args, **kwargs)
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    true_datasets = _create_dataset(user_field, user_list, query_string)

    result = False
    try:
        user_res = _request_dataset(url, true_datasets, *args, **kwargs)
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        result = False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        result = False
    else:
        num_comp = len(fake_res) * len(user_res)

        merged = ((x, y) for x in fake_res for y in user_res)

        from difflib import SequenceMatcher
        res = 0.0

        for resp_text, resp_time in merged:
            res += SequenceMatcher(None, resp_text, resp_time).ratio()

        rat = round(res / num_comp, 2)

        if rat > 0.95:
            show_close('User enumeration not possible',
                       details=dict(url=url, similar_answers_ratio=rat))
            result = False
        else:
            show_open('User enumeration possible',
                      details=dict(url=url, similar_answers_ratio=rat))
            result = True
    return result


# pylint: disable=keyword-arg-before-vararg
# pylint: disable=too-many-arguments
@notify
@level('medium')
@track
def can_brute_force(url: str, ok_regex: str, user_field: str, pass_field: str,
                    user_list: List[str] = None, pass_list: List[str] = None,
                    *args, **kwargs) -> bool:
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

    Either ``params`` or ``data`` must be present in ``kwargs``,
    if the request is ``GET`` or ``POST``, respectively.
    They must be strings as they would appear in the request.
    """
    if 'data' not in kwargs and 'params' not in kwargs and \
            'json' not in kwargs:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url))
        return False

    qs_params = list(filter(kwargs.get,
                            ['data', 'json', 'params']))[0]
    query_string = kwargs.get(qs_params)

    users_dataset = _create_dataset(user_field, user_list, query_string)

    dataset = []
    for password in pass_list:
        for user_ds in users_dataset:
            _datas = _create_dataset(pass_field, [password], user_ds)
            dataset.append(_datas[0])

    for _datas in dataset:
        kwargs[qs_params] = _datas
        try:
            sess = http.HTTPSession(url, *args, **kwargs)
            fingerprint = sess.get_fingerprint()
        except http.ConnError as exc:
            show_unknown('Could not connect',
                         details=dict(url=url, data_used=_datas,
                                      error=str(exc).replace(':', ',')))
            return False
        except http.ParameterError as exc:
            show_unknown('An invalid parameter was passed',
                         details=dict(url=url,
                                      error=str(exc).replace(':', ',')))
            return False
        if ok_regex in sess.response.text:
            show_open('Brute forcing possible',
                      details=dict(url=url, data_used=_datas,
                                   fingerprint=fingerprint))
            return True
    show_close('Brute forcing not possible',
               details=dict(url=url, fingerprint=fingerprint))
    return False


@notify
@level('medium')
@track
def has_clear_viewstate(url: str, *args, **kwargs) -> bool:
    r"""
    Check if URL has encrypted ViewState by checking response.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        fingerprint = http_session.get_fingerprint()
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    vsb64 = http_session.get_html_value('input', '__VIEWSTATE')

    if not vsb64:
        show_close('ViewState not found',
                   details=dict(url=http_session.url,
                                fingerprint=fingerprint))
        return False
    try:
        vs_obj = ViewState(vsb64)
        decoded_vs = vs_obj.decode()
        show_open('ViewState is not encrypted',
                  details=dict(url=http_session.url,
                               ViewState=decoded_vs,
                               fingerprint=fingerprint))
        return True
    except ViewStateException:
        show_close('ViewState is encrypted',
                   details=dict(url=http_session.url,
                                fingerprint=fingerprint))
    return False


@notify
@level('low')
@track
def is_date_unsyncd(url: str, *args, **kwargs) -> bool:
    r"""
    Check if server's date is not syncronized with NTP servers.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        sess = http.HTTPSession(url, *args, **kwargs)
        fingerprint = sess.get_fingerprint()

        server_date = datetime.strptime(sess.response.headers['Date'],
                                        '%a, %d %b %Y %H:%M:%S GMT')
        server_ts = server_date.timestamp()
        ntpclient = ntplib.NTPClient()
        response = ntpclient.request('pool.ntp.org', port=123, version=3)
        ntp_date = datetime.fromtimestamp(response.tx_time, tz=timezone('GMT'))
        ntp_ts = datetime.utcfromtimestamp(ntp_date.timestamp()).timestamp()
    except (KeyError, http.ConnError) as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    diff = ntp_ts - server_ts

    if diff < -3 or diff > 3:
        show_open("Server's clock is not syncronized with NTP",
                  details=dict(url=url,
                               server_date=server_date,
                               ntp_date=ntp_date,
                               offset=diff,
                               fingerprint=fingerprint))
        return True
    show_close("Server's clock is syncronized with NTP",
               details=dict(url=url,
                            server_date=server_date,
                            ntp_date=ntp_date,
                            offset=diff,
                            fingerprint=fingerprint))
    return False


@notify
@level('medium')
@track
def has_host_header_injection(url: str, *args, **kwargs) -> bool:
    r"""
    Check if server is vulnerable to 'Host' header injection.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    hostname = 'hackedbyfluidattacks.com'
    if 'headers' in kwargs:
        kwargs['headers'].update({'Host': hostname})
    else:
        kwargs['headers'] = {'Host': hostname}

    kwargs['redirect'] = False
    try:
        sess = http.HTTPSession(url, *args, **kwargs)
        fingerprint = sess.get_fingerprint()
    except (KeyError, http.ConnError) as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    if 'location' in sess.response.headers:
        if hostname in sess.response.headers['Location']:
            show_open('Server is vulnerable to Host header injection',
                      details=dict(url=url, fingerprint=fingerprint))
            return True
    show_close('Server not vulnerable to Host header injection',
               details=dict(url=url, fingerprint=fingerprint))
    return False


@notify
@level('low')
@track
def has_mixed_content(url: str, *args, **kwargs) -> bool:
    r"""
    Check if resource has mixed (HTTP and HTTPS) links.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        sess = http.HTTPSession(url, *args, **kwargs)
        fingerprint = sess.get_fingerprint()
    except (KeyError, http.ConnError) as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False

    links = _get_links(sess.response.text)
    if not links:
        show_close('No links found in site',
                   details=dict(url=url, fingerprint=fingerprint))
        return False
    if any(x.startswith('http://') for x in links) and \
            any(x.startswith('https://') for x in links):

        insecure = list(filter(lambda x: x.startswith('http://'), links))
        show_open('There is mixed content in resource',
                  details=dict(url=url, fingerprint=fingerprint,
                               http_links=insecure))
        return True
    show_close('There is not mixed content in resource',
               details=dict(url=url, fingerprint=fingerprint))
    return False


@notify
@level('low')
@track
def has_reverse_tabnabbing(url: str, *args, **kwargs) -> bool:
    r"""
    Check if resource has links vulnerable to a reverse tabnabbing.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        with http.HTTPSession(url, *args, **kwargs) as sess:
            html = sess.response.text
            fingerprint = sess.get_fingerprint()
    except http.ConnError as exc:
        show_unknown('Could not connnect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False

    vulns, checks = [], []

    http_re = re.compile("^http(s)?://")
    html_obj = BeautifulSoup(html, features="html.parser")

    for ahref in html_obj.findAll('a', attrs={'href': http_re}):
        parsed: dict = {
            'href': ahref.get('href'),
            'target': ahref.get('target'),
            'rel': ahref.get('rel'),
        }
        if parsed['href'] and parsed['target'] == '_blank' \
                and (not parsed['rel'] or 'noopener' not in parsed['rel']):
            vulns.append(parsed)
        else:
            checks.append(parsed)

    if vulns:
        show_open('There are a href tags succeptible to reverse tabnabbing',
                  details=dict(url=url,
                               vulns=vulns,
                               fingerprint=fingerprint))
        return True
    show_close('There are no a href tags succeptible to reverse tabnabbing',
               details=dict(url=url,
                            checks=checks,
                            fingerprint=fingerprint))
    return False
