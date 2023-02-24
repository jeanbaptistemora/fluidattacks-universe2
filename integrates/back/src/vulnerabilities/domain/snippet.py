from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from dynamodb.exceptions import (
    ValidationException,
)
from git.exc import (
    GitCommandError,
)
from git.repo import (
    Repo,
)
import logging
import os
from s3.operations import (
    upload_memory_file,
)
from s3.resource import (
    get_s3_resource,
)
from serializers import (
    make_snippet,
    Snippet,
    SnippetViewport,
)
from settings.logger import (
    LOGGING,
)
import tempfile

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def snippet_already_exists(
    vulnerability_id: str, vulnerability_modified_date: str | datetime
) -> bool:
    modified_date = (
        vulnerability_modified_date
        if isinstance(vulnerability_modified_date, str)
        else vulnerability_modified_date.isoformat()
    )
    client = await get_s3_resource()
    file_key = (
        f"{FI_AWS_S3_PATH_PREFIX}snippets"
        f"/VULN#{vulnerability_id}#STATE#{modified_date}"
    )
    with suppress(client.exceptions.NoSuchKey):
        await client.get_object_acl(Bucket=FI_AWS_S3_MAIN_BUCKET, Key=file_key)
        return True
    return False


async def upload_snippet(
    vulnerability_id: str, vulnerability_modified_date: str, contents: str
) -> None:
    file_key = (
        f"snippets/VULN#{vulnerability_id}#STATE"
        f"#{vulnerability_modified_date}"
    )
    with tempfile.NamedTemporaryFile() as snippet_file:
        snippet_file.write(contents.encode("utf-8", errors="ignore"))
        snippet_file.seek(os.SEEK_SET)
        await upload_memory_file(
            snippet_file,
            file_key,
        )


async def set_snippet(
    vulnerability: Vulnerability,
    last_state: VulnerabilityState,
    contents: Snippet,
) -> None:
    try:
        last_state = last_state._replace(snippet=contents)
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            entry=last_state,
        )
    except ValidationException as exc:
        LOGGER.error(
            "failed to set vulnerability snippet",
            extra={"extra": {"vulnerability_id": vulnerability.id}},
        )
        LOGGER.exception(exc)


def generate_snippet(
    vulnerability_state: VulnerabilityState, repo: Repo
) -> Snippet | None:
    current_commit = vulnerability_state.commit or "HEAD"
    with suppress(GitCommandError, ValueError):
        content = repo.git.show(
            f"{current_commit}:{vulnerability_state.where}"
        )
        return make_snippet(
            content=content,
            viewport=SnippetViewport(
                line=int(vulnerability_state.specific),
                column=0,
                show_line_numbers=False,
                highlight_line_number=False,
            ),
        )
    return None


async def get_snippet(
    vulnerability_id: str,
    vulnerability_modified_date: str | datetime,
) -> str | None:
    modified_date = (
        vulnerability_modified_date
        if isinstance(vulnerability_modified_date, str)
        else vulnerability_modified_date.isoformat()
    )
    client = await get_s3_resource()
    file_key = (
        f"{FI_AWS_S3_PATH_PREFIX}snippets"
        f"/VULN#{vulnerability_id}#STATE#{modified_date}"
    )
    with tempfile.NamedTemporaryFile() as snippet_file:
        try:
            await client.download_fileobj(
                FI_AWS_S3_MAIN_BUCKET, file_key, snippet_file
            )
        except ClientError:
            return None
        snippet_file.seek(os.SEEK_SET)
        return snippet_file.read().decode("utf-8")
