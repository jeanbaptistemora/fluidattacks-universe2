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
from test.mock import sip_server
from test.mock import http_server
from test.mock import graphql_server
from test.mock import camera_hard
from test.mock import camera_weak

# Constants
CLIENT = docker.from_env()


FLASK_MOCKS = [
    (sip_server.start, 'MockSIPServer', ['iot']),
    (http_server.start, 'MockHTTPServer', [
        'format',
        'ot',
        'proto_http',
        'proto_rest',
    ]),
    (graphql_server.start, 'MockGraphQLServer', ['proto_graphql']),
    (camera_weak.start, 'MockCameraWeakServer', ['iot']),
    (camera_hard.start, 'MockCameraHardServer', ['iot']),
]


MOCKS = [
    # These need to be built first
    {
        'dns:weak': {
            'expose': {'53/tcp': 53, '53/udp': 53},
            'asserts_modules': ['proto_dns']
        },
        'ftp:weak': {
            'expose': {'21/tcp': 21},
            'asserts_modules': ['proto_ftp']
        },
        'mysql_db:weak': {
            'expose': {'3306/tcp': 3306},
            'asserts_modules': ['db_mysql', 'syst']
        },
        'mysql_os:hard': {
            'expose': {'22/tcp': 22},
            'asserts_modules': ['db_mysql', 'syst']
        },
        'smb:weak': {
            'expose': {'139/tcp': 139},
            'asserts_modules': ['proto_smb']
        },
        'smtp:weak': {
            'expose': {'25/tcp': 25},
            'asserts_modules': ['proto_smtp']
        },
    },
    # Some of these are built in top of the previous ones
    {
        'bwapp': {
            'expose': {'80/tcp': 80},
            'asserts_modules': ['helper', 'proto_http']
        },
        'dns:hard': {
            'expose': {'53/tcp': 53, '53/udp': 53},
            'asserts_modules': ['proto_dns']
        },
        'ftp:hard': {
            'expose': {'21/tcp': 21},
            'asserts_modules': ['proto_ftp']
        },
        'ldap:hard': {
            'expose': {'389/tcp': 389},
            'asserts_modules': ['proto_ldap']
        },
        'ldap:weak': {
            'expose': {'389/tcp': 389},
            'asserts_modules': ['proto_ldap']
        },
        'mysql_db:hard': {
            'expose': {'3306/tcp': 3306},
            'asserts_modules': ['db_mysql']
        },
        'mysql_os:weak': {
            'expose': {'22/tcp': 22},
            'asserts_modules': ['syst']
        },
        'mssql:weak': {
            'expose': {'1432/tcp': 1432},
            'asserts_modules': ['db_mssql']
        },
        'mssql:hard': {
            'expose': {'1433/tcp': 1433},
            'asserts_modules': ['db_mssql']
        },
        'os:hard': {
            'expose': {'22/tcp': 22},
            'asserts_modules': ['proto_ssh', 'syst']
        },
        'os:weak': {
            'expose': {'22/tcp': 22},
            'asserts_modules': ['proto_ssh', 'syst']
        },
        'postgresql:hard': {
            'expose': {'5432/tcp': 5432},
            'asserts_modules': ['db_postgres']
        },
        'postgresql:weak': {
            'expose': {'5432/tcp': 5432},
            'asserts_modules': ['db_postgres']
        },
        'smb:hard': {
            'expose': {'139/tcp': 139},
            'asserts_modules': ['proto_smb']
        },
        'smtp:hard': {
            'expose': {'25/tcp': 25},
            'asserts_modules': ['proto_smtp']
        },
        'ssl:hard': {
            'expose': {'443/tcp': 443},
            'asserts_modules': ['format', 'proto_ssl']
        },
        'ssl:hard_tlsv13': {
            'expose': {'443/tcp': 443},
            'asserts_modules': ['proto_ssl']
        },
        'ssl:weak': {
            'expose': {'443/tcp': 443},
            'asserts_modules': ['format', 'proto_ssl']
        },
        'tcp:hard': {
            'expose': {'443/tcp': 443},
            'asserts_modules': ['proto_tcp']
        },
        'tcp:weak': {
            'expose': {'80/tcp': 80},
            'asserts_modules': ['proto_tcp']
        },
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

}


def pytest_addoption(parser):
    """Add an option to the CLI of pytest to indicate what tests to run."""
    parser.addoption(
        '--asserts-module',
        action='store',
        metavar='ASSERTS_MODULE',
        help='only run tests matching for the provided Asserts Module',
    )


def pytest_runtest_setup(item):
    """Skip the tests that are not part of the --asserts-module option."""
    modules = \
        [mark.args[0] for mark in item.iter_markers(name='asserts_module')]
    if modules:
        if item.config.getoption('--asserts-module', default='all') != 'all':
            if item.config.getoption('--asserts-module') not in modules:
                pytest.skip(
                    f'Test requires pytest --asserts-module in {modules}')


def should_run_mock(current_module: str, modules_where_should_run) -> bool:
    """Return True if given the context module this mock should be started."""
    if current_module == 'all':
        return True
    return current_module in modules_where_should_run


def get_mock_name(mock: str) -> str:
    """Get mock name."""
    branch = os.environ.get('CI_COMMIT_REF_NAME', 'test')
    mock_name = f'{mock.replace(":", "_")}_{branch}'
    return mock_name


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
            CLIENT.containers.run(image, name=mock_name, tty=True, detach=True)
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


def open_ports(mock: str, config) -> None:
    """Open the TCP ports needed for a container."""
    ip = get_container_ip(CLIENT.containers.get(get_mock_name(mock)))
    for port_mapping in config['expose'].values():
        wait.tcp.open(port_mapping, ip, timeout=30)


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
def flask_mocks(request):
    """Start mocks based on the Flask Framework."""
    asserts_module = \
        request.config.getoption('--asserts-module', default='all')
    processes = []
    for target, name, modules_where_should_run in FLASK_MOCKS:
        if should_run_mock(current_module=asserts_module,
                           modules_where_should_run=modules_where_should_run):
            process = Process(target=target, name=name)
            process.daemon = True
            process.start()
            processes.append(process)
    time.sleep(10.0)


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
    asserts_module = \
        request.config.getoption('--asserts-module', default='all')
    with Pool(processes=cpu_count()) as workers:
        for mocks in MOCKS:
            mocks = {
                mock: config
                for mock, config in mocks.items()
                if should_run_mock(
                    current_module=asserts_module,
                    modules_where_should_run=config['asserts_modules'])
            }
            workers.map(create_container, tuple(mocks.keys()), 1)
            workers.starmap(open_ports, tuple(mocks.items()), 1)


@pytest.fixture()
def stop_mocks(request):
    """Stop mocks mock with given parameters."""
    asserts_module = \
        request.config.getoption('--asserts-module', default='all')
    with Pool(processes=cpu_count()) as workers:
        for mocks in MOCKS:
            mocks = {
                mock: config
                for mock, config in mocks.items()
                if should_run_mock(
                    current_module=asserts_module,
                    modules_where_should_run=config['asserts_modules'])
            }
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
