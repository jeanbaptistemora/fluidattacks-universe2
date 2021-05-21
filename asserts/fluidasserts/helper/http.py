# -*- coding: utf-8 -*-

"""This module provide support for HTTP connections."""

# pylint: disable=no-member
# pylint: disable=import-error
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access


# standard imports
import sys
import time
import hashlib
import tempfile
import textwrap
from contextlib import contextmanager
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, NoReturn, Optional, Tuple

# 3rd party imports
import yaml
import names
import selenium.webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from bs4 import BeautifulSoup
from PIL import Image
import requests
from requests_ntlm import HttpNtlmAuth
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


class HTTPSession:
    """Class of HTTP request objects."""

    def __init__(
        self,
        url: str,
        params: Optional[str] = None,
        headers: Optional[dict] = None,
        method: Optional[str] = None,
        cookies: requests.cookies.RequestsCookieJar = None,
        data: Optional[str] = "",
        json: Optional[dict] = None,
        files: Optional[dict] = None,
        auth: Optional[Tuple[str, str]] = None,
        redirect: Optional[bool] = True,
        timeout: Optional[float] = 10.0,
        stream: Optional[bool] = False,
        ntlm_auth: Optional[Tuple[str, str]] = None,
        request_at_instantiation: Optional[bool] = True,
        **requests_kwargs,
    ) -> None:
        r"""
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
        :param ntlm_auth: Auth tuple to enable NTLM Auth.
                          Takes ('domain\\username','password').
        :param redirect: Indicates if redirects should be followed.
        :param timeout: Time to wait for the response before raising a
                        timeout error.
        :param stream: If ``False``, the response content
                       will be immediately downloaded.
        :param requests_args: Extra positional keyword arguments that will
                              be sent to the underlying
                              :class:`~requests.Request`.
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
        self.ntlm_auth = ntlm_auth
        self.verb_used = None
        self.response = None  # type: requests.Response
        self.is_auth = False
        self.stream = stream
        self.redirect = redirect
        self.timeout = timeout
        self.requests_kwargs = requests_kwargs
        self._vulns: List[Unit] = []
        self._safes: List[Unit] = []
        self._source: str = None
        self._msg_open: str = None
        self._msg_closed: str = None
        if self.headers is None:
            self.headers = dict()
        if "User-Agent" not in self.headers:
            self.headers["User-Agent"] = (
                "Mozilla/5.0 (X11; Linux x86_64; rv"
                ":45.0) Gecko/20100101 Firefox/45.0"
            )
        if "Accept" not in self.headers:
            self.headers["Accept"] = "*/*"
        if "Accept-Language" not in self.headers:
            self.headers["Accept-Language"] = "en-US,en;q=0.5"

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
            Unit(
                where=self.url,
                source=self._source,
                specific=specific
                or [self._msg_open if is_vulnerable else self._msg_closed],
                fingerprint=self.get_fingerprint(),
            )
        )

    def set_messages(self, *, source: str, msg_open: str, msg_closed: str):
        """Set the open and closed msg attributes for this session."""
        self._source, self._msg_open, self._msg_closed = (
            source,
            msg_open,
            msg_closed,
        )

    def get_tuple_result(self) -> Tuple[str, str, List[Unit], List[Unit]]:
        """Return a :class:`typing.Tuple` version of the results object."""
        if self._vulns:
            return OPEN, self._msg_open, self._vulns, self._safes
        return CLOSED, self._msg_closed, self._vulns, self._safes

    def __do_post_json(self) -> Optional[requests.Response]:
        self.verb_used = "POST"
        try:
            return requests.post(
                self.url,
                verify=self.requests_kwargs.pop("verify", False),
                auth=HttpNtlmAuth(*self.ntlm_auth)
                if self.ntlm_auth
                else self.auth,
                json=self.json,
                cookies=self.cookies,
                headers=self.headers,
                stream=self.stream,
                allow_redirects=self.redirect,
                timeout=self.timeout,
                **self.requests_kwargs,
            )
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_post_files(self) -> Optional[requests.Response]:
        self.verb_used = "POST"
        try:
            return requests.post(
                self.url,
                verify=self.requests_kwargs.pop("verify", False),
                auth=HttpNtlmAuth(*self.ntlm_auth)
                if self.ntlm_auth
                else self.auth,
                files=self.files,
                cookies=self.cookies,
                headers=self.headers,
                stream=self.stream,
                allow_redirects=self.redirect,
                timeout=self.timeout,
                **self.requests_kwargs,
            )
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_get(self) -> Optional[requests.Response]:
        self.verb_used = "GET"
        try:
            return requests.get(
                self.url,
                verify=self.requests_kwargs.pop("verify", False),
                auth=HttpNtlmAuth(*self.ntlm_auth)
                if self.ntlm_auth
                else self.auth,
                params=self.params,
                cookies=self.cookies,
                headers=self.headers,
                stream=self.stream,
                allow_redirects=self.redirect,
                timeout=self.timeout,
                **self.requests_kwargs,
            )
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_post(self) -> Optional[requests.Response]:
        self.verb_used = "POST"
        try:
            return requests.post(
                self.url,
                verify=self.requests_kwargs.pop("verify", False),
                data=self.data,
                auth=HttpNtlmAuth(*self.ntlm_auth)
                if self.ntlm_auth
                else self.auth,
                params=self.params,
                cookies=self.cookies,
                headers=self.headers,
                files=self.files,
                stream=self.stream,
                allow_redirects=self.redirect,
                timeout=self.timeout,
                **self.requests_kwargs,
            )
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def __do_generic(self) -> Optional[requests.Response]:
        self.verb_used = self.method.upper()
        try:
            return requests.request(
                method=self.method,
                url=self.url,
                params=self.params,
                data=self.data,
                json=self.json,
                headers=self.headers,
                cookies=self.cookies,
                files=self.files,
                auth=HttpNtlmAuth(*self.ntlm_auth)
                if self.ntlm_auth
                else self.auth,
                timeout=self.timeout,
                allow_redirects=self.redirect,
                stream=self.stream,
                verify=self.requests_kwargs.pop("verify", False),
                **self.requests_kwargs,
            )
        except ConnError.errors as exc:
            raise ConnError(exc)
        except ParameterError.errors as exc:
            raise ParameterError(exc)

    def do_request(self) -> Optional[requests.Response]:
        """Do HTTP request."""
        if self.method:
            self.response = self.__do_generic()
        elif self.data == "":
            if self.json:
                self.response = self.__do_post_json()
            elif self.files:
                self.response = self.__do_post_files()
            else:
                self.response = self.__do_get()
        else:
            self.response = self.__do_post()
        if "Location" in self.response.headers:
            self.headers["Referer"] = self.response.headers["Location"]

        if self.response.url != self.url:
            self.url = self.response.url

        if self.response.cookies == {}:
            if (
                self.response.request._cookies != {}
                and self.cookies != self.response.request._cookies
            ):
                self.cookies = self.response.request._cookies
        else:
            self.cookies = self.response.cookies
        return self.response

    def formauth_by_response(self, text: str) -> requests.Response:
        """
        Authenticate using regex as verification.

        :param text: Regex to look for in request response.
        """
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"

        http_req = self.do_request()
        self.is_auth = bool(http_req.text.find(text) >= 0)

        if http_req.cookies == {}:
            if (
                http_req.request._cookies != {}
                and self.cookies != http_req.request._cookies
            ):
                self.cookies = http_req.request._cookies
        else:
            self.cookies = http_req.cookies
        self.response = http_req
        self.data = ""
        del self.headers["Content-Type"]
        return http_req

    def get_html_value(
        self,
        field_type: str,
        field_name: str,
        field_id: str = "name",
        field: Optional[str] = "value",
    ) -> str:
        """
        Get a value from an HTML field.

        :param field_type: Name of HTML tag type to look for, e.g. ``script``.
        :param field: Name of field, e.g. ``type``.
        :param enc: Whether to URL-encode the results.
        """
        soup = BeautifulSoup(self.response.text, "html.parser")
        result_tag = soup.find(field_type, {field_id: field_name})
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
            "Date",
            "Set-Cookie",
            "Last-Modified",
            "ETag" "x-amz-id-2",
            "x-amz-request-id",
            "CF-RAY",
            "CF-Visitor",
        )

        sha256 = hashlib.sha256()
        sha256.update(
            "\r\n".join(
                f"{header}: {value}"
                for header, value in self.response.headers.items()
                if header not in dynamic_headers
            ).encode("utf-8")
        )

        return dict(
            verb=self.verb_used,
            status=self.response.status_code,
            headers=OrderedDict(self.response.headers.copy()),
            sha256=sha256.hexdigest(),
        )


def _reindent_and_print(lines):
    """Reindent a list of lines and print it as commented yaml."""
    print(textwrap.indent("\n".join(lines), "# "), file=sys.stderr)


# pylint: disable=too-many-public-methods


class WebBot:
    """HTTP Automation Bot."""

    def __init__(
        self, developer_mode: bool = False, implicitly_wait: float = 8.0
    ) -> NoReturn:
        """
        :class:`.WebBot` Constructor.

        :param implicitly_wait: How many seconds will the Bot poll the
            DOM when trying to find any element (or elements) not immediately
            available.
        :param developer_mode: When set to True you'll get usefull messages
            to aid in the development of exploits, (it logs to console).
        """
        # Webdriver options
        webdriver_options = selenium.webdriver.firefox.options.Options()
        webdriver_options.add_argument("--headless")
        # Webdriver instance
        self.driver = selenium.webdriver.Firefox(options=webdriver_options)
        self.driver.implicitly_wait(implicitly_wait)
        self.driver.set_window_size(2560, 1080)

        # Properties used later
        self.bot_id: str = names.get_first_name()
        self.developer_mode: bool = developer_mode

    def __enter__(self):
        """Context manager for this class."""
        return self

    def __exit__(self, *kwargs):
        """Context manager clean up function."""
        self.driver.quit()

    #
    # Actions to perform
    #

    def visit(self, url: str):
        """Visit a url."""
        self._notify_action(f"visit", locals())
        self.driver.get(url)
        self._notify_result(None)

    def wait(self, seconds: float) -> NoReturn:
        """Wait ``seconds`` seconds."""
        self._notify_action(f"wait", locals())
        time.sleep(seconds)
        self._notify_result(None)

    def _fill_by(self, selector, identifier: str, fill_with: str):
        """Fill a *fillable* element identifying it by its ``selector``."""
        _args = locals()
        _args.pop("selector")
        self._notify_action(f"fill_by_{selector}", _args)

        success: bool = False
        function = getattr(self.driver, f"find_elements_by_{selector}")
        elements = function(identifier)
        if len(elements) > 1:
            self._notify_warning("More than one element found!")
        if elements:
            elements[0].send_keys(fill_with)
            success = True
        else:
            self._notify_warning("No elements found!")

        self._notify_result({"success": success})
        return success

    def fill_by_id(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``id``."""
        self._fill_by("id", identifier, fill_with)

    def fill_by_name(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``name``."""
        self._fill_by("name", identifier, fill_with)

    def fill_by_class_name(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``class name``."""
        self._fill_by("class_name", identifier, fill_with)

    def fill_by_css_selector(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``css selector``."""
        self._fill_by("css_selector", identifier, fill_with)

    def fill_by_link_text(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``link text``."""
        self._fill_by("link_text", identifier, fill_with)

    def fill_by_partial_link_text(self, identifier: str, fill_with: str):
        """Fill an element identifying it by ``partial link text``."""
        self._fill_by("partial_link_text", identifier, fill_with)

    def fill_by_xpath(self, identifier: str, fill_with: str):
        """Fill an element identifying it by its ``xpath``."""
        self._fill_by("xpath", identifier, fill_with)

    def _click_by(self, selector, identifier: str):
        """Click a *clickable* element identifying it by its ``selector``."""
        _args = locals()
        _args.pop("selector")
        self._notify_action(f"click_by_{selector}", _args)

        success: bool = False
        function = getattr(self.driver, f"find_elements_by_{selector}")
        elements = function(identifier)
        if len(elements) > 1:
            self._notify_warning("More than one element found!")
        if elements:
            elements[0].click()
            success = True
        else:
            self._notify_warning("No elements found!")

        self._notify_result({"success": success})
        return success

    def click_by_name(self, identifier: str):
        """Click an element identifying it by its ``name``."""
        self._click_by("name", identifier)

    def click_by_link_text(self, identifier: str):
        """Click an element identifying it by its ``link text``."""
        self._click_by("link_text", identifier)

    def click_by_partial_link_text(self, identifier: str):
        """Click an element identifying it by its ``partial link text``."""
        self._click_by("partial_link_text", identifier)

    def click_by_human_text(self, identifier: str):
        """Click an element identifying it by the ``visible text``."""
        self._notify_action("click_by_human_text", locals())

        success: bool = False
        elements = tuple(
            element
            for element in self._get_clickables()
            if identifier == element.text
        )

        if len(elements) > 1:
            self._notify_warning("More than one element found!")
        if elements:
            elements[0].click()
            success = True
        else:
            self._notify_warning("No elements found!")

        self._notify_result({"success": success})
        return success

    def show_me(self):
        """Take an snapshot and display it in the default image viewer."""
        self._notify_action("show_me", locals())
        success: bool = False

        file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        file.close()

        success = self.driver.save_screenshot(file.name)

        image = Image.open(file.name)
        image.show()
        self._notify_result({"success": success})

    def send_enter(self):
        """Send an ``Enter`` to the current active element."""
        self._notify_action("send_enter", locals())
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    #
    # Interface to current state data
    #

    def get_cookie(self, name: str):
        """Return a cookie in the current session."""
        self._notify_action(f"get_cookie", locals())
        cookie = self.driver.get_cookie(name)
        self._notify_result(cookie)
        return cookie

    def get_cookies(self):
        """Return all cookies in the current session."""
        self._notify_action("get_cookies", locals())
        cookies = self.driver.get_cookies()
        self._notify_result(cookies)
        return cookies

    def get_cookies_as_dict(self) -> Dict[str, str]:
        """Return all cookies in the current session as a dictionary."""
        self._notify_action("get_cookies_as_dict", locals())
        cookies: Dict[str, str] = {
            cookie["name"]: cookie["value"]
            for cookie in self.driver.get_cookies()
        }
        self._notify_result(cookies)
        return cookies

    def get_cookies_as_jar(self) -> requests.cookies.RequestsCookieJar:
        """Return all cookies in the current session as a RequestsCookieJar."""
        self._notify_action("get_cookies_as_jar", locals())
        cookies = requests.cookies.RequestsCookieJar()
        for cookie in self.driver.get_cookies():
            cookies.set_cookie(
                requests.cookies.create_cookie(
                    name=cookie["name"],
                    value=cookie["value"],
                    version=cookie.get("version", 0),
                    domain=cookie.get("domain", ""),
                    path=cookie.get("path", "/"),
                    port=cookie.get("port"),
                    secure=cookie.get("secure", False),
                    expires=cookie.get("expiry"),
                    discard=cookie.get("discard", False),
                    comment=cookie.get("comment"),
                    comment_url=cookie.get("comment_url"),
                    rest={
                        "HttpOnly": cookie.get("httpOnly"),
                        "SameSite": cookie.get("sameSite"),
                    },
                )
            )
        self._notify_result(cookies)
        return cookies

    def get_source(self) -> str:
        """Return the current page source code."""
        self._notify_action("get_source", locals())
        source_code: BeautifulSoup = BeautifulSoup(
            self.driver.page_source, features="html.parser"
        )
        self._notify_result(source_code.prettify())
        return source_code

    #
    # Debuggers
    #

    @contextmanager
    def _no_dev_mode(self):
        """Temporarily disable the developer mode."""
        old_value = self.developer_mode
        self.developer_mode = False
        try:
            yield
        finally:
            self.developer_mode = old_value

    def _notify_action(self, where: str, args) -> NoReturn:
        """Notify to stderr what's being done by the bot."""
        if self.developer_mode:
            _args = args.copy()
            _args.pop("self")
            lines = []
            lines.append(f"---")
            lines.append(f"Bot[{self.bot_id}].{where}:")

            if _args:
                lines.append("  Args:")
                _args = textwrap.indent(
                    yaml.dump(_args, allow_unicode=True)[:-1], "    "
                )
                lines.append(_args)
            _reindent_and_print(lines)

    def _notify_result(self, body: Any) -> NoReturn:
        """Notify to stderr what's being done by the bot."""
        if self.developer_mode and body:
            lines = []
            lines.append("  Result:")
            lines.append(
                textwrap.indent(
                    yaml.dump(body, allow_unicode=True)[:-1], prefix="    "
                )
            )
            _reindent_and_print(lines)

    def _notify_warning(self, text: Any) -> NoReturn:
        """Notify to stderr what's being done by the bot."""
        if self.developer_mode:
            lines = []
            lines.append(f"    Warning: {text}")
            _reindent_and_print(lines)

    def get_fillables(self, show_hidden: bool = False) -> Tuple[dict]:
        """Print a list of possible fields to fill."""
        self._notify_action("get_fillables", locals())
        with self._no_dev_mode():
            fillables: Tuple[dict, ...] = tuple(
                {
                    "id": element.get_attribute("id"),
                    "name": element.get_attribute("name"),
                    "type": element.get_attribute("type"),
                    "value": element.get_attribute("value"),
                }
                for element in self.driver.find_elements_by_tag_name("input")
            )
            if not show_hidden:
                fillables = tuple(
                    filter(lambda x: x["type"] != "hidden", fillables)
                )

        self._notify_result(fillables)
        return fillables

    def _get_clickables(self) -> Iterable[WebElement]:
        """Yield clickable WebElements."""
        for element in self.driver.find_elements_by_tag_name("button"):
            # A button, we want to click that
            yield element

        found_texts: set = set()
        for element in reversed(self.driver.find_elements_by_tag_name("div")):
            # A decorative div
            if not element.text:
                continue
            element_parents = element.find_elements_by_xpath("..")
            if not element_parents or any(
                isinstance(x, WebDriver) for x in element_parents
            ):
                # This is the top level div
                continue
            if element_parents[0].text == element.text:
                # There is a more generic div with the same contents
                continue
            if any(ft in element.text for ft in found_texts):
                # This is generic div
                continue

            found_texts.add(element.text)
            yield element

    def get_clickables(self) -> Tuple[dict, ...]:
        """Print a list of possible elements to click."""
        self._notify_action("get_clickables", locals())

        fillables: Tuple[dict, ...] = tuple(
            {
                "tag": element.tag_name,
                "id": element.get_attribute("id"),
                "name": element.get_attribute("name"),
                "type": element.get_attribute("type"),
                "value": element.get_attribute("value"),
                "class": element.get_attribute("class"),
                "human_text": element.text,
                "human_size": f'x={element.size["height"]} y={element.size["width"]}',
                "human_location": f'x={element.location["x"]} y={element.location["y"]}',
            }
            for element in self._get_clickables()
        )

        self._notify_result(fillables)
        return fillables
