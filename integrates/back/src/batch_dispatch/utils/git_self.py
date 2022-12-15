from batch.types import (
    CloneResult,
)
from batch_dispatch.utils.s3 import (
    upload_cloned_repo_to_s3_tar,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    InvalidParameter,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from decorators import (
    retry_on_exceptions,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
import logging
from newutils import (
    git_self as git_utils,
)
from settings.logger import (
    LOGGING,
)
import shutil
import tempfile

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


cloned_repo_to_s3_tar = retry_on_exceptions(
    exceptions=(ErrorUploadingFileS3,),
    max_attempts=4,
    sleep_seconds=120,
)(upload_cloned_repo_to_s3_tar)


async def clone_root(
    *,
    group_name: str,
    root_nickname: str,
    branch: str,
    root_url: str,
    cred: Credentials,
) -> CloneResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        if isinstance(cred.state.secret, SshSecret):
            folder_to_clone_root, stderr = await git_utils.ssh_clone(
                branch=branch,
                credential_key=cred.state.secret.key,
                repo_url=root_url,
                temp_dir=temp_dir,
            )
        elif isinstance(cred.state.secret, HttpsPatSecret):
            folder_to_clone_root, stderr = await git_utils.https_clone(
                branch=branch,
                password=None,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=cred.state.secret.token,
                user=None,
            )
        elif isinstance(cred.state.secret, HttpsSecret):
            folder_to_clone_root, stderr = await git_utils.https_clone(
                branch=branch,
                password=cred.state.secret.password,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=None,
                user=cred.state.secret.user,
            )
        else:
            raise InvalidParameter()

        if folder_to_clone_root is None:
            LOGGER.error(
                "Root cloning failed",
                extra=dict(
                    extra={
                        "group_name": group_name,
                        "root_nickname": root_nickname,
                    }
                ),
            )
            shutil.rmtree(temp_dir, ignore_errors=True)
            return CloneResult(success=False, message=stderr)

        success = await cloned_repo_to_s3_tar(
            repo_path=folder_to_clone_root,
            group_name=group_name,
            nickname=root_nickname,
        )

        if success:
            try:
                commit = Repo(
                    folder_to_clone_root, search_parent_directories=True
                ).head.object
                result = CloneResult(
                    success=success,
                    commit=commit.hexsha,
                    commit_date=datetime.fromtimestamp(commit.authored_date),
                    message=stderr,
                )
                shutil.rmtree(temp_dir, ignore_errors=True)
                return result
            except (GitError, AttributeError) as exc:
                shutil.rmtree(temp_dir, ignore_errors=True)
                LOGGER.exception(
                    exc,
                    extra=dict(
                        extra={
                            "group_name": group_name,
                            "root_nickname": root_nickname,
                        }
                    ),
                )
        shutil.rmtree(temp_dir, ignore_errors=True)
    return CloneResult(success=False, message=stderr)
