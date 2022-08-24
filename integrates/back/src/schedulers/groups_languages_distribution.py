from aioextensions import (
    collect,
    run,
)
import asyncio
from batch.actions.refresh_toe_lines import (
    pull_repositories,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
import json
import logging
from organizations import (
    domain as orgs_domain,
)
import os
import tempfile
from typing import (
    Dict,
    List,
    Tuple,
)

LOGGER = logging.getLogger(__name__)


async def get_root_languages_stats(
    path: str, folder: str, group: str, roots_nicknames: List[str]
) -> Dict[str, int]:
    languages_stats = {}
    if folder not in roots_nicknames:
        LOGGER.warning(
            "Repository has a different name compared to its nickname",
            extra={
                "extra": {
                    "group": group,
                    "name": folder,
                    "nicknames": roots_nicknames,
                }
            },
        )
    else:
        proc = await asyncio.create_subprocess_exec(
            "tokei",
            "-o",
            "json",
            os.path.join(path, folder),
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            result = json.loads(stdout.decode())
            result.pop("Total", None)
            for language in result.keys():
                loc = result[language]["code"] + result[language]["comments"]
                if children := result[language]["children"]:
                    loc += sum(
                        child["stats"]["code"] + child["stats"]["comments"]
                        for child_lang in children.keys()
                        for child in children[child_lang]
                    )
                languages_stats.update({language: loc})
        else:
            LOGGER.error(
                "Error running tokei over repository",
                extra={
                    "extra": {
                        "error": stderr.decode(),
                        "group": group,
                        "repository": folder,
                    }
                },
            )

    return languages_stats


async def main() -> None:
    loaders = get_new_context()
    groups: Tuple[str, ...] = await orgs_domain.get_all_active_group_names(
        loaders
    )
    groups_roots = await loaders.group_roots.load_many(groups)
    for group, roots in zip(groups, groups_roots):
        active_git_roots = [
            root
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            )
        ]
        roots_nicknames = [root.state.nickname for root in active_git_roots]
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            pull_repositories(
                tmpdir=tmpdir,
                group_name=group,
                optional_repo_nickname=None,
            )
            repositories_path = f"{tmpdir}/groups/{group}/fusion"
            os.chdir(repositories_path)
            repositories = [
                _dir
                for _dir in os.listdir(repositories_path)
                if os.path.isdir(_dir)
            ]
            languages_distribution = await collect(
                (
                    get_root_languages_stats(
                        path=repositories_path,
                        folder=repository,
                        group=group,
                        roots_nicknames=roots_nicknames,
                    )
                    for repository in repositories
                ),
                workers=os.cpu_count(),
            )
            roots_language_distribution = dict(
                zip(repositories, languages_distribution)
            )
            LOGGER.info(
                "Language distribution for group %s: %s",
                group,
                roots_language_distribution,
            )


if __name__ == "__main__":
    run(main())
