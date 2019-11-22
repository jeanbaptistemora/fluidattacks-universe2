# -*- coding: utf-8 -*-

"""Unit test config module."""

# standard imports
from __future__ import print_function
import os
import time
from git import Repo
from typing import Optional
from multiprocessing import Process, cpu_count
from multiprocessing.pool import Pool

# 3rd party imports
import docker
import pytest
import wait
from docker.models.containers import Image, Container

# local imports
from test.mock import graphqlserver
from test.mock import httpserver
from test.mock import sip
from test.mock import camera_hard
from test.mock import camera_weak

# Constants
CLIENT = docker.from_env()

MOCKS = [
    # These need to be built first
    {
        'dns:weak': {'53/tcp': 53, '53/udp': 53},
        'ftp:weak': {'21/tcp': 21},
        'mysql_db:weak': {'3306/tcp': 3306},
        'mysql_os:hard': {'22/tcp': 22},
        'smb:weak': {'139/tcp': 139},
        'smtp:weak': {'25/tcp': 25},
    },
    # Some of these are built in top of the previous ones
    {
        'bwapp': {'80/tcp': 80},
        'dns:hard': {'53/tcp': 53, '53/udp': 53},
        'ftp:hard': {'21/tcp': 21},
        'ldap:hard': {'389/tcp': 389},
        'ldap:weak': {'389/tcp': 389},
        'mysql_db:hard': {'3306/tcp': 3306},
        'mysql_os:weak': {'22/tcp': 22},
        'mssql:weak': {'1432/tcp': 1432},
        'mssql:hard': {'1433/tcp': 1433},
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
        'aws:weak': {
            '8080/tcp': 8080,
            }
    }
]


POST_COMMANDS = {
    'postgresql:hard': [
        """
        psql --user postgres
             --command "ALTER USER postgres WITH PASSWORD 'postgres'"
        """,
    ],
    'mssql:weak': ['./scripts/commands.sh', ],
    'mssql:hard': ['./scripts/commands.sh', ],
    'aws:weak': ['bash /scripts/commands.sh'],
}


ENVS = {
    'aws:weak': [f'LOCALSTACK_API_KEY={os.environ["LOCALSTACK_API_KEY"]}']
}


def get_mock_name(mock: str) -> str:
    """Get mock name."""
    branch = os.environ.get('CI_COMMIT_REF_NAME', 'test')
    mock_name = f'{mock.replace(":", "_")}_{branch}'
    return mock_name


def get_mock_key(mock_name: str):
    """Get mock key."""
    mock = mock_name.split('_')
    return ':'.join(mock[0:2])


def get_container_ip(cont: Container) -> str:
    """Get mock IP."""
    return cont.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']


def image_to_digest(image: Image) -> int:
    """Return an image digest from the Image object."""
    # Repositories have the digest, but local images don't, let's compute one
    #   https://windsock.io/explaining-docker-image-ids/
    entries: tuple = tuple(image.attrs.get('RootFS', {}).get('Layers', []))
    return hash(entries)


def get_existing_image(image: str) -> Optional[int]:
    """Return the image digest or None if the image does not exist."""
    try:
        print(f'Get image: {image}')
        img_obj = CLIENT.images.get(image)
    except docker.errors.NotFound:
        print(f'Image not found: {image}')
        return None
    return image_to_digest(img_obj)


def build_image(image: str, context: str) -> Optional[int]:
    """Build an image and return its digest or None if the build fails."""
    try:
        print(f'Build image: {image}')
        img_obj, _ = CLIENT.images.build(tag=image, path=context)
    except docker.errors.BuildError as exc:
        print(f'Build image failed: {image} {exc}')
        return None
    return image_to_digest(img_obj)


def start_container(image: str, mock_name: str) -> None:
    """Start an existing container or create a new one from the given image."""
    try:
        cont = CLIENT.containers.get(mock_name)
        print(f'Start existing container: {mock_name}')
        cont.start()
    except docker.errors.NotFound:
        try:
            print(f'Start fresh container: {mock_name}')
            mock_key = get_mock_key(mock_name)
            CLIENT.containers.run(
                image, name=mock_name, tty=True, detach=True,
                environment=ENVS[mock_key] if mock_key in ENVS.keys() else [])
        except docker.errors.APIError as exc:
            print(f'Start container failed: {mock_name}')
            pytest.fail(str(exc))


