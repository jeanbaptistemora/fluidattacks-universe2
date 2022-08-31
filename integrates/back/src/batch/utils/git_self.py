from aioextensions import (
    collect,
)
from batch.types import (
    CloneResult,
)
from batch.utils.s3 import (
    upload_cloned_repo_to_s3_tar,
)
from concurrent.futures import (
    ThreadPoolExecutor,
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
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from git import (
    GitError,
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
from typing import (
    Optional,
)
from vulnerabilities.domain.rebase import (
    rebase as rebase_vulnerability,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


cloned_repo_to_s3_tar = retry_on_exceptions(
    exceptions=(ErrorUploadingFileS3,),
    max_attempts=4,
    sleep_seconds=120,
)(upload_cloned_repo_to_s3_tar)


async def _get_vulnerabilities_to_rebase(
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
) -> tuple[Vulnerability, ...]:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: tuple[
        tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities.load_many(
        tuple(find.id for find in findings)
    )
    vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vuln
        for vulns in findings_vulns
        for vuln in vulns
        if vuln.root_id == git_root.id
        and vuln.commit is not None
        and vuln.type == VulnerabilityType.LINES
    )
    return vulnerabilities


def _rebase_vulnerability(
    repo: Repo, vulnerability: Vulnerability
) -> Optional[git_utils.RebaseResult]:
    try:
        if vulnerability.commit and (
            result := git_utils.rebase(
                repo,
                path=vulnerability.where,
                line=int(vulnerability.specific),
                rev_a=str(
                    vulnerability.commit if vulnerability.commit else None
                ),
                rev_b="HEAD",
            )
        ):
            return result
    except GitError as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra={
                    "vuln_id": vulnerability.id,
                }
            ),
        )
    return None


async def rebase_root(
    loaders: Dataloaders, group_name: str, repo: Repo, git_root: GitRoot
) -> None:
    vulnerabilities = await _get_vulnerabilities_to_rebase(
        loaders, group_name, git_root
    )
    with ThreadPoolExecutor(max_workers=8) as executor:
        all_rebase: tuple[
            tuple[Optional[git_utils.RebaseResult], Vulnerability], ...
        ] = tuple(
            executor.map(
                lambda vuln: (_rebase_vulnerability(repo, vuln), vuln),
                vulnerabilities,
            )
        )
    futures = [
        rebase_vulnerability(
            finding_id=vuln.finding_id,
            finding_vulns_data=tuple(
                item
                for item in vulnerabilities
                if item.finding_id == vuln.finding_id
            ),
            vulnerability_commit=rebase_result.rev,
            vulnerability_id=vuln.id,
            vulnerability_where=rebase_result.path,
            vulnerability_specific=str(rebase_result.line),
            vulnerability_type=vuln.type,
        )
        for rebase_result, vuln in all_rebase
        if rebase_result
    ]
    await collect(futures)


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
                    commit_date=datetime.fromtimestamp(
                        commit.authored_date
                    ).isoformat(),
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
