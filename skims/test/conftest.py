from collections.abc import (
    Generator,
    Iterator,
)
import contextlib
from ctx import (
    NAMESPACES_FOLDER,
)
import datetime
from git.repo import (
    Repo,
)
from glob import (
    iglob,
)
from itertools import (
    chain,
)
import json
import os
from parse_cfn.loader import (
    load_as_yaml_without_line_number,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from shutil import (
    copyfile,
    rmtree,
)
import subprocess  # nosec
from test_helpers import (
    create_test_context,
)
from typing import (
    Any,
)

# Side effects
os.chdir("..")
create_test_context(debug=False)


def load_test_groups() -> set[str]:
    with open("skims/test/test_groups.json", encoding="utf-8") as file:
        return json.load(file)


# Constants
TEST_GROUPS: set[str] = set(load_test_groups())


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--skims-test-group",
        action="store",
        metavar="SKIMS_TEST_GROUP",
    )


def pytest_runtest_setup(item: Any) -> None:
    # We pass this command line option to tell what group do we want to run
    # This split the big test suite in components
    skims_test_group = item.config.getoption("--skims-test-group")

    # Validate that the dev specified a group that is run on the CI
    if not skims_test_group:
        raise ValueError("skims-test-group not specified")
    if skims_test_group != "all" and skims_test_group not in TEST_GROUPS:
        raise ValueError(
            f"skims-test-group must be one of: {TEST_GROUPS}, or all",
        )

    # The test expects to run on one of these groups
    # If the dev forgets to specify it while writing the test it'll run
    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name="skims_test_group")
    }

    # Validate that the dev specified a group that is run on the CI
    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f"skims-test-group must be one of: {TEST_GROUPS}")

    # Small logic to skip tests that should not run
    if runnable_groups:
        if skims_test_group == "all" or skims_test_group in runnable_groups:
            # Test should execute
            pass
        else:
            pytest.skip(f"Requires skims test group in: {runnable_groups}")


@pytest.fixture(autouse=True, scope="session")
def test_group() -> Iterator[str]:
    yield "jessup"


@pytest.fixture(autouse=True, scope="session")
def test_prepare_cfn_json_data() -> Generator:
    for path in chain(
        iglob("skims/test/data/lib_path/**/*.yaml", recursive=True),
        iglob("skims/test/data/parse_cfn/**/*.yaml", recursive=True),
    ):
        # Take the yaml and dump it as json as is
        with open(path, encoding="utf-8") as source, open(
            path + ".json", "w", encoding="utf-8"
        ) as target:
            source_data = load_as_yaml_without_line_number(source.read())
            target.write(json.dumps(source_data, indent=2))

    yield

    for path in chain(
        iglob("skims/test/data/lib_path/**/*.yaml.json", recursive=True),
        iglob("skims/test/data/parse_cfn/**/*.yaml.json", recursive=True),
    ):
        os.remove(path)


def _exec_and_wait_command(cmd: list[str]) -> int:
    exit_code: int = -1
    with subprocess.Popen(cmd) as process:
        exit_code = process.wait()
    return exit_code


@contextlib.contextmanager
def _exec_command(cmd: list[str], signal: str = "15") -> Iterator[None]:
    with subprocess.Popen(cmd, start_new_session=True) as sproc:
        try:
            yield
        finally:
            _exec_and_wait_command(
                ["common-kill-tree", signal, f"{sproc.pid}"]
            )


def _exec_mock_server(
    cmd: list[str], port: str, signal: str = "15", wait_time: str = "5"
) -> Iterator[None]:
    _exec_and_wait_command(["common-kill-port", port])
    with _exec_command(cmd, signal):
        _exec_and_wait_command(["common-wait", wait_time, f"localhost:{port}"])
        yield


@pytest.fixture(autouse=False, scope="session")
def test_mocks_http() -> Iterator[None]:
    yield from _exec_mock_server(
        ["skims-test-mocks-http", "localhost", "48000"], "48000"
    )


@pytest.fixture(autouse=False, scope="session")
def test_mocks_ssl_safe() -> Iterator[None]:
    yield from _exec_mock_server(["skims-test-mocks-ssl-safe"], "4445")


@pytest.fixture(autouse=False, scope="session")
def test_mocks_ssl_unsafe() -> Iterator[None]:
    yield from _exec_mock_server(["skims-test-mocks-ssl-unsafe"], "4446")


