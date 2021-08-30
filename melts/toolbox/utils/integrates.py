import json
import multiprocessing.pool
from retry import (  # type: ignore
    retry,
)
from toolbox import (
    api,
)
from toolbox.api.exceptions import (
    IntegratesError,
)
from toolbox.constants import (
    API_TOKEN,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.env import (
    guess_environment,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

if guess_environment() == "production":
    RETRIES = 10
    DELAY = 5
else:
    RETRIES = 1
    DELAY = 2


def get_project_repos(project: str) -> List:
    """Return the repositories for a project."""
    repositories: List[str] = []
    response = api.integrates.Queries.resources(
        api_token=API_TOKEN, project_name=project
    )
    if response.ok:
        repositories = json.loads(response.data["resources"]["repositories"])
    else:
        LOGGER.error("An error has occurred querying the %s group", project)
        LOGGER.error(response.errors)

    return repositories


def get_filter_rules(group: str) -> List[Dict[str, Any]]:
    filter_request = api.integrates.Queries.git_roots_filter(API_TOKEN, group)
    if not filter_request.ok:
        LOGGER.error("An error has occurred querying the %s group", group)
        LOGGER.error(filter_request.errors)
        return list()
    return filter_request.data["project"]["roots"]


@retry(IntegratesError, tries=RETRIES, delay=DELAY)
def has_forces(group: str) -> bool:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        raise IntegratesError(response.errors)

    return response.data["project"]["hasForces"]


@retry(IntegratesError, tries=RETRIES, delay=DELAY)
def get_projects_with_forces() -> List[str]:
    response = api.integrates.Queries.get_projects_with_forces(API_TOKEN)

    if not response.ok:
        raise IntegratesError(response.errors)

    return response.data["groupsWithForces"]


def get_projects_with_forces_json_str() -> bool:
    print(json.dumps(get_projects_with_forces()))
    return True


@retry(IntegratesError, tries=RETRIES, delay=DELAY, logger=LOGGER)
def get_group_language(group: str) -> str:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        LOGGER.error("An error has occurred querying the %s group", group)
        raise IntegratesError(response.errors)

    return response.data["project"]["language"]


@retry(IntegratesError, tries=RETRIES, delay=DELAY)
def has_drills(group: str) -> bool:
    response = api.integrates.Queries.get_group_info(API_TOKEN, group)
    if not response.ok:
        raise IntegratesError(response.errors)

    return response.data["project"]["hasDrills"]


@retry(IntegratesError, tries=RETRIES, delay=DELAY)
def get_forces_token(group: str) -> str:
    response = api.integrates.Queries.get_forces_token(API_TOKEN, group)
    if not response.ok:
        raise IntegratesError(response.errors)

    return response.data["project"]["forcesToken"]


def filter_groups_with_forces(groups: Tuple[str, ...]) -> Tuple[str, ...]:
    with multiprocessing.pool.ThreadPool(10) as pool:
        return tuple(
            group
            for group, group_has_forces in zip(
                groups,
                pool.map(has_forces, groups),
            )
            if group_has_forces
        )


def filter_groups_with_forces_as_json_str(groups: Tuple[str, ...]) -> bool:
    print(json.dumps(filter_groups_with_forces(groups)))
    return True


def update_root_cloning_status(
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> bool:
    if status not in {"OK", "FAILED", "UNKNOWN"}:
        raise ValueError(f"{status} is an invalid status")

    result = api.integrates.Mutations.update_cloning_status(
        API_TOKEN,
        group_name,
        root_id,
        status,
        message,
    )

    if result.errors:
        LOGGER.error(
            "An error has occurred updating the status: %s",
            result.errors[0]["message"],
        )
        return False
    if not result.data["updateRootCloningStatus"]["success"]:
        LOGGER.error("An error has occurred updating the status")
    return result.data["updateRootCloningStatus"]["success"]
