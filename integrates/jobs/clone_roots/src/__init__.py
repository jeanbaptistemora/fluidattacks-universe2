import asyncio
import base64
from contextlib import (
    suppress,
)
import http.client
import json
import logging
import os
from typing import (
    Any,
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


def get_roots(token: str, group_name: str) -> Optional[dict[str, Any]]:
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
) -> Optional[dict[str, Any]]:
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
