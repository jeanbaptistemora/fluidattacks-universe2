from aioextensions import (
    collect,
    run,
)
import asyncio
from custom_exceptions import (
    IndicatorAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    RootUnreliableIndicatorsToUpdate,
)
from db_model.roots.update import (
    update_unreliable_indicators as update_root_indicators,
)
from db_model.types import (
    CodeLanguage,
)
from git_self import (
    pull_repositories,
)
from groups import (
    domain as groups_domain,
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


def clone_mirrors(tmpdir: str, group: str) -> Tuple[str, List[str]]:
    os.chdir(tmpdir)
    pull_repositories(
        tmpdir=tmpdir,
        group_name=group,
        optional_repo_nickname=None,
    )
    repositories_path = f"{tmpdir}/groups/{group}/fusion"
    os.chdir(repositories_path)
    repositories = [
        _dir for _dir in os.listdir(repositories_path) if os.path.isdir(_dir)
    ]

    return repositories_path, repositories


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


async def update_language_indicators(
    loaders: Dataloaders,
    group: str,
    roots_by_nickname: Dict[str, GitRoot],
    roots_languages_distribution: Dict[str, Dict[str, int]],
) -> None:
    group_languages: Dict[str, int] = {}
    for nickname, languages in roots_languages_distribution.items():
        root = roots_by_nickname.get(nickname)
        if not root or not languages:
            continue
        for language, locs in languages.items():
            if language not in group_languages:
                group_languages[language] = locs
            else:
                group_languages[language] += locs
        try:
            await update_root_indicators(
                current_value=root,
                indicators=RootUnreliableIndicatorsToUpdate(
                    unreliable_code_languages=[
                        CodeLanguage(language=language, loc=loc)
                        for language, loc in languages.items()
                    ]
                ),
            )
            LOGGER.info("Root %s language stats were updated", nickname)
        except IndicatorAlreadyUpdated:
            LOGGER.info("Root %s language stats did not change", nickname)

    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group)
    )
    await groups_domain.update_indicators(
        group_name=group,
        indicators=GroupUnreliableIndicators(
            closed_vulnerabilities=group_indicators.closed_vulnerabilities,
            code_languages=[
                CodeLanguage(language=language, loc=loc)
                for language, loc in group_languages.items()
            ],
            exposed_over_time_cvssf=group_indicators.exposed_over_time_cvssf,
            exposed_over_time_month_cvssf=(
                group_indicators.exposed_over_time_month_cvssf
            ),
            exposed_over_time_year_cvssf=(
                group_indicators.exposed_over_time_year_cvssf
            ),
            last_closed_vulnerability_days=(
                group_indicators.last_closed_vulnerability_days
            ),
            last_closed_vulnerability_finding=(
                group_indicators.last_closed_vulnerability_finding
            ),
            max_open_severity=group_indicators.max_open_severity,
            max_open_severity_finding=(
                group_indicators.max_open_severity_finding
            ),
            max_severity=group_indicators.max_severity,
            mean_remediate=group_indicators.mean_remediate,
            mean_remediate_critical_severity=(
                group_indicators.mean_remediate_critical_severity
            ),
            mean_remediate_high_severity=(
                group_indicators.mean_remediate_high_severity
            ),
            mean_remediate_low_severity=(
                group_indicators.mean_remediate_low_severity
            ),
            mean_remediate_medium_severity=(
                group_indicators.mean_remediate_medium_severity
            ),
            open_findings=group_indicators.open_findings,
            open_vulnerabilities=group_indicators.open_vulnerabilities,
            remediated_over_time=group_indicators.remediated_over_time,
            remediated_over_time_30=group_indicators.remediated_over_time_30,
            remediated_over_time_90=group_indicators.remediated_over_time_90,
            remediated_over_time_cvssf=(
                group_indicators.remediated_over_time_cvssf
            ),
            remediated_over_time_cvssf_30=(
                group_indicators.remediated_over_time_cvssf_30
            ),
            remediated_over_time_cvssf_90=(
                group_indicators.remediated_over_time_cvssf_90
            ),
            remediated_over_time_month=(
                group_indicators.remediated_over_time_month
            ),
            remediated_over_time_month_cvssf=(
                group_indicators.remediated_over_time_month_cvssf
            ),
            remediated_over_time_year=(
                group_indicators.remediated_over_time_year
            ),
            remediated_over_time_year_cvssf=(
                group_indicators.remediated_over_time_year_cvssf
            ),
            treatment_summary=group_indicators.treatment_summary,
            unfulfilled_standards=group_indicators.unfulfilled_standards,
        ),
    )
    LOGGER.info("Group %s language stats were updated", group)


async def main() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_group_names(loaders)
    groups_roots = await loaders.group_roots.load_many(list(groups))
    for group, roots in zip(groups, groups_roots):
        active_git_roots: List[GitRoot] = [
            root
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            )
        ]
        LOGGER.info(
            "Updating language stats for group %s in %s roots",
            group,
            len(active_git_roots),
        )

        roots_nicknames: List[str] = [
            root.state.nickname for root in active_git_roots
        ]
        roots_by_nickname: Dict[str, GitRoot] = {
            root.state.nickname: root for root in active_git_roots
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            clone_path, clone_repos = clone_mirrors(tmpdir=tmpdir, group=group)
            languages_distribution: Tuple[Dict[str, int], ...] = await collect(
                (
                    get_root_languages_stats(
                        path=clone_path,
                        folder=repo,
                        group=group,
                        roots_nicknames=roots_nicknames,
                    )
                    for repo in clone_repos
                ),
                workers=os.cpu_count(),  # type: ignore
            )
            roots_language_distribution: Dict[str, Dict[str, int]] = dict(
                zip(clone_repos, languages_distribution)
            )
        await update_language_indicators(
            loaders=loaders,
            group=group,
            roots_by_nickname=roots_by_nickname,
            roots_languages_distribution=roots_language_distribution,
        )


if __name__ == "__main__":
    run(main())
