import json
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


def main(language: str = None) -> None:
    language = language or sys.argv[1] if len(sys.argv) > 1 else ""
    if language not in ("maven", "npm", "nuget"):
        log_blocking("error", f"Invalid/Missing parameter")
        return None
    language = sys.argv[1]
    advisories: Dict[str, Any] = {}
    for fun in (get_community_advisories,):
        fun(advisories, language)

    log_blocking("info", f"Creating file: {language}.json")
    with open(f"static/sca/{language}.json", "w") as outfile:
        json.dump(advisories, outfile, indent=2, sort_keys=True)


main()
