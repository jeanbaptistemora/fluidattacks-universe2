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
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from typing import (
    cast,
    Tuple,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()

toe_lines_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.add)
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


def _get_attacked_lines(
    new_attacked_lines: int,
    current_attacked_lines: int,
    attacked_at: str,
    modified_date: str,
) -> int:
    attacked_lines = (
        new_attacked_lines or current_attacked_lines
        if new_attacked_lines != 0
        and attacked_at
        and modified_date
        and datetime.fromisoformat(modified_date)
        <= datetime.fromisoformat(attacked_at)
        else 0
    )
    return attacked_lines


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
                    comments=repo_services_toe_lines[filename].comments,
                    attacked_at=repo_services_toe_lines[filename].tested_date,
                    attacked_lines=_get_attacked_lines(
                        repo_services_toe_lines[filename].tested_lines,
                        toe_lines.attacked_lines,
                        repo_services_toe_lines[filename].tested_date,
                        toe_lines.modified_date,
                    ),
                    seen_at=repo_services_toe_lines[filename].tested_date
                    or toe_lines.seen_at,
                ),
            )
            for filename, toe_lines in repo_toe_lines.items()
            if filename in repo_services_toe_lines
            and (
                toe_lines.comments,
                toe_lines.attacked_at,
                toe_lines.attacked_lines,
                toe_lines.first_attack_at,
                toe_lines.seen_at,
            )
            != (
                repo_services_toe_lines[filename].comments,
                repo_services_toe_lines[filename].tested_date,
                _get_attacked_lines(
                    repo_services_toe_lines[filename].tested_lines,
                    toe_lines.attacked_lines,
                    repo_services_toe_lines[filename].tested_date,
                    toe_lines.modified_date,
                ),
                repo_services_toe_lines[filename].tested_date,
                repo_services_toe_lines[filename].tested_date
                or toe_lines.seen_at,
            )
        )
    )
    await collect(
        tuple(
            toe_lines_add(
                group_name,
                root_id,
                filename,
                ToeLinesAttributesToAdd(
                    attacked_at=services_toe_lines.tested_date,
                    attacked_by="",
                    attacked_lines=services_toe_lines.tested_lines,
                    comments=services_toe_lines.comments,
                    commit_author="",
                    loc=services_toe_lines.loc,
                    modified_commit=services_toe_lines.modified_commit,
                    modified_date=services_toe_lines.modified_date,
                    be_present=False,
                    seen_at=services_toe_lines.tested_date,
                ),
            )
            for filename, services_toe_lines in repo_services_toe_lines.items()
            if filename not in repo_toe_lines
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