def exec_extra_commands(mock: str, mock_name: str) -> None:
    """Execute extra commands in the container."""
    container = CLIENT.containers.get(mock_name)
    for extra_cmd in POST_COMMANDS.get(mock, []):
        extra_cmd = extra_cmd.replace('\n', ' ')
        for retry_id in range(4):
            print('exec', retry_id, mock_name, 'cmd', extra_cmd)
            exit_code, output = container.exec_run(extra_cmd)
            print('exec', retry_id, mock_name, 'exit_code', exit_code)
            print('exec', retry_id, mock_name, 'output', output)
            if exit_code == 0:
                break
            time.sleep(15.0)


def create_container(mock: str) -> None:
    """Build mocks caching imgs/containers and building/running when needed."""
    image = f'registry.gitlab.com/fluidattacks/asserts/mocks/{mock}'
    context = f'test/provision/{mock.replace(":", "/")}'

    mock_name = get_mock_name(mock)

    # Get the current image digest in the registry
    img_digest = get_existing_image(image)

    # Build the image to get the current hash in the repository
    # if not changes has been made, then it'll be entirely get from cache
    new_img_digest = build_image(image, context)

    if not new_img_digest:
        # Build failed
        pytest.fail()

    # If the image in the registry is different from the one in the repository
    if not img_digest == new_img_digest:
        # Invalidate the existing container because it comes from an old image
        stop_container(mock_name, remove=True)

    # Start a container, create it if not exists
    start_container(image, mock_name)

    # Run extra commands
    exec_extra_commands(mock, mock_name)


def open_ports(mock: str, port_mapping) -> None:
    """Open the TCP ports needed for a container."""
    ip = get_container_ip(CLIENT.containers.get(get_mock_name(mock)))
    for value in port_mapping.values():
        wait.tcp.open(value, ip, timeout=30)


def stop_container(mock_name: str, remove: bool = False) -> None:
    """Stop a container removing it optionally."""
    try:
        cont = CLIENT.containers.get(mock_name)
    except docker.errors.NotFound:
        print(f'Container not found: {mock_name}')
    else:
        print(f'Stop container: {mock_name}')
        cont.stop(timeout=0)
        if remove:
            print(f'Remove container: {mock_name}')
            cont.remove(force=True)


@pytest.fixture(scope='session', autouse=True)
def mock_sip(request):
    """Start SIP mock endpoints."""
    prcs = Process(target=sip.start, name='MockSIPServer')
    prcs.daemon = True
    prcs.start()
    time.sleep(1)


@pytest.fixture(scope='session', autouse=True)
def mock_http(request):
    """Start HTTP mocks."""
    prcs = Process(target=httpserver.start, name='MockHTTPServer')
    prcs.daemon = True
    prcs.start()
    time.sleep(1)


@pytest.fixture(scope='session', autouse=True)
def mock_camera_weak(request):
    """Start camera mocks."""
    prcs = Process(target=camera_weak.start, name='MockCameraWeakServer')
    prcs.daemon = True
    prcs.start()
    time.sleep(1)


@pytest.fixture(scope='session', autouse=True)
def mock_camera_hard(request):
    """Start camera mocks."""
    prcs = Process(target=camera_hard.start, name='MockCameraHardServer')
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


@pytest.fixture(scope='session', autouse=True)
def clone_test_repositories(request):
    """Clone a test repository."""
    repos = {
        'test/times/rxjava': {
            'url': 'https://github.com/ReactiveX/RxJava.git',
            'rev': '9a36930bff81770c98b5babe58621fd8e49dba2d',
        }
    }
    for name, params in repos.items():
        if not os.path.exists(name):
            repo = Repo.clone_from(params['url'], name)
            repo.head.reference = repo.create_head('__testing', params['rev'])


@pytest.fixture()
def run_mocks(request):
    """Run mock with given parameters."""
    with Pool(processes=cpu_count()) as workers:
        for mocks in MOCKS:
            workers.map(create_container, tuple(mocks.keys()), 1)
            workers.starmap(open_ports, tuple(mocks.items()), 1)


@pytest.fixture()
def stop_mocks(request):
    """Stop mocks mock with given parameters."""
    with Pool(processes=cpu_count()) as workers:
        for mocks in MOCKS:
            mock_names: tuple = tuple(map(get_mock_name, mocks.keys()))
            workers.map(stop_container, mock_names, 1)


@pytest.fixture(scope='function')
def get_mock_ip(request):
    """Run mock with given parameters."""
    mock = request.param
    con = CLIENT.containers.get(get_mock_name(mock))
    if con.status != 'running':
        con.start()
    yield get_container_ip(con)
