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
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    HttpsPatSecret,
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
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
import git_self as git_utils
import logging
from newutils.datetime import (
    get_utc_now,
)
from oauth.azure import (
    get_azure_token,
)
from oauth.bitbucket import (
    get_bitbucket_token,
)
from oauth.gitlab import (
    get_token,
)
from settings.logger import (
    LOGGING,
)
import shutil
import tempfile
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


cloned_repo_to_s3_tar = retry_on_exceptions(
    exceptions=(ErrorUploadingFileS3,),
    max_attempts=4,
    sleep_seconds=120,
)(upload_cloned_repo_to_s3_tar)


async def _get_token(  # pylint: disable=too-many-return-statements
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> Optional[str]:
    if isinstance(credential.state.secret, OauthGitlabSecret):
        if credential.state.secret.valid_until <= get_utc_now():
            return await get_token(credential=credential, loaders=loaders)

        return credential.state.secret.access_token

    if isinstance(credential.state.secret, OauthAzureSecret):
        if credential.state.secret.valid_until <= get_utc_now():
            return await get_azure_token(
                credential=credential, loaders=loaders
            )

        return credential.state.secret.access_token

    if isinstance(credential.state.secret, OauthBitbucketSecret):
        if credential.state.secret.valid_until <= get_utc_now():
            return await get_bitbucket_token(
                credential=credential, loaders=loaders
            )

        return credential.state.secret.access_token

    return None


async def clone_root(
    *,
    group_name: str,
    root_nickname: str,
    branch: str,
    root_url: str,
    cred: Credentials,
    loaders: Dataloaders,
) -> CloneResult:
    token: Optional[str] = None
    _credential: Credentials
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
        elif isinstance(
            cred.state.secret, (OauthAzureSecret, OauthGitlabSecret)
        ):
            _credential = await loaders.credentials.load(
                CredentialsRequest(
                    id=cred.id,
                    organization_id=cred.organization_id,
                )
            )
            token = await _get_token(credential=_credential, loaders=loaders)
            folder_to_clone_root, stderr = await git_utils.https_clone(
                branch=branch,
                password=None,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=token,
                user=None,
                is_oauth=True,
            )
        elif isinstance(cred.state.secret, OauthGithubSecret):
            folder_to_clone_root, stderr = await git_utils.https_clone(
                branch=branch,
                password=None,
                repo_url=root_url,
                temp_dir=temp_dir,
                token=cred.state.secret.access_token,
                user=None,
                is_oauth=True,
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
