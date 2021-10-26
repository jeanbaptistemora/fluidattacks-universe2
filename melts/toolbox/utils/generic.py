import boto3
from botocore.exceptions import (
    ClientError,
)
from click import (
    BadParameter,
)
import configparser
from configparser import (
    ConfigParser,
)
import contextlib
from datetime import (
    datetime,
)
import dateutil.parser  # type: ignore
from functools import (
    lru_cache,
)
import git
import io
import json
import os
import re
import subprocess
import sys
import textwrap
from toolbox.logger import (
    LOGGER,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)

DEFAULT_PROFILE: str = "continuous-unspecified-subs"


def run_command_old(
    cmd: List[str],
    cwd: str,
    env: dict,
) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout and stderr."""
    return run_command(cmd, cwd, env, shell=True)


def run_command(  # pylint: disable=too-many-arguments
    cmd: List[str],
    cwd: str,
    env: Dict[str, Any],
    stdout: Optional[int] = subprocess.PIPE,
    stderr: Optional[int] = subprocess.PIPE,
    universal_newlines: bool = True,
    **kwargs: Any,
) -> Tuple[int, str, str]:
    """Run a command and return exit-code, stdout and stderr."""
    # We are checking the exit code in upstream components
    # pylint: disable=subprocess-run-check
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env={**os.environ.copy(), **env},
        stdout=stdout,
        stderr=stderr,
        universal_newlines=universal_newlines,
        **kwargs,
    )
    return proc.returncode, proc.stdout, proc.stderr


def is_env_ci() -> bool:
    """
    Check if environment is local or CI.
    Return True if CI.
    Return False if local.
    """
    return bool(os.environ.get("CI"))


def is_dev_mode() -> bool:
    """
    Check if developer mode is enable.
    Return True if developer mode is enable.
    Return False if developer mode is disable.
    """
    return bool(os.environ.get("DEV_MODE"))


def is_branch_master() -> bool:
    """
    Check if branch is master or dev.
    Return True if branch is master.
    Return False if branch is dev.
    """
    return os.environ.get("CI_COMMIT_REF_NAME") == "master"


def is_credential_valid(
    aws_access_key_id: bool,
    aws_secret_access_key: bool,
    aws_session_token: bool,
) -> bool:
    try:
        client = boto3.client(
            "sts",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )
        client.get_caller_identity()
    except ClientError:
        return False
    return True


def is_inside_services() -> bool:
    starting_dir: str = os.getcwd()
    if "services" not in starting_dir:
        return False
    return True


def go_back_to_services() -> None:
    if is_inside_services():
        while not os.getcwd().endswith("services"):
            os.chdir("..")
            LOGGER.debug("Adjusted working dir to: %s", os.getcwd())


def get_current_group() -> str:
    actual_path: str = os.getcwd()
    try:
        return actual_path.split("/services/")[1].split("/")[1]
    except IndexError:
        return "unspecified-subs"


def is_valid_group(  # pylint: disable=unused-argument
    ctx: Any,
    param: Any,
    subs: str,
) -> str:
    actual_path: str = os.getcwd()

    if (
        "groups" not in actual_path
        and os.path.exists("groups")
        and subs not in os.listdir("groups")
        and subs not in ("admin", "all", "unspecified-subs")
    ):
        msg = f"the group {subs} does not exist"
        raise BadParameter(msg)
    go_back_to_services()
    return subs


@contextlib.contextmanager
def output_block(*, indent: int = 2) -> Iterator[None]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(
        buffer
    ):
        yield
    print(textwrap.indent(buffer.getvalue(), " " * indent))


def guess_date_from_str(
    date_str: str,
    default: str = "2000-01-01T00:00:00Z",
) -> str:
    """Use heuristics to transform any-format string into an RFC 3339 date."""
    try:
        date_obj = dateutil.parser.parse(date_str)
    except (ValueError, OverflowError):
        return default
    else:
        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


def rfc3339_str_to_date_obj(
    date_str: str,
) -> datetime:
    """Parse an RFT3339 formatted string into a datetime object."""
    return dateutil.parser.parse(date_str)


def get_change_request_summary(
    ref: str = "HEAD",
    path: str = os.getcwd(),
) -> str:
    """Return the commit message, or the merge request title."""
    commit_summary: str
    gitlab_summary_var: str = "CI_MERGE_REQUEST_TITLE"

    if gitlab_summary_var in os.environ:
        commit_summary = os.environ[gitlab_summary_var]
    else:
        commit_summary = (
            git.Repo(path, search_parent_directories=True).commit(ref).summary
        )

    return commit_summary


def get_change_request_body(ref: str = "HEAD", path: str = os.getcwd()) -> str:
    """Return the HEAD commit message, or the merge request body."""
    gitlab_summary_var: str = "CI_MERGE_REQUEST_DESCRIPTION"

    if gitlab_summary_var in os.environ:
        return os.environ[gitlab_summary_var]
    with contextlib.suppress(IndexError):
        return (
            git.Repo(path, search_parent_directories=True)
            .commit(ref)
            .message.split("\n\n", 1)[1]
        )
    return ""


def get_change_request_patch(
    ref: str = "HEAD",
    path: str = os.getcwd(),
) -> str:
    """Return the HEAD commit patch."""
    return git.Repo(path, search_parent_directories=True).git.show(
        "--format=", ref
    )


def get_change_request_hunks(ref: str = "HEAD") -> List[str]:
    """Return the HEAD commit patch."""
    hunks: List[str] = []

    for line in get_change_request_patch(ref).splitlines():
        if line.startswith("diff"):
            hunks.append(str())

        hunks[-1] += line + "\n"

    return hunks


def get_change_request_deltas(ref: str = "HEAD") -> int:
    """Return the HEAD commit deltas."""
    insertions: int = 0
    deletions: int = 0

    for hunk in get_change_request_hunks(ref):
        hunk_lines: List[str] = hunk.splitlines()
        hunk_diff_lines: List[str] = hunk_lines[4:]

        for hunk_diff_line in hunk_diff_lines:
            insertions += hunk_diff_line.startswith("+")
            deletions += hunk_diff_line.startswith("-")

    return insertions + deletions


def get_change_request_touched_files(
    ref: str = "HEAD",
    path: str = os.getcwd(),
) -> Tuple[str, ...]:
    """Return touched files in HEAD commit."""
    return tuple(
        git.Repo(path, search_parent_directories=True)
        .git.show("--format=", "--name-only", ref)
        .splitlines()
    )


def get_change_request_touched_and_existing_exploits(
    ref: str = "HEAD",
) -> Tuple[str, ...]:
    """Return a tuple of paths to exploits in the last commit."""
    changed_files = get_change_request_touched_and_existing_files(ref)
    changed_exploits = tuple(
        file for file in changed_files if "/exploits/" in file
    )
    return changed_exploits


def get_change_request_touched_and_existing_files(
    ref: str = "HEAD",
) -> Tuple[str, ...]:
    """Return touched files in HEAD commit."""
    return tuple(
        os.path.abspath(path)
        for path in get_change_request_touched_files(ref)
        if os.path.exists(path)
    )


def _write_aws_credentials(
    profile: str, key_info: Dict[str, str], delete_default: bool = False
) -> None:
    """
    Add profile credentials in aws credential file.

    :param profile: Profile name.
    :param key_info: AWS credentials for profile.
    :param delete_default: Delete default credentials.
    """
    creds_file: str = os.path.expanduser("~/.aws/credentials")
    if not os.path.exists(creds_file):
        with contextlib.suppress(FileExistsError):
            os.mkdir(os.path.expanduser("~/.aws/"))
        with open(creds_file, "w", encoding="utf8") as read_file:
            read_file.close()
    config: ConfigParser = ConfigParser()
    config.read(creds_file)
    if not config.has_section(profile):
        config.add_section(profile)
    if delete_default and config.has_section(DEFAULT_PROFILE):
        del config[DEFAULT_PROFILE]
    config[profile]["aws_access_key_id"] = key_info["AccessKeyId"]
    config[profile]["aws_secret_access_key"] = key_info["SecretAccessKey"]
    config[profile]["aws_session_token"] = key_info["SessionToken"]
    config[profile]["aws_session_token_expiration"] = key_info["Expiration"]

    with open(creds_file, "w", encoding="utf8") as file:
        config.write(file)


def _get_aws_credentials(profile: str) -> Dict:
    """
    Returns aws credentials of the profile by reading the aws credentials file.
    """
    creds_file: str = os.path.expanduser("~/.aws/credentials")
    config: ConfigParser = ConfigParser()
    config.read(creds_file)
    if not config.has_section(profile):
        creds: Dict = {}
    else:
        profile_data = config[profile]
        if profile_data.get("aws_session_token_expiration", None):
            creds = {
                "AccessKeyId": profile_data["aws_access_key_id"],
                "SecretAccessKey": profile_data["aws_secret_access_key"],
                "SessionToken": profile_data["aws_session_token"],
                "Expiration": profile_data["aws_session_token_expiration"],
            }
        else:
            creds = {}

    return creds


def _get_okta_user() -> Optional[str]:
    """Returns the okta user."""
    user: Optional[str] = os.environ.get("AWS_OKTA_USER")
    if not user:
        LOGGER.info("Set the variable AWS_OKTA_USER in your shell profile")
        try:
            path: str = os.path.expanduser("~/.aws-okta-processor/cache/")
            users: List[str] = os.listdir(path)
            if users:
                with open(path + users[0], "r", encoding="utf8") as reader:
                    session: Dict = json.load(reader)
                    user = session["login"]
                    LOGGER.info("Using %s", user)
            else:
                user = input("Username: ")
        except FileNotFoundError as exc:
            LOGGER.exception(exc)
            user = input("Username: ")

    return user


def _set_aws_env_creds(profile: str) -> None:
    """
    Set aws credentials as environment variables.

    :param profile: Profile name credentials are extracted.
    """
    credentials = boto3.Session(profile_name=profile).get_credentials()
    os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
    os.environ["AWS_SESSION_TOKEN"] = credentials.token


def _get_okta_aws_credentials(profile: str) -> Dict:
    """Login in okta to get the aws credentials of the profile."""
    creds_file: str = os.path.expanduser("~/.aws/credentials")
    config: ConfigParser = ConfigParser()
    config.read(creds_file)
    url: str = "fluidattacks.okta.com"
    applink: str = f"https://{url}/home/amazon_aws/0oa9ahz3rfx1SpStS357/272"
    envs: Dict = {
        "AWS_OKTA_APPLICATION": applink,
        "AWS_OKTA_ORGANIZATION": "fluidattacks.okta.com",
        "AWS_OKTA_USER": _get_okta_user(),
        "AWS_OKTA_DURATION": "32400",
    }
    if profile != DEFAULT_PROFILE:
        envs["AWS_OKTA_ROLE"] = f"arn:aws:iam::205810638802:role/{profile}"
    command: List[str] = [
        "aws-okta-processor",
        "authenticate",
        "--no-aws-cache",
        "--silent",
    ]
    success: int
    out: str
    error: str
    success, out, error = run_command(command, cwd=".", env=envs)
    if success > 0:
        LOGGER.error(error)
        if config.has_section("continuous-admin"):
            LOGGER.info("Using the continuous-admin credentials")
            envs[
                "AWS_OKTA_ROLE"
            ] = "arn:aws:iam::205810638802:role/continuous-admin"
            key_info = _get_aws_credentials("continuous-admin")
            out = json.dumps(key_info)
            is_aws_valid = is_credential_valid(
                key_info["AccessKeyId"],
                key_info["SecretAccessKey"],
                key_info["SessionToken"],
            )
            if not is_aws_valid:
                success, out, error = run_command(command, cwd=".", env=envs)
        else:
            envs.pop("AWS_OKTA_ROLE")
            success, out, error = run_command(command, cwd=".", env=envs)
    return json.loads(out)


def okta_aws_login(profile: str = "default") -> bool:
    """
    Login to AWS through OKTA using a specific profile.
    """
    LOGGER.info("Logging in to Okta.")

    success: int = 0
    expired: bool = False
    is_aws_account_valid: bool = False
    key_info: Dict = _get_aws_credentials(profile)

    if key_info:
        now: datetime = datetime.utcnow()
        expire: datetime = datetime.strptime(
            key_info["Expiration"], "%Y-%m-%dT%H:%M:%SZ"
        )
        expired = now > expire

        is_aws_account_valid = is_credential_valid(
            key_info["AccessKeyId"],
            key_info["SecretAccessKey"],
            key_info["SessionToken"],
        )

    if not key_info or expired or not is_aws_account_valid:
        key_info = _get_okta_aws_credentials(profile)

    _write_aws_credentials(profile, key_info)
    if profile == DEFAULT_PROFILE:
        client = boto3.client("sts")
        profile = client.get_caller_identity()["Arn"].split("/")[1]
        _write_aws_credentials(profile, key_info, delete_default=True)
    _set_aws_env_creds(profile)

    return success == 0


def aws_login(profile: str = "default") -> None:
    """
    Login as either:
    1. AWS Prod if branch is master in CI
    2. AWS Dev if branch is dev in CI
    3. Okta AWS if local integration
    """
    if is_env_ci():
        if is_branch_master():
            os.environ["AWS_ACCESS_KEY_ID"] = os.environ[
                "PROD_AWS_ACCESS_KEY_ID"
            ]
            os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ[
                "PROD_AWS_SECRET_ACCESS_KEY"
            ]
        else:
            os.environ["AWS_ACCESS_KEY_ID"] = os.environ[
                "DEV_AWS_ACCESS_KEY_ID"
            ]
            os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ[
                "DEV_AWS_SECRET_ACCESS_KEY"
            ]

        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]

        credentials = configparser.ConfigParser()
        credentials_dir = os.path.expanduser("~/.aws")
        credentials_path = f"{credentials_dir}/credentials"
        credentials.read(credentials_path)
        credentials.setdefault("default", {})
        credentials["default"]["aws_access_key_id"] = aws_access_key_id
        credentials["default"]["aws_secret_access_key"] = aws_secret_access_key
        os.makedirs(credentials_dir, exist_ok=True)
        with open(credentials_path, "w", encoding="utf8") as handler:
            credentials.write(handler)

    else:
        okta_aws_login(profile)


@lru_cache(maxsize=None, typed=True)
def get_sops_secret(var: str, path: str, profile: str = "default") -> str:
    """
    Get a key from a sops file.
    """
    if is_env_ci():
        profile = "default"
    cmd = [
        "sops",
        "--aws-profile",
        profile,
        "--decrypt",
        "--extract",
        f'["{var}"]',
        path,
    ]
    code, stdout, stderr = run_command(cmd=cmd, cwd=".", env={})
    if code:
        LOGGER.error("while calling sops:")
        LOGGER.error("  stdout:")
        LOGGER.error(textwrap.indent(stdout, "    "))
        LOGGER.error("  stderr:")
        LOGGER.error(textwrap.indent(stderr, "    "))
        sys.exit(78)
    return stdout


@lru_cache(maxsize=None, typed=True)
def does_subs_exist(subs: str) -> bool:
    """Return True if the group exists."""
    return os.path.isdir(f"groups/{subs}")


def does_fusion_exist(subs: str) -> bool:
    """Return True if fusion folder present in group"""
    return os.path.isdir(f"groups/{subs}/fusion")


def glob_re(pattern: str, paths: str = ".") -> Iterator[str]:
    """Return the file paths that are regex compliant."""
    for dirpath, _, filenames in os.walk(paths):
        for path in filenames:
            file_path = os.path.join(dirpath, path)
            if re.match(pattern, file_path):
                yield file_path
