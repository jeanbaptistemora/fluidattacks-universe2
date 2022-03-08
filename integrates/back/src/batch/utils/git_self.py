import asyncio
import base64
from batch.types import (
    CloneResult,
)
from batch.utils.s3 import (
    upload_cloned_repo_to_s3,
)
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    CredentialItem,
)
from git.exc import (
    GitError,
)
from git.objects.commit import (
    Commit,
)
from git.repo.base import (
    Repo,
)
import logging
import os
from settings.logger import (
    LOGGING,
)
import tempfile
from typing import (
    Optional,
)
from urllib.parse import (
    urlparse,
)
import uuid

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def ssh_clone_root(
    *,
    group_name: str,
    root_nickname: str,
    branch: str,
    root_url: str,
    cred: CredentialItem,
) -> CloneResult:
    success: bool = False
    raw_root_url = root_url.replace(f"{urlparse(root_url).scheme}://", "")

    if cred.state.key is None:
        return CloneResult(success=False)

    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(cred.state.key).decode())

        folder_to_clone_root = f"{temp_dir}/{root_nickname}"
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
                    "StrictHostKeyChecking=no"
                ),
            },
        )
        _, stderr = await proc.communicate()

        os.remove(ssh_file_name)
        commit: Optional[Commit] = None
        if proc.returncode != 0:
            LOGGER.error(
                "Root SSH cloning failed",
                extra=dict(
                    extra={
                        "group_name": group_name,
                        "root_nickname": root_nickname,
                        "stderr": stderr.decode(),
                    }
                ),
            )
        else:
            success = await upload_cloned_repo_to_s3(
                repo_path=folder_to_clone_root,
                group_name=group_name,
                nickname=root_nickname,
            )
            with suppress(GitError, AttributeError):
                commit = Repo(
                    folder_to_clone_root, search_parent_directories=True
                ).head.object
        if commit:
            return CloneResult(
                success=success,
                commit=commit.hexsha,
                commit_date=datetime.fromtimestamp(
                    commit.authored_date
                ).isoformat(),
            )
    return CloneResult(success=success)
