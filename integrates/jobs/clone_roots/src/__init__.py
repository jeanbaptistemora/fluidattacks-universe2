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
import http.client
import json
import logging
import os
import requests  # type: ignore
import shutil
import sys
import tarfile
import tempfile
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
    Tuple,
)
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    quote_plus,
    urlparse,
)
import uuid


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


def get_roots(token: str, group_name: str) -> Optional[Dict[str, Any]]:
    conn = http.client.HTTPSConnection("app.fluidattacks.com")
    query = """
        query GetRootUpload($groupName: String!) {
            group(groupName: $groupName) {
              roots {
                ... on GitRoot {
                  id
                  nickname
                  uploadUrl
                  branch
                  url
                  credentials {
                    id
                    user
                    password
                    token
                    key
                  }
                  state
                }
              }
            }
        }
    """
    payload = {"query": query, "variables": {"groupName": group_name}}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/api", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    with suppress(json.decoder.JSONDecodeError):
        result = json.loads(data.decode("utf-8"))
        if "errors" in result:
            logging.error(result["errors"])
            return None
        return result
    return None


def update_root_cloning_status(  # pylint: disable=too-many-arguments
    token: str,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
    commit: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    conn = http.client.HTTPSConnection("app.fluidattacks.com")
    query = """
        mutation MeltsUpdateRootCloningStatus(
          $groupName: String!
          $rootId: ID!
          $status: CloningStatus!
          $message: String!
          $commit: String
        ) {
          updateRootCloningStatus(
            groupName: $groupName
            id: $rootId
            status: $status
            message: $message
            commit: $commit
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
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/api", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    with suppress(json.decoder.JSONDecodeError):
        result = json.loads(data.decode("utf-8"))
        if "errors" in result:
            logging.error(result["errors"])
            return None
        return result
    return None


def _format_https_url(
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    user = quote_plus(user) if user is not None else user
    password = quote_plus(password) if password is not None else password
    parsed_url = parse_url(repo_url)
    if token is not None:
        url = str(parsed_url._replace(auth=token))
    elif user is not None and password is not None:
        url = str(parsed_url._replace(auth=f"{user}:{password}"))
    else:
        raise Exception()

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
                f"ssh -i {ssh_file_name} -o"
                "UserKnownHostsFile=/dev/null -o "
                "StrictHostKeyChecking=no -o "
                "IdentitiesOnly=yes"
            ),
        },
    )
    _, stderr = await proc.communicate()

    os.remove(ssh_file_name)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    logging.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: Optional[str] = None,
    token: Optional[str] = None,
    user: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    url = _format_https_url(repo_url, user, password, token)
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


async def upload_cloned_repo_to_s3_tar(
    *, repo_path: str, nickname: str, upload_url: str
) -> bool:
    success: bool = False
    _, zip_output_path = tempfile.mkstemp()

    if not create_git_root_tar_file(nickname, repo_path, zip_output_path):
        logging.error(
            "Failed to compress root %s",
            nickname,
            extra=dict(extra=locals()),
        )
        os.remove(zip_output_path)
        return False
    with open(zip_output_path, "rb") as object_file:
        object_text = object_file.read()
        response = requests.put(upload_url, data=object_text)
        response.raise_for_status()
        success = True
    os.remove(zip_output_path)
    return success


@asynccontextmanager
async def clone_root(
    *, group_name: str, root: Dict[str, Any], token: str
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
            )
        elif user := cred.get("user") and (password := cred.get("password")):
            folder_to_clone_root, stderr = await https_clone(
                branch=branch,
                password=password,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=None,
                user=user,
            )
        else:
            raise Exception()

        if folder_to_clone_root is None:
            logging.error(
                "Root cloning failed",
                extra=dict(
                    extra={
                        "group_name": group_name,
                        "root_nickname": root_nickname,
                        "stderr": stderr,
                    }
                ),
            )
            update_root_cloning_status(
                token=token,
                group_name=group_name,
                root_id=root["id"],
                status="FAILED",
                message=stderr or "Failed to clone",
            )
            shutil.rmtree(temp_dir, ignore_errors=True)
            return
            yield
        try:
            yield folder_to_clone_root
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


async def main() -> None:
    logging.basicConfig(level="INFO")
    token = os.environ["INTEGRATES_API_TOKEN"]

    action_key = sys.argv[2]
    action = get_action(action_dynamo_pk=action_key)
    if not action:
        logging.error("The job can not be found: %s", action_key)
        return

    data = json.loads(action.additional_info)
    group_name = data["group_name"]
    root_nicknames = data["roots"]
    roots_data = get_roots(token, group_name)
    if not roots_data:
        return

    roots = [
        root
        for root in roots_data["data"]["group"]["roots"]
        if root["state"] == "ACTIVE" and root["nickname"] in root_nicknames
    ]
    for root in roots:
        update_root_cloning_status(
            token=token,
            group_name=group_name,
            root_id=root["id"],
            status="CLONING",
            message="Cloning in progress...",
        )

        logging.info("Cloning %s", root["nickname"])

        async with clone_root(
            group_name=group_name, root=root, token=token
        ) as folder_to_clone_root:
            success_upload = await upload_cloned_repo_to_s3_tar(
                repo_path=folder_to_clone_root,
                nickname=root["nickname"],
                upload_url=root["uploadUrl"],
            )
            if success_upload:
                try:
                    commit = Repo(
                        folder_to_clone_root, search_parent_directories=True
                    ).head.object.hexsha
                    logging.info(
                        "Cloned success with commit: %s",
                        commit,
                    )
                    update_root_cloning_status(
                        token=token,
                        group_name=group_name,
                        root_id=root["id"],
                        status="OK",
                        message="Cloned successfully",
                        commit=commit,
                    )
                    delete_action(action_dynamo_pk=action_key)
                    continue
                except (GitError, AttributeError) as exc:
                    logging.exception(
                        exc,
                        extra=dict(
                            extra={
                                "group_name": group_name,
                                "root_nickname": root["nickname"],
                            }
                        ),
                    )
                    update_root_cloning_status(
                        token=token,
                        group_name=group_name,
                        root_id=root["id"],
                        status="FAILED",
                        message=str(exc),
                    )
                    continue

            update_root_cloning_status(
                token=token,
                group_name=group_name,
                root_id=root["id"],
                status="FAILED",
                message="The repository can not be uploaded",
            )


if __name__ == "__main__":
    run(main())
