# -*- coding: utf-8 -*-

"""This module enables banner and fingerprint grabbing for other modules."""


# standard imports
from abc import ABCMeta
from abc import abstractmethod
import hashlib
import re
import socket
import ssl
from typing import Optional

# 3rd party imports
import certifi
import six

# local imports
from fluidasserts.helper import http


@six.add_metaclass(ABCMeta)
class Service():
    """Abstract class of service."""

    def __init__(self, port: int, is_active: bool,
                 is_ssl: bool, payload=None) -> None:
        """
        Build a new Service object.

        :param port: Port to connect to.
        :param is_active: Whether server is active.
        :param is_ssl: Whether connection is to be made via SSL.
        """
        self.port = port
        self.is_active = is_active
        self.is_ssl = is_ssl
        self.payload = payload

    def get_banner(self, server: str) -> str:
        """
        Get the banner of the service on a given port of an IP address.

        :param server: Server to connect to.
        """
        banner = ''
        try:
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.is_ssl:
                sock = ssl.SSLSocket(sock=raw_socket,
                                     ca_certs=certifi.where(),
                                     cert_reqs=ssl.CERT_REQUIRED,
                                     server_hostname=server)
            else:
                sock = raw_socket
            sock.connect((server, self.port))
            if self.payload is not None:
                sent_bytes = sock.send(self.payload.encode())
                if sent_bytes < len(self.payload):
                    raise socket.error
            banner = sock.recv(5096).decode('ISO-8859-1')
        except socket.error:
            raw_socket = False
            banner = ''
        finally:
            if raw_socket:
                raw_socket.close()

        return banner.rstrip()

    def get_fingerprint(self, server: str) -> dict:
        """
        Get fingerprint of the banner.

        :param server:
        """
        sha256 = hashlib.sha256()
        banner = self.get_banner(server)
        sha256.update(banner.encode('utf-8'))
        return dict(sha256=sha256.hexdigest(), banner=banner)

    @abstractmethod
    def get_version(self, server: str) -> None:
        """Parse the banner.

        Return the product and version of the service.
        """


class SMTPService(Service):
    """SMTP Service definition."""

    def __init__(self, port: int = 25, is_active: bool = False,
                 is_ssl: bool = False, payload: str = None) -> None:
        """Build a new Service object."""
        super(SMTPService, self).__init__(port=port,
                                          is_active=is_active,
                                          is_ssl=is_ssl,
                                          payload=payload)

    def get_version(self, server: str) -> Optional[str]:
        """
        Get version.

        :param server: Server to connect to.
        """
        regex_list = [r'220.*ESMTP (.*)',
                      r'214-2.0.0 This is sendmail version (.*)']
        banner = self.get_banner(server)
        for regex in regex_list:
            regex_match = re.search(regex, banner)
            if regex_match:
                return regex_match.group(1)
        return None


class HTTPService():
    """HTTP Service definition."""

    def __init__(self, url, *args, **kwargs) -> None:
        """Build a new Service object."""
        self.url = url
        self.sess = http.HTTPSession(self.url, *args, **kwargs)

    def get_banner(self) -> str:
        """Get HTTP Server banner."""
        try:
            banner = self.sess.response.headers['Server']
            return banner
        except KeyError:
            return ''

    def get_version(self) -> Optional[str]:
        """
        Get version.

        :param server: Server to connect to.
        """
        banner = 'Server: {}'.format(self.get_banner())
        regex_match = re.search(r'Server: [a-z-A-Z]+[^a-zA-Z0-9](.*)',
                                banner)
        if regex_match:
            return regex_match.group(1)
        return None

    def get_fingerprint(self) -> dict:
        """Get HTTP fingerprint."""
        return self.sess.get_fingerprint()


class SSHService(Service):
    """SSH Service definition."""

    def __init__(self, port: int = 22, is_active: bool = False,
                 is_ssl: bool = False, payload=None) -> None:
        """Build a new SSHService object."""
        super(SSHService, self).__init__(port=port,
                                         is_active=is_active,
                                         is_ssl=is_ssl,
                                         payload=payload)

    def get_version(self, server: str) -> Optional[str]:
        """
        Get version.

        :param server: Server to connect to.
        """
        banner = self.get_banner(server)
        regex_match = re.search(r'SSH-[0-9.-]+(.*)', banner)
        version = regex_match.group(1)
        if len(version) < 3:
            return False
        return version
