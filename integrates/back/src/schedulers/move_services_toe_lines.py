from aioextensions import (
    collect,
)
from custom_exceptions import (
    GroupNameNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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
    ToeLinesAttributesToUpdate,
)
from typing import (
    cast,
    Tuple,
)

# Constants
DEFAULT_RISK_LEVEL = -1

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()


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


async def move_repo_services_toe_lines(
    loaders: Dataloaders, group_name: str, root_id: str
) -> None:
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
        filename: services_toe_lines._replace(
            sorts_risk_level=DEFAULT_RISK_LEVEL
        )
        if services_toe_lines.sorts_risk_level == 0
        else services_toe_lines
        for filename, services_toe_lines in repo_services_toe_lines.items()
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
                    attacked_lines=repo_services_toe_lines[
                        filename
                    ].tested_lines,
                    sorts_risk_level=repo_services_toe_lines[
                        filename
                    ].sorts_risk_level,
                ),
            )
            for filename, toe_lines in repo_toe_lines.items()
            if filename in repo_services_toe_lines
            and (
                toe_lines.comments,
                toe_lines.attacked_at,
                toe_lines.attacked_lines,
                toe_lines.sorts_risk_level,
            )
            != (
                repo_services_toe_lines[filename].comments,
                repo_services_toe_lines[filename].tested_date,
                repo_services_toe_lines[filename].tested_lines,
                repo_services_toe_lines[filename].sorts_risk_level,
            )
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
            move_repo_services_toe_lines(loaders, group_name, repo.id)
            for repo in repos
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
