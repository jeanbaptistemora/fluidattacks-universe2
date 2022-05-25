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
import re
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from urllib3.util.url import (
    parse_url,
)

PATTERNS: List[Dict[str, Union[str, List[Dict[str, Any]]]]] = [
    {
        "name": ".csproj",
        "description": "visual studio c sharp project",
        "type": "file_extension",
    },
    {
        "name": ".vbproj",
        "description": "visual studio visual basic project",
        "type": "file_extension",
    },
    {
        "name": "pom.xml",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "description": "java maven project",
        "type": "specific_file",
    },
    {
        "name": "build.gradle",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "description": "java gradel project",
        "type": "specific_file",
    },
    {
        "name": "settings.gradle",
        "description": "java gradel project",
        "type": "specific_file",
    },
    {
        "name": "setup.cfg",
        "description": "python project",
        "type": "specific_file",
    },
    {
        "name": "pyproject.toml",
        "description": "python project",
        "type": "specific_file",
    },
    {
        "name": "requirements.txt",
        "description": "file of dependencies in python projects",
        "type": "specific_file",
    },
    {
        "name": "poetry.lock",
        "description": "python poetry project",
        "type": "specific_file",
    },
    {
        "name": "package.json",
        "description": "node npm project",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "type": "specific_file",
    },
    {
        "name": "yarn.lock",
        "description": "node yarn project",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "type": "specific_file",
    },
]


def evaluate_requirement(
    requirement: Dict[str, Any],
    current_directories: List[str],
    current_files: List[str],
) -> bool:
    if requirement.get("optional", False):
        return True
    if requirement["name"] == "directory":
        return all(
            required_directory in current_directories
            for required_directory in requirement["values"]
        )
    if requirement["name"] == "file":
        return all(
            required_file in current_files
            for required_file in requirement["values"]
        )
    return False


def file_match_expected_patterns(
    file: str,
    current_directories: List[str],
    current_files: List[str],
) -> Optional[Dict[str, Any]]:
    for config in PATTERNS:
        if (
            config["type"] == "file_extension"
            and re.match(f"(.?)*{config['name']}$", file) is not None
        ):
            # matches the pattern of a project configuration file
            return config

        if config["type"] == "specific_file" and config["name"] == file:
            # has the name of a configuration file
            if requires := config.get("requires"):
                requires = cast(List[Dict[str, Any]], requires)
                if all(
                    evaluate_requirement(
                        req, current_directories, current_files
                    )
                    for req in requires
                ):
                    return config
            else:
                return config

    return None


async def get_scopes_from_group(group: str, namespace: str) -> Set[str]:
    roots = await get_group_roots(group=group)
    return {
        environment_url
        for root in roots
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

    for parsed_url in {parse_url(url) for url in urls}:
        if parsed_url.port is None:
            if ((parsed_url.host, "443")) not in targets:
                targets.append((parsed_url.host, "443"))
        else:
            if ((parsed_url.host, str(parsed_url.port))) not in targets:
                targets.append((parsed_url.host, str(parsed_url.port)))
    targets.sort(key=lambda x: x[0])

    return targets


async def generate_config(
    *,
    group_name: str,
    namespace: str,
    checks: Tuple[str, ...],
    language: LocalesEnum = LocalesEnum.EN,
    exclude: Tuple[str, ...] = (),
    working_dir: str = ".",
    is_main: bool = True,
) -> SkimsConfig:
    create_session(os.environ["INTEGRATES_API_TOKEN"])

    scopes: Set[str] = set()
    urls: List[str] = []
    ssl_targets: List[Tuple[str, str]] = []
    if is_main:
        scopes = await get_scopes_from_group(group_name, namespace)
        urls = get_urls_from_scopes(scopes)
        ssl_targets = get_ssl_targets(urls)

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
            exclude=tuple(sorted(("glob(**/.git)", *exclude))),
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
