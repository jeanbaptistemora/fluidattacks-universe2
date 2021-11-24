from aioextensions import (
    run,
)
import argparse
import csv
from integrates.dal import (
    get_group_roots,
)
from integrates.graphql import (
    create_session,
)
from operator import (
    itemgetter,
)
import os
from ruamel.yaml import (
    safe_dump,
)
from typing import (
    List,
    Set,
    Tuple,
)
from urllib.parse import (
    urlparse,
)


async def get_scopes_from_group(group: str, namespace: str) -> Set[str]:
    return {
        environment_url
        for root in await get_group_roots(group=group)
        for environment_url in root.environment_urls
        if root.nickname == namespace
    }


def get_components_from_group(group: str) -> List[str]:
    path: str = f"groups/{group}/toe/inputs.csv"

    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8") as inputs_handle:
        components = list(
            map(
                itemgetter("component"),
                csv.DictReader(inputs_handle),
            )
        )
    return components


def get_urls_from_scopes(scopes: Set[str], components: List[str]) -> List[str]:
    urls: Set[str] = set()
    urls.update(scopes)

    for scope in scopes:
        scope_c = urlparse(scope)

        for component in components:
            component_c = urlparse(f"schema://{component}")

            if (
                scope_c.netloc == component_c.netloc
                and component_c.path.startswith(scope_c.path)
            ):
                urls.add(f"{scope_c.scheme}://{component}")

    for scope in scopes:
        # FP: switch the type of protocol
        for from_, to_ in (
            ("http://", "https://"),  # NOSONAR
            ("https://", "http://"),  # NOSONAR
        ):
            if scope.startswith(from_):
                urls.add(scope.replace(from_, to_, 1))

    return sorted(urls)


def get_ssl_targets(urls: List[str]) -> List[Tuple[str, str]]:
    targets: List[Tuple[str, str]] = []

    for netloc in {urlparse(url).netloc for url in urls}:
        if ":" not in netloc:
            targets.append((netloc, "443"))
        else:
            host, port = netloc.rsplit(":", maxsplit=1)
            targets.append((host, port))

    return targets


async def main() -> None:
    parser = argparse.ArgumentParser()
    for arg in ("group", "language", "namespace", "out"):
        parser.add_argument(f"--{arg}", required=True)

    parser.add_argument("--check", nargs="+", required=True)
    args = parser.parse_args()

    create_session(os.environ["INTEGRATES_API_TOKEN"])

    scopes: Set[str] = await get_scopes_from_group(args.group, args.namespace)
    components: List[str] = get_components_from_group(args.group)
    urls: List[str] = get_urls_from_scopes(scopes, components)
    ssl_targets: List[Tuple[str, str]] = get_ssl_targets(urls)

    data: str = safe_dump(
        dict(
            apk=dict(
                include=sorted(["glob(**/*.apk)"]),
            ),
            checks=args.check,
            language=args.language,
            namespace=args.namespace,
            http=dict(
                include=urls,
            ),
            path=dict(
                include=sorted(["."]),
                exclude=sorted(["glob(**/.git)"]),
            ),
            ssl=dict(
                include=[
                    dict(host=host, port=int(port))
                    for host, port in ssl_targets
                ],
            ),
            working_dir=f"groups/{args.group}/fusion/{args.namespace}",
        ),
        default_flow_style=False,
    )

    print(data)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(data)


if __name__ == "__main__":
    run(main())
