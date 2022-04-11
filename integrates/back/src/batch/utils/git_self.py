from batch.types import (
    CloneResult,
)
from batch.utils.s3 import (
    upload_cloned_repo_to_s3_tar,
)
from custom_exceptions import (
    InvalidParameter,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    CredentialItem,
)
from db_model.enums import (
    CredentialType,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
import logging
import newutils.git
from settings.logger import (
    LOGGING,
)
import tempfile

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def clone_root(
    *,
    group_name: str,
    root_nickname: str,
    branch: str,
    root_url: str,
    cred: CredentialItem,
) -> CloneResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        if (
            cred.metadata.type == CredentialType.SSH
            and cred.state.key is not None
        ):
            folder_to_clone_root, stderr = await newutils.git.ssh_clone(
                branch=branch,
                credential_key=cred.state.key,
                repo_url=root_url,
                temp_dir=temp_dir,
            )
        elif cred.metadata.type == CredentialType.HTTPS and (
            cred.state.token is not None
            or (
                cred.state.user is not None and cred.state.password is not None
            )
        ):
            folder_to_clone_root, stderr = await newutils.git.https_clone(
                branch=branch,
                password=cred.state.password,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=cred.state.token,
                user=cred.state.user,
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
            return CloneResult(success=False, message=stderr)

        success = await upload_cloned_repo_to_s3_tar(
            repo_path=folder_to_clone_root,
            group_name=group_name,
            nickname=root_nickname,
        )

        if success:
            try:
                commit = Repo(
                    folder_to_clone_root, search_parent_directories=True
                ).head.object
                return CloneResult(
                    success=success,
                    commit=commit.hexsha,
                    commit_date=datetime.fromtimestamp(
                        commit.authored_date
                    ).isoformat(),
                    message=stderr,
                )
            except (GitError, AttributeError) as exc:
                LOGGER.exception(
                    exc,
                    extra=dict(
                        extra={
                            "group_name": group_name,
                            "root_nickname": root_nickname,
                        }
                    ),
                )

        return CloneResult(success=False, message=stderr)
