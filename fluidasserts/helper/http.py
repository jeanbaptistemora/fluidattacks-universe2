# -*- coding: utf-8 -*-

"""This module provide support for HTTP connections."""

# pylint: disable=no-member
# pylint: disable=import-error
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access


# standard imports
import hashlib
from collections import OrderedDict
from typing import List, Optional, Tuple

# 3rd party imports
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# local imports
from fluidasserts import Unit, OPEN, CLOSED


# On call
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ConnError(Exception):
    """A connection error occurred."""

    errors: tuple = (
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.ContentDecodingError,
        requests.exceptions.HTTPError,
        requests.exceptions.ProxyError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.RetryError,
        requests.exceptions.SSLError,
        requests.exceptions.StreamConsumedError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.UnrewindableBodyError,
    )


class ParameterError(Exception):
    """A parameter (user input) error occurred."""

    errors: tuple = (
        requests.exceptions.URLRequired,
        requests.exceptions.InvalidHeader,
        requests.exceptions.InvalidProxyURL,
        requests.exceptions.InvalidSchema,
        requests.exceptions.InvalidURL,
        requests.exceptions.MissingSchema,
    )


class HTTPSession():
    """Class of HTTP request objects."""

    def __init__(self,
                 url: str,
                 params: Optional[str] = None,
                 headers: Optional[dict] = None,
                 method: Optional[str] = None,
                 cookies: requests.cookies.RequestsCookieJar = None,
                 data: Optional[str] = '',
                 json: Optional[dict] = None,
                 files: Optional[dict] = None,
                 auth: Optional[Tuple[str, str]] = None,
                 redirect: Optional[bool] = True,
                 timeout: Optional[float] = 10.0,
                 stream: Optional[bool] = False,
                 request_at_instantiation: bool = True) -> None:
        """
        Construct method.

        :param url: URL for the new :class:`.HTTPSession` object.
        :param params: Parameters to send with the :class:`requests.Request`.
                       the :class:`~requests.Request` body.
        :param headers: Dict of HTTP headers to send with the Request.
        :param method: Must be either ``OPTIONS``, ``HEAD``, ``PUT``,
                       ``PATCH``, or ``DELETE``.
        :param cookies: Dict or CookieJar object to send with the Request.
        :param data: Payload to be sent in
                     the :class:`~requests.Request` body.
        :param json: Dictionary to be sent in
                     the :class:`~requests.Request` body.
        :param files: Dictionary of ``'name': file-like-objects``
                      for multipart encoding upload.
        :param auth: Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param redirect: Indicates if redirects should be followed.
        :param timeout: Time to wait for the response before raising a
                        timeout error.
        :param stream: If ``False``, the response content
                       will be immediately downloaded.
        """
        self.url = url
        self.params = params
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.json = json
        self.auth = auth
        self.files = files
        self.method = method
        self.verb_used = None
        self.response = None  # type: requests.Response
        self.is_auth = False
        self.stream = stream
        self.redirect = redirect
        self.timeout = timeout
        self._vulns: List[Unit] = []
        self._safes: List[Unit] = []
        self._source: str = None
        self._msg_open: str = None
        self._msg_closed: str = None
        if self.headers is None:
            self.headers = dict()
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = ('Mozilla/5.0 (X11; Linux x86_64; rv'
                                          ':45.0) Gecko/20100101 Firefox/45.0')
        if 'Accept' not in self.headers:
            self.headers['Accept'] = '*/*'
        if 'Accept-Language' not in self.headers:
            self.headers['Accept-Language'] = 'en-US,en;q=0.5'

        if request_at_instantiation:
            self.do_request()

    def __enter__(self):
        """Context manager for this class."""
        return self

    def __exit__(self, *kwargs) -> None:
        """Context manager clean up function."""

    def add_unit(self, *, is_vulnerable: bool, specific: list = None) -> None:
        """Append a new :class:`fluidasserts.Unit` object to this session."""
        (self._vulns if is_vulnerable else self._safes).append(
            Unit(where=self.url,
                 source=self._source,
                 specific=specific or [
                     self._msg_open if is_vulnerable else self._msg_closed],
                 fingerprint=self.get_fingerprint()))

    def set_messages(self, *, source: str, msg_open: str, msg_closed: str):
        """Set the open and closed msg attributes for this session."""
        self._source, self._msg_open, self._msg_closed = \
            source, msg_open, msg_closed

    def get_tuple_result(self) -> Tuple[str, str, List[Unit], List[Unit]]:
        """Return a :class:`typing.Tuple` version of the results object."""
        if self._vulns:
            return OPEN, self._msg_open, self._vulns, self._safes
        return CLOSED, self._msg_closed, self._vulns, self._safes

    def __do_post_json(self) -> Optional[requests.Response]:
        self.verb_used = 'POST'
        try:
            return requests.post(self.url, verify=False,
                                 auth=self.auth,
                                 json=self.json,
                                 cookies=self.cookies,
                                 headers=self.headers,
                                 stream=self.stream,
                                 allow_redirects=self.redirect,
                                 timeout=self.timeout)
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_post_files(self) -> Optional[requests.Response]:
        self.verb_used = 'POST'
        try:
            return requests.post(self.url, verify=False,
                                 auth=self.auth,
                                 files=self.files,
                                 cookies=self.cookies,
                                 headers=self.headers,
                                 stream=self.stream,
                                 allow_redirects=self.redirect,
                                 timeout=self.timeout)
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_get(self) -> Optional[requests.Response]:
        self.verb_used = 'GET'
        try:
            return requests.get(self.url, verify=False,
                                auth=self.auth,
                                params=self.params,
                                cookies=self.cookies,
                                headers=self.headers,
                                stream=self.stream,
                                allow_redirects=self.redirect,
                                timeout=self.timeout)
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_post(self) -> Optional[requests.Response]:
        self.verb_used = 'POST'
        try:
            return requests.post(self.url, verify=False,
                                 data=self.data,
                                 auth=self.auth,
                                 params=self.params,
                                 cookies=self.cookies,
                                 headers=self.headers,
                                 files=self.files,
                                 stream=self.stream,
                                 allow_redirects=self.redirect,
                                 timeout=self.timeout)
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_generic(self) -> Optional[requests.Response]:
        self.verb_used = self.method.upper()
        try:
            return requests.request(method=self.method,
                                    url=self.url,
                                    params=self.params,
                                    data=self.data,
                                    json=self.json,
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    files=self.files,
                                    auth=self.auth,
                                    timeout=self.timeout,
                                    allow_redirects=self.redirect,
                                    stream=self.stream,
                                    verify=False)
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def do_request(self) -> Optional[requests.Response]:
        """Do HTTP request."""
        if self.method:
            self.response = self.__do_generic()
        elif self.data == '':
            if self.json:
                self.response = self.__do_post_json()
            elif self.files:
                self.response = self.__do_post_files()
            else:
                self.response = self.__do_get()
        else:
            self.response = self.__do_post()
        if 'Location' in self.response.headers:
            self.headers['Referer'] = self.response.headers['Location']

        if self.response.url != self.url:
            self.url = self.response.url

        if self.response.cookies == {}:
            if (self.response.request._cookies != {} and
                    self.cookies != self.response.request._cookies):
                self.cookies = self.response.request._cookies
        else:
            self.cookies = self.response.cookies
        return self.response

    def formauth_by_response(self, text: str) -> requests.Response:
        """
        Authenticate using regex as verification.

        :param text: Regex to look for in request response.
        """
        self.headers['Content-Type'] = \
            'application/x-www-form-urlencoded'

        http_req = self.do_request()
        self.is_auth = bool(http_req.text.find(text) >= 0)

        if http_req.cookies == {}:
            if http_req.request._cookies != {} and \
                    self.cookies != http_req.request._cookies:
                self.cookies = http_req.request._cookies
        else:
            self.cookies = http_req.cookies
        self.response = http_req
        self.data = ''
        del self.headers['Content-Type']
        return http_req

    def get_html_value(self, field_type: str, field_name: str,
                       field_id: str = 'name',
                       field: Optional[str] = 'value') -> str:
        """
        Get a value from an HTML field.

        :param field_type: Name of HTML tag type to look for, e.g. ``script``.
        :param field: Name of field, e.g. ``type``.
        :param enc: Whether to URL-encode the results.
        """
        soup = BeautifulSoup(self.response.text, 'html.parser')
        result_tag = soup.find(field_type,
                               {field_id: field_name})
        text_to_get = None
        if result_tag:
            text_to_get = result_tag[field]
        return text_to_get

    def get_fingerprint(self) -> Optional[dict]:
        """
        Get HTTP fingerprint.

        :return: A dict containing the SHA and banner of the host,
                 as per :meth:`Service.get_fingerprint()`.
        """
        if not self.response:
            return None

        dynamic_headers = (
            'Date', 'Set-Cookie', 'Last-Modified', 'ETag'
            'x-amz-id-2', 'x-amz-request-id',
            'CF-RAY', 'CF-Visitor')

        sha256 = hashlib.sha256()
        sha256.update(
            '\r\n'.join(
                f'{header}: {value}'
                for header, value in self.response.headers.items()
                if header not in dynamic_headers).encode('utf-8'))

        return dict(verb=self.verb_used,
                    status=self.response.status_code,
                    headers=OrderedDict(self.response.headers.copy()),
                    sha256=sha256.hexdigest())
