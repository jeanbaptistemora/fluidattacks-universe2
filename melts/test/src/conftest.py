# pylint: disable=unused-argument

import boto3
from click.testing import (
    CliRunner,
    Result,
)
import contextlib
import os
import pytest
from toolbox.cli import (
    melts as cli,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils import (
    generic,
)
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
)

# Constants
SUBS: str = "continuoustest"


@contextlib.contextmanager
def _relocate(path: str = "../") -> Iterator[str]:
    """Change temporarily the working directory."""
    # The toolbox need to be run in the root of the repository
    current_dir: str = os.getcwd()
    try:
        os.chdir(path)
        LOGGER.info("yield, %s", os.getcwd())
        yield os.getcwd()
    finally:
        # Return to where we were
        LOGGER.info("finally, %s", current_dir)
        os.chdir(current_dir)


@pytest.fixture(scope="function")
def relocate(request: Any) -> Iterable[str]:
    """Change temporarily the working directory."""
    with _relocate() as new_path:
        yield new_path


@pytest.fixture(scope="function")
def relocate_to_cloned_repo(request: Any) -> Iterable[str]:
    """Change temporarily the working directory."""
    with _relocate(path=f"../groups/{SUBS}/fusion/services") as new_path:
        yield new_path


@pytest.fixture(scope="function")
def prepare_s3_continuous_repositories(request: Any) -> None:
    """Create empty continuous-repositories s3 bucket"""
    localstack_endpoint: str = (
        "localstack" if generic.is_env_ci() else "localhost"
    )
    # FP: the endpoint is hosted in a local environment
    endpoint_url: str = f"http://{localstack_endpoint}:4566"  # NOSONAR
    bucket_name: str = "continuous-repositories"
    s3_client = boto3.client("s3", endpoint_url=endpoint_url)
    s3_client.create_bucket(Bucket=bucket_name)


@pytest.fixture(scope="session", autouse=True)
def cli_runner(  # pylint: disable=unused-argument
    request: Any,
) -> Callable[..., Result]:
    def executor(command: List[str]) -> Result:
        runner = CliRunner()
        return runner.invoke(cli, command)

    return executor
