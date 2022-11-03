# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)
from db_model.vulnerabilities.types import (
    VulnerabilityState,
)
from git import (
    Repo,
)
from git.exc import (
    GitCommandError,
)
import os
from s3.operations import (
    upload_memory_file,
)
from s3.resource import (
    get_s3_resource,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
import tempfile
from typing import (
    Optional,
    Union,
)


async def snippet_already_exists(
    vulnerability_id: str, vulnerability_modified_date: Union[str, datetime]
) -> bool:
    modified_date = (
        vulnerability_modified_date
        if isinstance(vulnerability_modified_date, str)
        else vulnerability_modified_date.isoformat()
    )
    client = await get_s3_resource()
    file_key = f"snippets/VULN#{vulnerability_id}#STATE#{modified_date}"
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
        snippet_file.write(contents.encode("utf-8"))
        snippet_file.seek(os.SEEK_SET)
        await upload_memory_file(
            FI_AWS_S3_MAIN_BUCKET,
            snippet_file,
            file_key,
        )


async def get_snippet(
    vulnerability_state: VulnerabilityState, repo: Repo
) -> Optional[str]:
    current_commit = vulnerability_state.commit or "HEAD"
    with suppress(GitCommandError, ValueError):
        content = repo.git.show(
            f"{current_commit}:{vulnerability_state.where}"
        )
        return make_snippet(
            content=content,
            viewport=SnippetViewport(0, int(vulnerability_state.specific)),
        )
    return None
