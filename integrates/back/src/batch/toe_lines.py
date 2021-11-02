import asyncio
import os


async def apply_git_config(repo_path: str) -> None:
    """apply config in the git repository"""
    await asyncio.create_subprocess_exec(
        "git", f"--git-dir={repo_path}/.git", "config", "core.quotepath", "off"
    )


def make_group_dir(tmpdir: str, group_name: str) -> None:
    group_dir = os.path.join(tmpdir, "groups", group_name)
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(tmpdir: str, group_name: str) -> None:
    make_group_dir(tmpdir, group_name)
    os.system(  # nosec
        f"PROD_AWS_ACCESS_KEY_ID=$SERVICES_PROD_AWS_ACCESS_KEY_ID "
        f"PROD_AWS_SECRET_ACCESS_KEY=$SERVICES_PROD_AWS_SECRET_ACCESS_KEY "
        f"melts drills --pull-repos {group_name}"
    )
