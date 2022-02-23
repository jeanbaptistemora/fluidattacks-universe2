import csv
from integrates.dal import (
    get_group_roots,
)
from integrates.graphql import (
    create_session,
)
from model.core_model import (
    FindingEnum,
    LocalesEnum,
    SkimsAPKConfig,
    SkimsConfig,
    SkimsHttpConfig,
    SkimsPathConfig,
    SkimsSslConfig,
    SkimsSslTarget,
)
from operator import (
    itemgetter,
)
import os
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


async def generate_config(
    *,
    group_name: str,
    namespace: str,
    checks: Tuple[str, ...],
    language: LocalesEnum = LocalesEnum.EN,
    working_dir: str = ".",
) -> SkimsConfig:
    create_session(os.environ["INTEGRATES_API_TOKEN"])

    scopes: Set[str] = await get_scopes_from_group(group_name, namespace)
    components: List[str] = get_components_from_group(group_name)
    urls: List[str] = get_urls_from_scopes(scopes, components)
    ssl_targets: List[Tuple[str, str]] = get_ssl_targets(urls)

    return SkimsConfig(
        apk=SkimsAPKConfig(
            exclude=(),
            include=("glob(**/*.apk)",),
        ),
        checks=(
            {
                FindingEnum[finding]
                for finding in checks
                if finding in FindingEnum.__members__
            }
            if checks
            else set(FindingEnum)
        ),
        group=group_name,
        http=SkimsHttpConfig(
            include=tuple(urls),
        ),
        language=language,
        namespace=namespace,
        output=os.path.abspath("result.csv"),
        path=SkimsPathConfig(
            include=(".",),
            exclude=("glob(**/.git)",),
            lib_path=True,
            lib_root=True,
        ),
        ssl=SkimsSslConfig(
            include=tuple(
                SkimsSslTarget(host=host, port=int(port))
                for host, port in ssl_targets
            )
        ),
        start_dir=os.getcwd(),
        working_dir=os.path.abspath(working_dir),
    )
