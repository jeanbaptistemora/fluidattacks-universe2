import aiohttp
from aiohttp.client_exceptions import (
    ClientOSError,
    ServerDisconnectedError,
)
import asyncio
from asyncio import (
    run,
)
import base64
import boto3
from contextlib import (
    asynccontextmanager,
    suppress,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
import json
import logging
import os
from retry import (  # type: ignore
    retry,
)
import shutil
import sys
import tarfile
import tempfile
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)
from urllib3.util.url import (
    parse_url,
    Url,
)
from urllib.parse import (
    quote_plus,
    urlparse,
)
import uuid


class CredentialsNotFound(Exception):
    pass


class BatchProcessing(NamedTuple):
    key: str
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str
    queue: str


def get_action(
    *,
    action_dynamo_pk: str,
) -> Optional[BatchProcessing]:
    client = boto3.client("dynamodb", "us-east-1")
    query_payload = {
        "TableName": "fi_async_processing",
        "KeyConditionExpression": "#69240 = :69240",
        "ExpressionAttributeNames": {"#69240": "pk"},
        "ExpressionAttributeValues": {":69240": {"S": action_dynamo_pk}},
    }
    response_items = client.query(**query_payload)
    if not response_items or not response_items["Items"]:
        return None

    item = response_items["Items"][0]
    return BatchProcessing(
        key=item["pk"]["S"],
        action_name=item["action_name"]["S"].lower(),
        entity=item["entity"]["S"].lower(),
        subject=item["subject"]["S"].lower(),
        time=item["time"]["S"],
        additional_info=item.get("additional_info", {}).get("S"),
        queue=item["queue"]["S"],
    )


def delete_action(
    *,
    action_dynamo_pk: str,
) -> None:
    client = boto3.client("dynamodb", "us-east-1")
    operation_payload = {
        "TableName": "fi_async_processing",
        "Key": {"pk": {"S": action_dynamo_pk}},
    }
    client.delete_item(**operation_payload)


@retry(
    (
        TypeError,
        ClientOSError,
        asyncio.exceptions.TimeoutError,
        ServerDisconnectedError,
    ),
    tries=5,
    delay=2,
)
async def _request_asm(
    payload: Dict[str, Any],
    token: str,
) -> Optional[Dict[str, Any]]:
    result: Optional[Dict[str, Any]] = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "https://app.fluidattacks.com/api", data=json.dumps(payload)
        ) as response:
            if response.status == 200:
                parsed_response = await response.json()
                if "errors" not in parsed_response:
                    result = parsed_response

    return result


async def get_roots(
    token: str, group_name: str
) -> Optional[List[Dict[str, Any]]]:
    result: Optional[List[Dict[str, Any]]] = None
    query = """
        query GetRoots($groupName: String!) {
            group(groupName: $groupName) {
              roots {
                ... on GitRoot {
                  id
                  nickname
                  branch
                  url
                  credentials {
                    id
                    user
                    oauthType
                    password
                    token
                    type
                    key
                  }
                  state
                }
              }
            }
        }
    """
    payload = {"query": query, "variables": {"groupName": group_name}}

    response = await _request_asm(payload=payload, token=token)
    if response is not None:
        result = response["data"]["group"]["roots"]
    else:
        logging.error("Failed to fetch root info for group %s", group_name)

    return result


@retry((TypeError,), tries=3, delay=1)
async def update_root_cloning_status(  # pylint: disable=too-many-arguments
    token: str,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
    commit: Optional[str] = None,
) -> bool:
    result: bool = False
    query = """
        mutation UpdateRootCloningStatus(
          $groupName: String!
          $rootId: ID!
          $status: CloningStatus!
          $message: String!
          $commit: String
          $queueMachine: Boolean
        ) {
          updateRootCloningStatus(
            groupName: $groupName
            id: $rootId
            status: $status
            message: $message
            commit: $commit
            queueMachine: $queueMachine
          ) {
            success
          }
        }
    """
    payload = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "rootId": root_id,
            "status": status,
            "message": message,
            "commit": commit,
            "queueMachine": False,
        },
    }

    response = await _request_asm(payload=payload, token=token)
    if response is not None:
        result = response["data"]["updateRootCloningStatus"]["success"]
    else:
        logging.error(
            "Failed to update status for root %s in group %s",
            root_id,
            group_name,
        )

    return result


