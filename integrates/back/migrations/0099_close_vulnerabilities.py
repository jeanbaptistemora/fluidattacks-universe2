# pylint: disable=invalid-name
"""
This migration aims to close related vulnerabilities

1st execution
Execution time: 2021-07-14 00:06:30-05
Finalization time: 2021-07-14 00:08:34-05

2nd execution
Execution time: 2021-07-14 22:03:20-05
Finalization time: 2021-07-14 22:05:47-05

3rd execution
Execution Time: 2021-07-26 19:50:35-05
Finalization Time: 2021-07-26 19:50:43-05
"""

from aioextensions import (
    collect,
    run,
)
from collections import (
    defaultdict,
)
import csv
from custom_types import (
    Finding,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from dynamodb.types import (
    GitRootItem,
    RootItem,
)
from itertools import (
    chain,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations.domain import (
    get_id_for_group,
)
from roots.dal import (
    get_root_vulns,
)
from roots.domain import (
    get_org_roots,
)
import time
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Set,
)
from urllib.parse import (
    unquote,
    urlparse,
)
from vulnerabilities.dal import (
    update,
)

# Constants
PROD: bool = True


# Types
class NickName(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    nickname: str
    root_url: str
    group_name: str


def get_findings_ids(*, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
    return list(
        {str(vulnerability["finding_id"]) for vulnerability in vulnerabilities}
    )


def format_root_url(*, root_url: str) -> str:
    return urlparse(root_url).path


def format_roots_url(*, roots_url: Set[str]) -> Set[str]:
    return {format_root_url(root_url=root_url) for root_url in roots_url}


def get_repo_nickname_roots(
    *,
    nicknames: Set[NickName],
) -> Dict[str, str]:
    repo_nickname: Dict[str, str] = defaultdict()
    for nickname in nicknames:
        repo_nickname[nickname.nickname] = format_root_url(
            root_url=nickname.root_url
        )

    return repo_nickname


def get_findings_ids_from_groups(
    *,
    groups_roots: Dict[str, Set[str]],
    findings: List[Dict[str, Finding]],
    vulnerabilities: List[Dict[str, Any]],
    nicknames: Set[NickName],
) -> Set[str]:
    repo_nickname: Dict[str, str] = get_repo_nickname_roots(
        nicknames=nicknames
    )

    return {
        finding["finding_id"]
        for vulnerability in vulnerabilities
        for finding in findings
        if repo_nickname[vulnerability["repo_nickname"]]
        in format_roots_url(
            roots_url=groups_roots[finding["group_name"].lower()]
        )
    }


async def close_vulnerabilities(
    *,
    vulnerabilities: List[Dict[str, Any]],
    findings_ids: Set[str],
    current_day: str,
    loaders: Dataloaders,
    nicknames: Set[NickName],
    groups_roots: Dict[str, Set[str]],
) -> None:
    await collect(
        [
            close_vulnerability(
                vulnerability=vulnerability,
                findings_ids=findings_ids,
                current_day=current_day,
                loaders=loaders,
                nicknames=nicknames,
                groups_roots=groups_roots,
            )
            for vulnerability in vulnerabilities
        ],
        workers=20,
    )


async def close_vulnerability(
    *,
    vulnerability: Dict[str, Any],
    findings_ids: Set[str],
    current_day: str,
    loaders: Dataloaders,
    nicknames: Set[NickName],
    groups_roots: Dict[str, Set[str]],
) -> None:
    finding_id: str = vulnerability["finding_id"]
    finding = await loaders.finding.load(finding_id)
    historic_state: List[Dict[str, str]] = vulnerability["historic_state"]
    repo_nickname: Dict[str, str] = get_repo_nickname_roots(
        nicknames=nicknames
    )

    if (
        finding_id not in findings_ids
        or historic_state[-1]["state"] != "open"
        or repo_nickname[vulnerability["repo_nickname"]]
        not in format_roots_url(
            roots_url=groups_roots[finding["group_name"].lower()]
        )
    ):
        return

    current_state = [
        {
            "analyst": str(historic_state[-1]["analyst"]),
            "date": current_day,
            "source": str(historic_state[-1]["source"]),
            "state": "closed",
        }
    ]
    data_to_update: Dict[str, Finding] = {
        "historic_state": [*historic_state, *current_state]
    }

    if PROD:
        print(
            "Updating vulnerabilities state",
            finding["group_name"],
            finding_id,
            vulnerability["UUID"],
            vulnerability["repo_nickname"],
            data_to_update,
        )
        await update(finding_id, str(vulnerability["UUID"]), data_to_update)


def get_nicknames(
    *,
    roots: List[RootItem],
    groups_roots: Dict[str, Set[str]],
    groups_nicknames: Dict[str, Set[str]],
    groups_names: Set[str],
) -> Set[NickName]:

    return {
        NickName(
            nickname=root.state.nickname,
            root_url=unquote(root.metadata.url),
            group_name=root.group_name,
        )
        for root in roots
        if isinstance(root, GitRootItem)
        and root.group_name.lower() in groups_names
        and root.state.nickname in groups_nicknames[root.group_name.lower()]
        and format_root_url(root_url=root.metadata.url)
        in format_roots_url(roots_url=groups_roots[root.group_name.lower()])
    }


async def get_vulnerabilities(
    *, nicknames: Set[NickName]
) -> List[Dict[str, Any]]:
    nicknames_vulnerabilities = await collect(
        [get_root_vulns(nickname=nickname.nickname) for nickname in nicknames],
        workers=20,
    )
    return list(chain.from_iterable(nicknames_vulnerabilities))


async def get_organizations_id(*, groups_name: Set[str]) -> Set[str]:
    return set(
        await collect(
            [get_id_for_group(group_name) for group_name in groups_name]
        )
    )


async def main() -> None:
    groups_name: List[str] = []
    roots_url: List[str] = []
    groups_roots: Dict[str, Set[str]] = defaultdict(set)
    groups_nicknames: Dict[str, Set[str]] = defaultdict(set)
    with open("roots.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            groups_name.append(row["Grupo"].lower())
            roots_url.append(unquote(row["GIT"]))
            groups_roots[row["Grupo"].lower()].add(unquote(row["GIT"]))
            groups_nicknames[row["Grupo"].lower()].add(row["Nickname"])

    current_day = datetime_utils.get_now_as_str()
    organizations_ids: Set[str] = await get_organizations_id(
        groups_name=set(groups_name)
    )

    loaders: Dataloaders = get_new_context()
    roots: List[RootItem] = list(
        chain.from_iterable(
            await collect(
                [
                    get_org_roots(loaders=loaders, org_id=org_id)
                    for org_id in organizations_ids
                ]
            )
        )
    )

    nicknames: Set[NickName] = get_nicknames(
        roots=roots,
        groups_roots=groups_roots,
        groups_names=set(groups_name),
        groups_nicknames=groups_nicknames,
    )

    vulnerabilities: List[Dict[str, Any]] = await get_vulnerabilities(
        nicknames=nicknames
    )

    findings: List[Dict[str, Finding]] = await loaders.finding.load_many(
        get_findings_ids(vulnerabilities=vulnerabilities)
    )

    finding_ids_of_vulnerabilities_to_close: Set[
        str
    ] = get_findings_ids_from_groups(
        groups_roots=groups_roots,
        findings=findings,
        vulnerabilities=vulnerabilities,
        nicknames=nicknames,
    )
    await close_vulnerabilities(
        vulnerabilities=vulnerabilities,
        findings_ids=finding_ids_of_vulnerabilities_to_close,
        current_day=current_day,
        loaders=loaders,
        nicknames=nicknames,
        groups_roots=groups_roots,
    )


if __name__ == "__main__":
    execution_time = time.strftime("Execution Time: %Y-%m-%d %H:%M:%S%Z")
    run(main())
    finalization_time = time.strftime("Finalization Time: %Y-%m-%d %H:%M:%S%Z")
    print(f"{execution_time}\n{finalization_time}")
