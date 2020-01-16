# -*- coding: utf-8 -*-
"""This module provide a man in the middle Proxy."""

# standard imports
import os
import random
from typing import List
import string
from contextlib import contextmanager, suppress
from multiprocessing import Process
from collections import namedtuple
import pkg_resources

# 3rd party imports
from mitmproxy import proxy
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster

AddOn = namedtuple(
    'AddOn', ['request', 'response'], defaults=[None, ] * 2)


@contextmanager
def proxy_server(listen_host: str = '127.0.0.1',
                 listen_port: int = 8085,
                 addons: List[AddOn] = None,
                 ignore_hosts: List[str] = None,
                 **kwargs):
    """
    Create a man in the middle proxy.

    This proxy allow pass :class:`Addons` that modify the requests and
    responses that pass through the proxy. Each :class:`Addon` has two
    functions that are executed for each request that passes through the proxy,
    you must use enough validations to avoid errors in type of execution

    :param listen_host: Address to bind proxy to.
    :param listen_port: Proxy service port.
    :param addons: A list of modifications for requests and responses.
    :param ignore_hosts: Ignore host and forward all traffic without
     processing it.
    :param start: Start the proxy server immediately.
    :param kwargs: See all allowed option in `mitmproxy <https://docs.
     mitmproxy.org/stable/concepts-options/#available-options>`_

    :examples:
    - **Create a men in the middle proxy:**

      .. literalinclude:: example/create_proxy.py
          :linenos:
          :language: python

      `$ python3 create_proxy.py`:
    """
    ignore_hosts = [] if not ignore_hosts else ignore_hosts
    addons = [] if not addons else addons

    args = {
        'listen_host': listen_host,
        'listen_port': listen_port,
        'ignore_hosts': ignore_hosts,
        'confdir': _get_config_path(),
        **kwargs
    }
    opts = options.Options(**args)

    master = DumpMaster(opts)

    for addon in addons:
        master.addons.add(_refact_addon(addon))

    proxy_config = proxy.config.ProxyConfig(opts)
    master.server = proxy.server.ProxyServer(proxy_config)

    processor = Process(target=master.run, name='mitmproxy')
    processor.daemon = True
    try:
        yield processor.start()
    finally:
        master.shutdown()
        processor.kill()


def _refact_addon(addon: AddOn):
    _class = type('AddOn', (object, ), {'request': None, 'response': None})
    _class.request = addon.request
    _class.response = addon.response
    if not _class.request:
        _class.request = lambda x: x
    if not _class.response:
        _class.response = lambda x: x
    setattr(_class.request, 'name', 'request')
    setattr(_class.response, 'name', 'response')
    setattr(_class, 'name', _random_string())
    return _class


def _get_config_path():
    static_path = pkg_resources.resource_filename('fluidasserts', 'static/')
    with suppress(FileNotFoundError):
        os.rename(f'{static_path}mock_data_proxy/mitmproxy-ca',
                  f'{static_path}mock_data_proxy/mitmproxy-ca.pem')
    return f'{static_path}mock_data_proxy'


def get_firefox_profile_path():
    """Path of a Firefox profile that has the proxy certificate installed."""
    static_path = pkg_resources.resource_filename('fluidasserts', 'static/')
    return f'{static_path}mock_data_proxy/firefox_profile/'


def get_certificate_path():
    """Proxy certificate path in pem format."""
    static_path = pkg_resources.resource_filename('fluidasserts', 'static/')
    with suppress(FileNotFoundError):
        os.rename(f'{static_path}mock_data_proxy/mitmproxy-ca',
                  f'{static_path}mock_data_proxy/mitmproxy-ca.pem')
    return f'{static_path}mock_data_proxy/mitmproxy-ca.pem'


def _random_string(string_length=5):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, string_length))
