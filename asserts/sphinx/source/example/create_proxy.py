import time
import json
import requests
from pathlib import Path
from mitmproxy.http import HTTPFlow
from fluidasserts.helper.proxy import (proxy_server, AddOn,
                                       get_certificate_path)

HOST = '127.0.0.1'
PORT = 8085
API_HOST = 'https://pokeapi.co/api/v2/'

PROXIES = {'http': f'http://{HOST}:{PORT}', 'https': f'https://{HOST}:{PORT}'}


def mod_request(flow: HTTPFlow):
    # Change the required pokemon
    flow.request.url = flow.request.url.replace('ditto', 'piplup')


def mod_response(flow: HTTPFlow) -> None:
    pokemon = json.loads(flow.response.content.decode('utf-8'))
    # Rename the pokemon
    pokemon['name'] = 'mew'
    flow.response.content = str(json.dumps(pokemon)).encode('utf-8')


addons = [
    AddOn(response=mod_response, request=mod_request),
]

with proxy_server(listen_port=PORT, addons=addons):
    ditto = requests.get(
        f'{API_HOST}pokemon/ditto/',
        proxies=PROXIES,
        verify=get_certificate_path())
    print(f'Now the name of the pokemon is: {ditto.json()["name"]}')
