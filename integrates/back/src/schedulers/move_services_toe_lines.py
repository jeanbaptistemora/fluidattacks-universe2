from aioextensions import (
    collect,
)
from custom_exceptions import (
    GroupNameNotFound,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import glob
import logging
import logging.config
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    git as git_utils,
)
import re
from settings import (
    LOGGING,
)
import tempfile
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from typing import (
    cast,
    Optional,
    Tuple,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()

toe_lines_remove = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.remove)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.update)


def _get_group_name(tmpdirname: str, lines_csv_path: str) -> str:
    group_match = re.match(
        pattern=fr"{tmpdirname}/groups/(\w+)", string=lines_csv_path
    )
    if not group_match:
        raise GroupNameNotFound()

    return group_match.groups("1")[0]


def _get_attacked_at(
    services_toe_lines: ServicesToeLines,
    toe_lines: ToeLines,
) -> Optional[datetime]:
    if services_toe_lines.tested_date and (
        toe_lines.attacked_at
        and datetime.fromisoformat(services_toe_lines.tested_date)
        > toe_lines.attacked_at
    ):
        return datetime.fromisoformat(services_toe_lines.tested_date)
    if toe_lines.attacked_at is not None:
        return toe_lines.attacked_at
    return (
        datetime.fromisoformat(services_toe_lines.tested_date)
        if services_toe_lines.tested_date
        else None
    )


def _get_attacked_lines(
    new_attacked_lines: int,
    toe_lines: ToeLines,
    new_attacked_at: Optional[datetime],
) -> int:
    if new_attacked_at == toe_lines.attacked_at:
        attacked_lines = toe_lines.attacked_lines
    else:
        attacked_lines = (
            new_attacked_lines
            if new_attacked_at
            and toe_lines.modified_date
            and toe_lines.modified_date <= new_attacked_at
            else 0
        )
    if attacked_lines > toe_lines.loc:
        attacked_lines = toe_lines.loc
    return attacked_lines


def _get_comments(
    new_comments: str,
    toe_lines: ToeLines,
    new_attacked_at: Optional[datetime],
) -> str:
    if new_attacked_at == toe_lines.attacked_at:
        comments = toe_lines.comments
    else:
        comments = (
            new_comments
            if new_attacked_at
            and toe_lines.attacked_at
            and toe_lines.attacked_at < new_attacked_at
            else ""
        )
    return comments


def _get_first_attack_at(
    services_toe_lines: ServicesToeLines,
    toe_lines: ToeLines,
) -> Optional[datetime]:
    if services_toe_lines.tested_date and (
        toe_lines.first_attack_at
        and datetime.fromisoformat(services_toe_lines.tested_date)
        < toe_lines.first_attack_at
    ):
        return datetime.fromisoformat(services_toe_lines.tested_date)
    if toe_lines.first_attack_at is not None:
        return toe_lines.first_attack_at
    return (
        datetime.fromisoformat(services_toe_lines.tested_date)
        if services_toe_lines.tested_date
        else None
    )


def _get_seen_at(
    services_toe_lines: ServicesToeLines,
    toe_lines: ToeLines,
) -> datetime:
    return (
        datetime.fromisoformat(services_toe_lines.tested_date)
        if services_toe_lines.tested_date
        and datetime.fromisoformat(services_toe_lines.tested_date)
        < toe_lines.seen_at
        else toe_lines.seen_at
    )


