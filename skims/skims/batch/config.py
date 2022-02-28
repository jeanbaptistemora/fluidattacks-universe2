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


def get_urls_from_scopes(scopes: Set[str]) -> List[str]:
    urls: Set[str] = set()
    urls.update(scopes)

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
    urls: List[str] = get_urls_from_scopes(scopes)
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
