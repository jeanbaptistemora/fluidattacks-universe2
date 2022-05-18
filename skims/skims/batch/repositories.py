import aiohttp
from aiohttp.client_exceptions import (
    ClientResponseError,
)
import asyncio
from ctx import (
    NAMESPACES_FOLDER,
)
from git import (
    Repo,
)
from git.exc import (
    GitError,
)
from integrates.dal import (
    get_group_roots,
)
import os
import pathspec
from pathspec.patterns.gitwildmatch import (
    GitWildMatchPattern,
)
import shutil
import tempfile
from typing import (
    List,
    Optional,
)
from utils.fs import (
    iter_rel_paths,
)
from utils.logs import (
    log_blocking,
    log_exception_blocking,
)


def match_file(patterns: List[GitWildMatchPattern], file: str) -> bool:
    matches = []
    for pattern in patterns:
        if pattern.include is not None:
            if file in pattern.match((file,)):
                matches.append(pattern.include)
            elif not pattern.include:
                matches.append(True)

    return all(matches) if matches else False


async def get_namespace(
    group_name: str,
    root_nickname: str,
    presigned_ulr: Optional[str] = None,
    delete: bool = True,
) -> Optional[str]:
    path = await pull_namespace_from_s3(
        group_name, root_nickname, presigned_ulr
    )
    if delete:
        await delete_out_of_scope_files(group_name, root_nickname)
    return path


async def delete_out_of_scope_files(
    group_name: str, *root_nicknames: str
) -> bool:
    roots = await get_group_roots(group=group_name)
    for root in roots:
        if root.nickname not in root_nicknames:
            continue
        # Get the expected repo name from the URL
        nickname = root.nickname
        spec_ignore = pathspec.PathSpec.from_lines(
            "gitwildmatch", root.gitignore
        )
        # Compute what files should be deleted according to the scope rules
        path_to_namespace = os.path.join(
            NAMESPACES_FOLDER, group_name, nickname
        )
        for path in iter_rel_paths(path_to_namespace):
            if match_file(spec_ignore.patterns, path):
                if path.startswith(".git/"):
                    continue
                path_to_delete = os.path.join(path_to_namespace, path)
                if os.path.isfile(path_to_delete):
                    os.unlink(path_to_delete)
                elif os.path.isdir(path_to_delete):
                    shutil.rmtree(path_to_delete)

    return True


async def pull_namespace_from_s3(
    group_name: str,
    root_nickname: str,
    presigned_url: Optional[str] = None,
) -> Optional[str]:
    local_path = os.path.join(NAMESPACES_FOLDER, group_name, root_nickname)
    os.makedirs(local_path, mode=0o700, exist_ok=True)

    if presigned_url:
        async with aiohttp.ClientSession() as session:
            async with session.get(presigned_url, timeout=None) as response:
                try:
                    response.raise_for_status()
                except ClientResponseError:
                    log_blocking("error", "failed to download root")
                    return None

                _, file_path = tempfile.mkstemp()

                with open(file_path, "wb") as file_handler:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        file_handler.write(chunk)

                proc = await asyncio.create_subprocess_exec(
                    "tar",
                    "-xf",
                    file_path,
                    cwd=os.path.join(NAMESPACES_FOLDER, group_name),
                )
                _, _stderr = await proc.communicate()
                os.remove(file_path)
                if proc.returncode != 0:
                    log_blocking(
                        "error", "failed to decompress repo %s", _stderr
                    )
                    return None
    else:
        aws_sync_command: List[str] = [
            "aws",
            "s3",
            "sync",
            "--delete",
            "--sse",
            "AES256",
            "--exact-timestamps",
            f"s3://continuous-repositories/{group_name}/{root_nickname}",
            local_path,
        ]
        proc = await asyncio.create_subprocess_exec(
            *aws_sync_command,
            env={**os.environ.copy()},
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.STDOUT,
        )
        _, _stderr = await proc.communicate()
        if _stderr:
            log_blocking("error", _stderr.decode("utf-8"))
            return None

    try:
        repo = Repo(local_path)
        repo.git.reset("--hard", "HEAD")
    except GitError as exc:
        log_blocking("error", "Expand repositories has failed:")
        log_exception_blocking("exception", exc)
        return None

    return local_path
