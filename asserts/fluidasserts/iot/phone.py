# -*- coding: utf-8 -*-

"""This module allows to check SIP vulnerabilities."""

# standard imports
import io
import re
import email
import base64
import socket
import textwrap
from typing import Dict

# local imports
from fluidasserts import DAST, LOW, HIGH, _get_result_as_tuple_host_port
from fluidasserts.helper import http
from fluidasserts.utils.decorators import unknown_if, api


def _make_udp_request(server: str, port: int, data: str):
    """Make UDP request to SIP server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    while data:
        bytes_sent = sock.sendto(data[:8192].encode(), (server, port))
        data = data[bytes_sent:]
    buff, _ = sock.recvfrom(8192)
    return buff.decode()


def _make_tcp_request(server: str, port: int, data: str):
    """Make TCP request to SIP server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((server, port))
    sock.send(data.encode())
    buff = sock.recv(8192)
    return buff.decode()


@api(risk=LOW, kind=DAST)
@unknown_if(socket.error)
def is_version_visible(server: str, port: int = 5060,
                       source_ip: str = '127.0.0.1',
                       source_port: int = 5060) -> tuple:
    """
    Check if SIP server version is visible.

    :param server: IP address to test.
    :param port: Port to connect to.
    """
    is_vulnerable: bool = False
    fingerprint: Dict[str, str] = {}
    request: str = textwrap.dedent(f"""
        OPTIONS sip:100@{server} SIP/2.0
        Via: SIP/2.0/UDP {source_ip}:{source_port};rport
        Content-Length: 0
        From: "fake" <sip:fake@{source_ip}>
        Accept: application/sdp
        User-Agent: Fluid Asserts
        To: <sip:100@1.1.1.1>
        Contact: sip:fake@{source_ip}:{source_port}
        CSeq: 1 OPTIONS
        Call-ID: fake-id@{source_ip}
        Max-Forwards: 70

        """)[1:].replace('\n', '\r\n')

    try:
        recv_data = _make_udp_request(server, port, request)
    except socket.error:
        recv_data = _make_tcp_request(server, port, request)

    _, headers_alone = recv_data.split('\r\n', 1)
    message = email.message_from_file(io.StringIO(headers_alone))
    headers = dict(message.items())

    if 'Server' in headers and 'User-Agent' in headers:
        is_vulnerable = re.search(
            r'([a-z-A-Z]+)[^a-zA-Z0-9](.*)', headers['Server'])

        if is_vulnerable:
            fingerprint.update({
                'product': is_vulnerable.group(1),
                'version': is_vulnerable.group(2)
            })

    return _get_result_as_tuple_host_port(
        protocol='SIP', host=server, port=port,
        msg_open='Version is visible',
        msg_closed='Version is not visible',
        open_if=is_vulnerable,
        fingerprint=fingerprint)


@api(risk=HIGH, kind=DAST)
@unknown_if(AssertionError, http.ConnError)
def unify_has_default_credentials(hostname: str,
                                  proto: str = 'https',
                                  port: int = '443',
                                  password: str = '123456') -> tuple:
    """
    Check if Unify OpenScape Desk Phone IP 55G has default credentials.

    :param hostname: IP or host of phone.
    :param password: Default password.
    """
    session = http.HTTPSession(
        f'{proto}://{hostname}:{port}/index.cmd?user=Admin')

    if 'OpenScape Desk Phone IP Admin' not in session.response.text:
        raise AssertionError(
            'Resource not found. Is it a valid phone version?')

    session.url = f'{proto}://{hostname}:{port}/page.cmd'
    session.data: str = \
        f'page_submit=WEBMp_Admin_Login&lang=es&AdminPassword={password}'
    session.do_request()

    if session.response.status_code > 400:
        raise AssertionError(
            'Resources not found. Is it a valid phone version?')

    session.set_messages(
        source='Unify OpenScape Desk Phone IP 55G/Credentials',
        msg_open='Phone has default credentials',
        msg_closed='Phone has not default credentials')
    session.add_unit(
        is_vulnerable="action='./page.cmd'" not in session.response.text)
    return session.get_tuple_result()


@api(risk=HIGH, kind=DAST)
@unknown_if(AssertionError, http.ConnError)
def polycom_has_default_credentials(hostname: str,
                                    proto: str = 'https',
                                    port: int = '443',
                                    password: str = '456') -> tuple:
    """
    Check if Polycom SoundStation IP 6000 has default credentials.

    :param hostname: IP or host of phone.
    :param password: Default password.
    """
    url: str = f'{proto}://{hostname}:{port}/login.htm'
    encoded: str = base64.b64encode(f'Polycom:{password}'.encode())

    session = http.HTTPSession(url)

    if 'Polycom Web Configuration Utility' not in session.response.text:
        raise AssertionError(
            'Resources not found. Is it a valid phone version?')

    session.url = (f'{proto}://{hostname}:{port}/auth.htm'
                   '?t=Tue,%2020%20Nov%202018%2019:48:43%20GMT')
    session.headers.update({
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': f'Basic {encoded.decode()}',
    })
    session.do_request()

    if session.response.status_code > 401:
        raise AssertionError(
            'Resources not found. Is it a valid phone version?')

    session.set_messages(
        source='Unify OpenScape Desk Phone IP 55G/Credentials',
        msg_open='Phone has default credentials',
        msg_closed='Phone has not default credentials')
    session.add_unit(
        is_vulnerable='SoundStation IP 6000' in session.response.text)
    return session.get_tuple_result()
