import asyncio


async def apply_git_config(repo_path: str) -> None:
    """apply config in the git repository"""
    await asyncio.create_subprocess_exec(
        "git", f"--git-dir={repo_path}/.git", "config", "core.quotepath", "off"
    )
