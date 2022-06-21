import json
from repositories.advisory_database import (
    get_advisory_database,
)
from repositories.community_advisories import (
    get_community_advisories,
)
import sys
from typing import (
    Any,
    Dict,
)
from utils.logs import (
    log_blocking,
)

Advisories = Dict[str, Dict[str, str]]


def main(platform: str = None) -> None:
    platform = platform or sys.argv[1] if len(sys.argv) > 1 else ""
    if platform not in ("maven", "npm", "nuget"):
        log_blocking("error", f"Invalid/Missing parameter")
        return None
    platform = sys.argv[1]
    advisories: Advisories = {}
    for fun in (
        get_community_advisories,
        get_advisory_database,
    ):
        fun(advisories, platform)

    log_blocking("info", f"Creating file: {platform}.json")
    with open(f"static/sca/{platform}.json", "w") as outfile:
        json.dump(advisories, outfile, indent=2, sort_keys=True)


main()