@pytest.fixture(scope="function")
def mock_pull_namespace_from_s3(
    mocker: MockerFixture,
    test_group: str,  # pylint: disable=redefined-outer-name
) -> Iterator[None]:
    repo_path = os.path.join(NAMESPACES_FOLDER, test_group, "static_namespace")
    files = {
        f"{repo_path}/back/test/conftest.py",
        f"{repo_path}/back/test/test_utils.py",
        f"{repo_path}/back/test/test_generic.py",
        f"{repo_path}/back/test/controlles/test_user.py",
        f"{repo_path}/back/test/controlles/test_client.py",
        f"{repo_path}/back/test/controlles/test_admin.py",
        f"{repo_path}/back/test/conftest.py",
        f"{repo_path}/back/src/controlles/user.py",
        f"{repo_path}/back/src/controlles/client.py",
        f"{repo_path}/back/src/controlles/admin.py",
        f"{repo_path}/back/src/controlles/admin.py",
        f"{repo_path}/back/src/statics/key.ssh",
        f"{repo_path}/back/src/statics/log.img",
        f"{repo_path}/README.md",
        f"{repo_path}/front/node_modules/colors/index.js",
        f"{repo_path}/front/node_modules/babel/index.js",
        f"{repo_path}/front/index.js",
        f"{repo_path}/front/www.html",
        f"{repo_path}/front/components/user/index.js",
        f"{repo_path}/front/components/user/index.spec.js",
        f"{repo_path}/front/components/admin/index.js",
        f"{repo_path}/front/components/admin/index.spec.js",
    }
    try:
        os.makedirs(repo_path, exist_ok=True)
        repo = Repo.init(repo_path)
        for file in files:
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            with open(file, "w", encoding="utf-8") as handler:
                handler.write(f"# {file.split('/')[-1]}")
            repo.index.add(file)
        repo.index.commit("Initial commit")
        mocker.patch(
            "batch.repositories.pull_namespace_from_s3", return_value=repo_path
        )
        yield
    finally:
        rmtree(repo_path)


@pytest.fixture(scope="function")
def mock_pull_git_repo_initial_commit(
    mocker: MockerFixture,
    test_group: str,  # pylint: disable=redefined-outer-name
) -> Iterator[None]:
    repo_path = os.path.join(
        NAMESPACES_FOLDER, test_group, "dynamic_namespace_1"
    )
    file_path = "skims/test/data/lib_path/f073/cluster_instance_test.tf"
    repo_file_path = os.path.join(repo_path, file_path)

    os.makedirs(repo_path, exist_ok=True)
    repo = Repo.init(repo_path)

    os.makedirs(os.path.split(repo_file_path)[0], exist_ok=True)
    copyfile(file_path, repo_file_path)
    repo.index.add(repo_file_path)

    repo.index.commit(
        message="Initial commit",
        author_date=datetime.date(2020, 7, 21).strftime("%Y-%m-%d %H:%M:%S"),
        commit_date=datetime.date(2020, 7, 21).strftime("%Y-%m-%d %H:%M:%S"),
    )
    mocker.patch(
        "batch.repositories.pull_namespace_from_s3", return_value=repo_path
    )
    yield


@pytest.fixture(scope="function")
def mock_pull_git_repo_next_commit(
    mocker: MockerFixture,
    test_group: str,  # pylint: disable=redefined-outer-name
) -> Iterator[None]:
    repo_path = os.path.join(
        NAMESPACES_FOLDER, test_group, "dynamic_namespace_1"
    )
    repo_file_path = os.path.join(
        repo_path, "skims/test/data/lib_path/f073/cluster_instance_test.tf"
    )
    new_file_path = "skims/test/data/lib_path/f073/cluster_instance_rebase.tf"
    try:
        repo = Repo(repo_path)
        copyfile(new_file_path, repo_file_path)
        repo.index.add(repo_file_path)

        repo.index.commit("Update file")
        mocker.patch(
            "batch.repositories.pull_namespace_from_s3", return_value=repo_path
        )
        yield
    finally:
        rmtree(repo_path)


@pytest.fixture(scope="function")
def mock_pull_git_repo_commits_for_zr(
    mocker: MockerFixture,
    test_group: str,  # pylint: disable=redefined-outer-name
) -> Iterator[None]:
    repo_path = os.path.join(
        NAMESPACES_FOLDER, test_group, "dynamic_namespace_3"
    )

    repo_file_path = os.path.join(
        repo_path, "skims/test/data/lib_path/f109/subnet_test_rebase.tf"
    )

    new_file_path = "skims/test/data/lib_path/f109/subnet_test.tf"
    try:
        os.makedirs(repo_path, exist_ok=True)
        repo = Repo.init(repo_path)

        os.makedirs(os.path.split(repo_file_path)[0], exist_ok=True)

        copyfile(new_file_path, repo_file_path)

        repo.index.add(repo_file_path)
        repo.index.commit(
            message="Initial commit",
            author_date=datetime.date(2020, 7, 21).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            commit_date=datetime.date(2020, 7, 21).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        copyfile(
            "skims/test/data/lib_path/f109/subnet_test_rebase.tf",
            repo_file_path,
        )
        repo.index.add(repo_file_path)
        repo.index.commit(message="Rebase commit")

        mocker.patch(
            "batch.repositories.pull_namespace_from_s3", return_value=repo_path
        )
        yield

    finally:
        rmtree(repo_path)
