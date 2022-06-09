import json
from repositories.community_advisories import (
    get_remote_advisories,
)
import sys
from typing import (
    Any,
    Dict,
)
from utils.logs import (
    log_blocking,
)


def main() -> None:
    language = sys.argv[1]
    community_advisories_vulns: Dict[str, Any] = get_remote_advisories(
        language
    )

    log_blocking("info", f"Creating file: {language}.json")
    with open(f"{language}.json", "w") as outfile:
        json.dump(
            community_advisories_vulns, outfile, indent=2, sort_keys=True
        )