async def submit_group_machine_execution(
    group_name: str,
    root_nicknames: List[str],
    token: str,
) -> bool:
    result: bool = False
    query = """
        mutation ExecuteMachinePostClone(
          $groupName: String!
          $rootNicknames: [String!]!
        ) {
          submitGroupMachineExecution(
            groupName: $groupName
            rootNicknames: $rootNicknames
          ) {
            success
          }
        }
    """
    payload = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "rootNicknames": root_nicknames,
        },
    }

    response = await _request_asm(payload=payload, token=token)
    if response is not None:
        result = response["data"]["submitGroupMachineExecution"]["success"]
    else:
        logging.error(
            "Failed to submit Machine execution for group %s", group_name
        )

    return result


def _format_token(
    parsed_url: Url,
    token: str,
    is_oauth: bool,
    provider: str,
) -> str:
    url = str(parsed_url._replace(auth=token))
    if is_oauth:
        url = str(parsed_url._replace(auth=f"oauth2:{token}"))
        if provider == "BITBUCKET":
            url = str(parsed_url._replace(auth=f"x-token-auth:{token}"))

    return url


def _format_https_url(
    *,
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    is_oauth: bool = False,
    provider: str = "",
) -> str:
    user = quote_plus(user) if user is not None else user
    password = quote_plus(password) if password is not None else password
    parsed_url = parse_url(repo_url)
    if token is not None:
        url = _format_token(parsed_url, token, is_oauth, provider)
    elif user is not None and password is not None:
        url = str(parsed_url._replace(auth=f"{user}:{password}"))

    return url


async def ssh_clone(
    *, branch: str, credential_key: str, repo_url: str, temp_dir: str
) -> Tuple[Optional[str], Optional[str]]:
    raw_root_url = repo_url
    if "source.developers.google" not in raw_root_url:
        raw_root_url = repo_url.replace(f"{urlparse(repo_url).scheme}://", "")
    ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
    with open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        ssh_file.write(base64.b64decode(credential_key).decode())

    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "clone",
        "--branch",
        branch,
        raw_root_url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={
            **os.environ.copy(),
            "GIT_SSH_COMMAND": (
                f"ssh -i {ssh_file_name}"
                " -o UserKnownHostsFile=/dev/null"
                " -o StrictHostKeyChecking=no"
                " -o IdentitiesOnly=yes"
                " -o HostkeyAlgorithms=+ssh-rsa"
                " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
            ),
        },
    )
    _, stderr = await proc.communicate()

    os.remove(ssh_file_name)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    logging.error("Repo cloning failed: %s", stderr.decode())

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: Optional[str] = None,
    token: Optional[str] = None,
    user: Optional[str] = None,
    is_oauth: bool = False,
    provider: str = "",
) -> Tuple[Optional[str], Optional[str]]:
    url = _format_https_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        is_oauth=is_oauth,
        provider=provider,
    )
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        "clone",
        "--branch",
        branch,
        url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    logging.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: Optional[str] = None
) -> bool:
    git_dir = os.path.normpath(f"{repo_path}/.git")
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if os.path.exists(git_dir):
            tar_handler.add(
                git_dir, arcname=f"{root_nickname}/.git", recursive=True
            )
            return True
        return False


@retry(ConnectionError, tries=5, delay=2)
async def upload_cloned_repo_to_s3_tar(
    *, repo_path: str, group_name: str, nickname: str
) -> bool:
    _, zip_output_path = tempfile.mkstemp()
    if not create_git_root_tar_file(nickname, repo_path, zip_output_path):
        logging.error(
            "Failed to compress root %s",
            nickname,
        )
        os.remove(zip_output_path)
        return False
    cliente_s3 = boto3.client("s3")
    cliente_s3.upload_file(
        zip_output_path,
        "integrates",
        f"continuous-repositories/{group_name}/{nickname}.tar.gz",
    )
    return True


