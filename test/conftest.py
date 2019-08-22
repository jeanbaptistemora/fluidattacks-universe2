# -*- coding: utf-8 -*-

"""Unit test config module."""

# standard imports
from __future__ import print_function
from multiprocessing import Process
import os
import time
import sys

# 3rd party imports
import docker
import pytest
import wait

# local imports
from test.mock import graphqlserver
from test.mock import httpserver
from test.mock import sip

# Constants
NETWORK_NAME = 'bridge'

MOCKS = {
    # This need to be built first
    'dns:weak': {'53/tcp': 53, '53/udp': 53},
    'ftp:weak': {'21/tcp': 21},
    'mysql_db:weak': {'3306/tcp': 3306},
    'mysql_os:hard': {'22/tcp': 22},
    'smb:weak': {'139/tcp': 139},
    'smtp:weak': {'25/tcp': 25},

    # Some of these are built in top of the previous ones
    'bwapp': {'80/tcp': 80},
    'dns:hard': {'53/tcp': 53, '53/udp': 53},
    'ftp:hard': {'21/tcp': 21},
    'ldap:hard': {'389/tcp': 389},
    'ldap:weak': {'389/tcp': 389},
    'mysql_db:hard': {'3306/tcp': 3306},
    'mysql_os:weak': {'22/tcp': 22},
    'os:hard': {'22/tcp': 22},
    'os:weak': {'22/tcp': 22},
    'postgresql:hard': {'5432/tcp': 5432},
    'postgresql:weak': {'5432/tcp': 5432},
    'smb:hard': {'139/tcp': 139},
    'smtp:hard': {'25/tcp': 25},
    'ssl:hard': {'443/tcp': 443},
    'ssl:hard_tlsv13': {'443/tcp': 443},
    'ssl:weak': {'443/tcp': 443},
    'tcp:hard': {'443/tcp': 443},
    'tcp:weak': {'80/tcp': 80},
}


def get_docker_client():
    """Get docker client."""
    client = docker.from_env()
    client.login(registry='registry.gitlab.com',
                 username=os.environ['DOCKER_USER'],
                 password=os.environ['DOCKER_PASS'])
    return client


def get_mock_name(mock):
    """Get mock IP."""
    try:
        mock_name = '{}_{}'.format(mock.replace(':', '_'),
                                   os.environ['CI_COMMIT_REF_NAME'])
    except KeyError:
        print('CI_COMMIT_REF_NAME not in environ')
        sys.exit(-1)
    return mock_name


def get_ip(con):
    """Get mock IP."""
    return con.attrs['NetworkSettings']['Networks']\
        ['bridge']['IPAddress']


@pytest.fixture(scope='session', autouse=True)
def mock_sip(request):
    """Start SIP mock endpoints."""
    prcs = Process(target=sip.start, name='MockHTTPServer')
    prcs.daemon = True
    prcs.start()
    time.sleep(1)


@pytest.fixture(scope='session', autouse=True)
def mock_http(request):
    """Inicia y detiene el servidor HTTP antes de ejecutar una prueba."""
    prcs = Process(target=httpserver.start, name='MockHTTPServer')
    prcs.daemon = True
    prcs.start()
    time.sleep(1)


@pytest.fixture(scope='session', autouse=True)
def mock_graphql(request):
    """Start and stop the Graphql server."""
    prcs = Process(target=graphqlserver.start, name='GraphQL Mock Server')
    prcs.daemon = True
    prcs.start()
    time.sleep(1.0)


@pytest.fixture()
def run_mocks(request):
    """Run mock with given parameters."""
    client = get_docker_client()

    for mock, port_mapping in MOCKS.items():
        image = f'registry.gitlab.com/fluidattacks/asserts/mocks/{mock}'
        mock_dir = f'test/provision/{mock.replace(":", "/")}'

        mock_name = get_mock_name(mock)

        try:
            cont = client.containers.get(mock_name)
            cont.start()
        except docker.errors.NotFound:
            print('Building {} ... '.format(image))
            client.images.build(path=mock_dir, tag=image)
            try:
                print('Running {} ... '.format(mock_name))
                client.containers.run(image, name=mock_name,
                                      tty=True, detach=True)
            except docker.errors.APIError:
                print('Starting {} ... '.format(mock_name))
                cont = client.containers.get(mock_name)
                cont.start()

    for mock, port_mapping in MOCKS.items():
        ip = get_ip(client.containers.get(get_mock_name(mock)))
        for value in port_mapping.values():
            wait.tcp.open(value, ip, timeout=30)


@pytest.fixture()
def stop_mocks(request):
    """Stop mocks mock with given parameters."""
    client = get_docker_client()

    for mock, port_mapping in MOCKS.items():
        image = f'registry.gitlab.com/fluidattacks/asserts/mocks/{mock}'
        mock_dir = f'test/provision/{mock.replace(":", "/")}'

        mock_name = get_mock_name(mock)

        cont = client.containers.get(mock_name)
        cont.stop(timeout=0)


@pytest.fixture(scope='function')
def get_mock_ip(request):
    """Run mock with given parameters."""
    mock = request.param
    client = docker.from_env()
    con = client.containers.get(get_mock_name(mock))
    if con.status != 'running':
        con.start()
    yield get_ip(con)
