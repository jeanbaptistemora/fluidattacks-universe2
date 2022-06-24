import json
from repositories.advisory_database import (
    get_advisory_database,
)
from repositories.community_advisories import (
    get_community_advisories,
)
import sys
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Tuple,
)
from utils.logs import (
    log_blocking,
)

Advisories = Dict[str, Dict[str, str]]


REPOSITORIES: List[Tuple[Callable[[Advisories, str], dict], Iterable[str]]] = [
    (get_community_advisories, ("maven", "npm", "nuget")),
    (get_advisory_database, ("maven", "npm", "nuget", "pip")),
]
VALID_ENTRIES = ("maven", "npm", "nuget", "pip")


def main(platform: str = None) -> None:
    platform = platform or sys.argv[1] if len(sys.argv) > 1 else ""
    if platform not in VALID_ENTRIES:
        log_blocking("error", f"Invalid/Missing parameter")
        return None
    platform = sys.argv[1]
    advisories: Advisories = {}
    for fun, platforms in REPOSITORIES:
        if platform in platforms:
            fun(advisories, platform)

    log_blocking("info", f"Creating file: {platform}.json")
    with open(f"static/sca/{platform}_g.json", "w") as outfile:
        json.dump(advisories, outfile, indent=2, sort_keys=True)


main()
