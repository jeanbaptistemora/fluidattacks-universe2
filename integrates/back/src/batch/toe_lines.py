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
