import aiofiles  # type: ignore
import asyncio
from batch.types import (
    BatchProcessing,
)
from context import (
    FI_TOE_LINES_RULES,
)
import os
import tempfile
from typing import (
    Set,
)

CLOC_ENV = os.environ.copy()
CLOC_ENV["LC_ALL"] = "C"
CLOC_DOC_LANGS = ["Markdown"]
CLOC_STYLE_LANGS = ["CSS", "SASS", "LESS", "Stylus"]
CLOC_FORMAT_LANGS = ["XML", "XAML"]
CLOC_FORCE_LANG_DEF = "--force-lang-def=" + FI_TOE_LINES_RULES
CLOC_EXCLUDE_LIST = ",".join(
    CLOC_DOC_LANGS + CLOC_STYLE_LANGS + CLOC_FORMAT_LANGS
)
CLOC_EXCLUDE_LANG = "--exclude-lang=" + CLOC_EXCLUDE_LIST


async def apply_git_config(repo_path: str) -> None:
    """apply config in the git repository"""
    await asyncio.create_subprocess_exec(
        "git", f"--git-dir={repo_path}/.git", "config", "core.quotepath", "off"
    )


async def get_ignored_files(repo_path: str) -> Set[str]:
    ignored_files = set()
    call_cloc = ["cloc", CLOC_FORCE_LANG_DEF, CLOC_EXCLUDE_LANG]
    call_cloc += [repo_path, "--ignored", "ignored.txt", "--timeout", "900"]
    await asyncio.create_subprocess_exec(*call_cloc, env=CLOC_ENV)
    async with aiofiles.open("ignored.txt", "r", encoding="utf8") as outfile:
        lines = await outfile.readlines()
        ignored_files = {line.split(":  ")[0] for line in lines}

    return ignored_files


def make_group_dir(tmpdir: str, group_name: str) -> None:
    group_dir = os.path.join(tmpdir, "groups", group_name)
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(tmpdir: str, group_name: str) -> None:
    make_group_dir(tmpdir, group_name)
    os.system(  # nosec
        "CI=true "
        "CI_COMMIT_REF_NAME=master "
        "PROD_AWS_ACCESS_KEY_ID=$SERVICES_PROD_AWS_ACCESS_KEY_ID "
        "PROD_AWS_SECRET_ACCESS_KEY=$SERVICES_PROD_AWS_SECRET_ACCESS_KEY "
        f"melts drills --pull-repos {group_name} "
    )


async def refresh_toe_lines(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        pull_repositories(tmpdir, group_name)
        os.chdir(current_dir)