@retry_on_exceptions(
    exceptions=(ToeLinesAlreadyUpdated,),
    sleep_seconds=10,
)
async def move_repo_services_toe_lines(group_name: str, root_id: str) -> None:
    loaders = get_new_context()
    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(group_name=group_name, root_id=root_id)
        )
    }
    repo_services_toe_lines = {
        services_toe_lines.filename: services_toe_lines
        for services_toe_lines in cast(
            Tuple[ServicesToeLines, ...],
            await loaders.root_services_toe_lines.load((group_name, root_id)),
        )
    }
    repo_services_toe_lines = {
        filename: services_toe_lines._replace(tested_date="")
        if services_toe_lines.tested_date == datetime_utils.DEFAULT_ISO_STR
        else services_toe_lines
        for filename, services_toe_lines in repo_services_toe_lines.items()
    }
    await collect(
        tuple(
            toe_lines_update(
                toe_lines,
                ToeLinesAttributesToUpdate(
                    comments=_get_comments(
                        repo_services_toe_lines[filename].comments,
                        toe_lines,
                        _get_attacked_at(
                            repo_services_toe_lines[filename], toe_lines
                        ),
                    ),
                    attacked_at=_get_attacked_at(
                        repo_services_toe_lines[filename], toe_lines
                    ),
                    attacked_lines=_get_attacked_lines(
                        repo_services_toe_lines[filename].tested_lines,
                        toe_lines,
                        _get_attacked_at(
                            repo_services_toe_lines[filename], toe_lines
                        ),
                    ),
                    first_attack_at=_get_first_attack_at(
                        repo_services_toe_lines[filename], toe_lines
                    ),
                    has_vulnerabilities=toe_lines.has_vulnerabilities or False,
                    seen_at=_get_seen_at(
                        repo_services_toe_lines[filename], toe_lines
                    ),
                    is_moving_toe_lines=True,
                ),
            )
            for filename, toe_lines in repo_toe_lines.items()
            if filename in repo_services_toe_lines
            and (
                toe_lines.comments,
                toe_lines.attacked_at,
                toe_lines.attacked_lines,
                toe_lines.first_attack_at,
                toe_lines.has_vulnerabilities or False,
                toe_lines.seen_at,
            )
            != (
                _get_comments(
                    repo_services_toe_lines[filename].comments,
                    toe_lines,
                    _get_attacked_at(
                        repo_services_toe_lines[filename], toe_lines
                    ),
                ),
                _get_attacked_at(repo_services_toe_lines[filename], toe_lines),
                _get_attacked_lines(
                    repo_services_toe_lines[filename].tested_lines,
                    toe_lines,
                    _get_attacked_at(
                        repo_services_toe_lines[filename], toe_lines
                    ),
                ),
                _get_first_attack_at(
                    repo_services_toe_lines[filename], toe_lines
                ),
                toe_lines.has_vulnerabilities,
                _get_seen_at(repo_services_toe_lines[filename], toe_lines),
            )
        )
    )
    non_present_toe_lines = await loaders.root_toe_lines.load_nodes(
        RootToeLinesRequest(
            group_name=group_name, root_id=root_id, be_present=False
        )
    )
    await collect(
        tuple(
            toe_lines_remove(
                toe_lines.group_name, toe_lines.root_id, toe_lines.filename
            )
            for toe_lines in non_present_toe_lines
            if not toe_lines.be_present and not toe_lines.commit_author
        )
    )


async def move_group_services_toe_lines(
    loaders: Dataloaders, group_name: str
) -> None:
    LOGGER_CONSOLE.info(
        "Moving services toe lines",
        extra={"extra": {"group_name": group_name}},
    )
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    repos = tuple(root for root in roots if isinstance(root, GitRootItem))
    await collect(
        tuple(
            move_repo_services_toe_lines(group_name, repo.id) for repo in repos
        )
    )


async def main() -> None:
    """Move the services toe lines info to the toe lines"""
    loaders = get_new_context()
    with tempfile.TemporaryDirectory() as tmpdirname:
        git_utils.clone_services_repository(tmpdirname)
        lines_csv_glob = f"{tmpdirname}/groups/*/toe/lines.csv"
        lines_cvs_paths = glob.glob(lines_csv_glob)
        services_group_names = set(
            _get_group_name(tmpdirname, lines_cvs_path)
            for lines_cvs_path in lines_cvs_paths
        )
        await collect(
            tuple(
                move_group_services_toe_lines(loaders, group_name)
                for group_name in services_group_names
            ),
            workers=20,
        )
