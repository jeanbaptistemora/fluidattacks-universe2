# -*- coding: utf-8 -*-

"""This module allows to check SIP vulnerabilities."""

# standard imports
import base64
import email
import io
import re
import socket

# third party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import http
from fluidasserts.utils.decorators import track, level, notify


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


@notify
@level('low')
@track
def is_version_visible(server: str, port: int = 5060,
                       source_ip: str = '127.0.0.1',
                       source_port: int = 5060) -> bool:
    """
    Check if SIP server version is visible.

    :param ipaddress: IP address to test.
    :param port: Port to connect to.
    """
    request = f"""OPTIONS sip:100@{server} SIP/2.0
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

"""
    request = request.replace('\n', '\r\n')

    proto = None
    try:
        recv_data = _make_udp_request(server, port, request)
        proto = 'UDP'
    except socket.error:
        try:
            recv_data = _make_tcp_request(server, port, request)
            proto = 'TCP'
        except socket.error as exc:
            show_unknown('Could not connect',
                         details=dict(server=server, port=port, proto=proto,
                                      error=str(exc).replace(':', ',')))
            return False
    _, headers_alone = recv_data.split('\r\n', 1)
    message = email.message_from_file(io.StringIO(headers_alone))
    headers = dict(message.items())
    if 'Server' not in headers or 'User-Agent' not in headers:
        show_close('Server or User-Agent header were not returned',
                   details=dict(server=server, port=port, proto=proto))
        return False
    regex_match = re.search(r'([a-z-A-Z]+)[^a-zA-Z0-9](.*)',
                            headers['Server'])
    if regex_match:
        show_open('SIP server version visible',
                  details=dict(server=server, port=port, proto=proto,
                               product=regex_match.group(1),
                               version=regex_match.group(2)))
        result = True
    else:
        show_close('SIP server version not visible',
                   details=dict(server=server, port=port, proto=proto))
        result = False
    return result


@notify
@level('high')
@track
def unify_has_default_credentials(hostname: str,
                                  proto: str = 'https',
                                  port: int = '443',
                                  password: str = '123456') -> bool:
    """
    Check if Unify OpenScape Desk Phone IP 55G has default credentials.

    :param hostname: IP or host of phone.
    :param password: Default password.
    """
    try:
        url = '{}://{}:{}/index.cmd?user=Admin'.format(proto, hostname, port)
        sess = http.HTTPSession(url)

        if 'OpenScape Desk Phone IP Admin' not in sess.response.text:
            show_unknown('Resources not found. Is it a valid phone version?',
                         details=dict(host=hostname, url=url,
                                      status_code=sess.response.status_code))
            return False

        sess.data = 'page_submit=WEBMp_Admin_Login&lang=es&AdminPassword={}'\
            .format(password)
        sess.url = '{}://{}:{}/page.cmd'.format(proto, hostname, port)
        sess.do_request()
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(hostname=hostname, url=url,
                                  reason=str(exc).replace(':', ',')))
        return False

    failed = "action='./page.cmd'"

    if sess.response.status_code > 400:
        show_unknown('Resources not found. Is it a valid phone version?',
                     details=dict(host=hostname, url=url,
                                  status_code=sess.response.status_code))
        return False
    if failed not in sess.response.text:
        show_open('Phone has default credentials',
                  details=dict(host=hostname, username='Admin',
                               password=password))
        result = True
    else:
        show_close('Phone has not default credentials',
                   details=dict(host=hostname, username='Admin',
                                password=password))
        result = False
    return result


@notify
@level('high')
@track
def polycom_has_default_credentials(hostname: str,
                                    proto: str = 'https',
                                    port: int = '443',
                                    password: str = '456') -> bool:
    """
    Check if Polycom SoundStation IP 6000 has default credentials.

    :param hostname: IP or host of phone.
    :param password: Default password.
    """
    try:
        url = '{}://{}:{}/login.htm'.format(proto, hostname, port)
        sess = http.HTTPSession(url)
        if 'Polycom Web Configuration Utility' not in sess.response.text:
            show_unknown('Resources not found. Is it a valid phone version?',
                         details=dict(host=hostname, url=url,
                                      status_code=sess.response.status_code))
            return False
        creds = 'Polycom:{}'.format(password)
        encoded = base64.b64encode(creds.encode())

        sess.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        sess.headers.update({'Authorization': 'Basic {}'
                                              .format(encoded.decode())})
        sess.url = '{}://{}:{}/auth.htm?\
t=Tue,%2020%20Nov%202018%2019:48:43%20GMT'.format(proto, hostname, port)
        sess.do_request()
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(hostname=hostname, url=url,
                                  reason=str(exc).replace(':', ',')))
        return False
    expected = "SoundStation IP 6000"

    if sess.response.status_code > 401:
        show_unknown('Resources not found. Is it a valid phone version?',
                     details=dict(host=hostname, url=url,
                                  status_code=sess.response.status_code))
        return False
    if expected in sess.response.text:
        show_open('Phone has default credentials',
                  details=dict(host=hostname, username='Admin',
                               password=password))
        result = True
    else:
        show_close('Phone has not default credentials',
                   details=dict(host=hostname, username='Admin',
                                password=password))
        result = False
    return result