@asynccontextmanager
async def clone_root(
    *, group_name: str, root: Dict[str, Any], api_token: str
) -> Any:
    cred = root["credentials"]
    branch = root["branch"]
    root_url = root["url"]
    root_nickname = root["nickname"]
    with tempfile.TemporaryDirectory() as temp_dir:
        if key := cred.get("key"):
            folder_to_clone_root, stderr = await ssh_clone(
                branch=branch,
                credential_key=key,
                repo_url=root_url,
                temp_dir=temp_dir,
            )
        elif token := cred.get("token"):
            folder_to_clone_root, stderr = await https_clone(
                branch=branch,
                password=None,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=token,
                user=None,
                is_oauth=cred.get("type", "") == "OAUTH",
                provider=cred.get("oauthType", ""),
            )
        elif (user := cred.get("user")) and (password := cred.get("password")):
            folder_to_clone_root, stderr = await https_clone(
                branch=branch,
                password=password,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=None,
                user=user,
            )
        else:
            await update_root_cloning_status(
                token=api_token,
                group_name=group_name,
                root_id=root["id"],
                status="FAILED",
                message="Credentials not found",
            )
            return

        if folder_to_clone_root is None:
            logging.error("Failed to clone %s: %s", root_nickname, stderr)
            await update_root_cloning_status(
                token=api_token,
                group_name=group_name,
                root_id=root["id"],
                status="FAILED",
                message=stderr or "Failed to clone",
            )
            shutil.rmtree(temp_dir, ignore_errors=True)
            return
        try:
            yield folder_to_clone_root
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


async def update_root_mirror(
    root: Dict[str, Any], group_name: str, api_token: str, action_key: str
) -> Tuple[str, bool]:
    await update_root_cloning_status(
        token=api_token,
        group_name=group_name,
        root_id=root["id"],
        status="CLONING",
        message="Cloning in progress...",
    )
    mirror_updated: bool = False

    with suppress(RuntimeError):
        async with clone_root(
            group_name=group_name, root=root, api_token=api_token
        ) as folder_to_clone_root:
            _repo = Repo(folder_to_clone_root)
            # remove not required branches
            for branch in _repo.branches:  # type: ignore
                if branch.name != root["branch"]:
                    branch.delete(_repo, branch.name, force=True)

            success_upload = await upload_cloned_repo_to_s3_tar(
                repo_path=folder_to_clone_root,
                nickname=root["nickname"],
                group_name=group_name,
            )
            if success_upload:
                try:
                    commit = Repo(
                        folder_to_clone_root,
                        search_parent_directories=True,
                    ).head.object.hexsha
                    logging.info(
                        "Cloned %s successfully with commit: %s",
                        root["nickname"],
                        commit,
                    )
                    await update_root_cloning_status(
                        token=api_token,
                        group_name=group_name,
                        root_id=root["id"],
                        status="OK",
                        message="Cloned successfully",
                        commit=commit,
                    )
                    mirror_updated = True
                    delete_action(action_dynamo_pk=action_key)
                except (GitError, AttributeError) as exc:
                    logging.exception(exc)
                    await update_root_cloning_status(
                        token=api_token,
                        group_name=group_name,
                        root_id=root["id"],
                        status="FAILED",
                        message=str(exc),
                    )

            else:
                await update_root_cloning_status(
                    token=api_token,
                    group_name=group_name,
                    root_id=root["id"],
                    status="FAILED",
                    message="The repository can not be uploaded",
                )
    return (root["nickname"], mirror_updated)


async def main() -> None:
    logging.basicConfig(level="INFO")
    api_token = os.environ["INTEGRATES_API_TOKEN"]

    action_key = sys.argv[2]
    action = get_action(action_dynamo_pk=action_key)
    if not action:
        logging.error("The job can not be found: %s", action_key)
        return

    data = json.loads(action.additional_info)
    group_name = data["group_name"]
    root_nicknames = data["roots"]
    roots_data = await get_roots(api_token, group_name)
    if roots_data is None:
        return

    roots = [
        root
        for root in roots_data
        if root
        and root["state"] == "ACTIVE"
        and root["nickname"] in root_nicknames
    ]
    roots_update_ok = [
        await update_root_mirror(
            root=root,
            group_name=group_name,
            api_token=api_token,
            action_key=action_key,
        )
        for root in roots
    ]
    roots_to_analyze = [
        nickname for nickname, status in roots_update_ok if status
    ]
    machine_queued = await submit_group_machine_execution(
        group_name=group_name,
        root_nicknames=roots_to_analyze,
        token=api_token,
    )
    if machine_queued:
        logging.info(
            "Machine execution queued for roots:\n\t%s",
            "\n\t".join(roots_to_analyze),
        )


if __name__ == "__main__":
    run(main())
