# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.helper.http."""

# standard library
from fluidasserts.helper.proxy import (
    proxy_server, AddOn, get_certificate_path)
import requests
import json

# 3rd party imports
from mitmproxy.http import HTTPFlow
import pytest
pytestmark = pytest.mark.asserts_module('helper')

# local imports

#
# Helpers
#

HOST = '127.0.0.1'
PORT = 8086
API_HOST = 'https://pokeapi.co/api/v2/'

PROXIES = {'http': f'http://{HOST}:{PORT}', 'https': f'https://{HOST}:{PORT}'}


def _mod_request(flow: HTTPFlow):
    request: requests.Request = flow.request
    request.url = request.url.replace('ditto', 'piplup')


def _mod_response(flow: HTTPFlow) -> None:
    response = flow.response
    value = json.loads(response.content.decode('utf-8'))
    value['name'] = 'piplup'
    response.content = str(json.dumps(value)).encode('utf-8')


#
# Functional tests
#


def test_modify_ulr_request():
    """Modify the URL of the requests."""
    addons = [AddOn(_mod_request)]

    with proxy_server(listen_port=PORT, addons=addons):
        ditto = requests.get(
            f'{API_HOST}pokemon/ditto/',
            proxies=PROXIES,
            verify=get_certificate_path())
        assert ditto.json()['name'] == 'piplup'


def test_modify_response():
    """Modify the responses."""
    addons = [AddOn(response=_mod_response)]

    with proxy_server(listen_port=PORT, addons=addons):
        ditto = requests.get(
            f'{API_HOST}pokemon/ditto/',
            proxies=PROXIES,
            verify=get_certificate_path())
        assert ditto.json()['name'] == 'piplup'
