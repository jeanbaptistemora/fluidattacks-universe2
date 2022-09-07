# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import aioboto3
from aioextensions import (
    collect,
)
from config import (
    dump_to_yaml,
)
from contextlib import (
    suppress,
)
from integrates.dal import (
    get_group_roots,
    ResultGetGroupRoots,
)
from integrates.graphql import (
    create_session,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    FindingEnum,
    LocalesEnum,
    SkimsAPKConfig,
    SkimsConfig,
    SkimsDastConfig,
    SkimsHttpConfig,
    SkimsPathConfig,
    SkimsSslConfig,
    SkimsSslTarget,
)
import os
import re
import tempfile
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
from urllib3 import (
    exceptions,
)
from urllib3.util.url import (
    parse_url,
    Url,
)
from utils.repositories import (
    get_repo_head_hash,
)
import uuid

PATTERNS: List[Dict[str, Union[str, List[Dict[str, Any]]]]] = [
    {
        "name": ".csproj",
        "description": "visual studio c sharp project",
        "type": "file_extension",
    },
    {
        "name": "App.Config",
        "description": "C Sharp module",
        "type": "file_extension",
    },
    {
        "name": ".sln",
        "description": "visual studio c sharp set of projects",
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
            {"name": "directory", "values": ["src"], "optional": True}
        ],
        "description": "java maven project",
        "type": "specific_file",
    },
    {
        "name": "build.xml",
        "description": "Apache ant build",
        "type": "specific_file",
    },
    {
        "name": "build.gradle",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": True}
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
        "name": "setup.py",
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
    {
        "name": "main.tf",
        "description": "terraform infra",
        "type": "specific_file",
    },
    {
        "name": "variables.tf",
        "description": (
            "terraform infra, main can not be present, this can be a module"
        ),
        "type": "specific_file",
    },
    {
        "name": "Podfile",
        "description": ("swift project"),
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
    parsed_urls: Set[Url] = set()
    for url in urls:
        with suppress(ValueError, exceptions.HTTPError):
            parsed_urls = {*parsed_urls, parse_url(url)}
    for parsed_url in parsed_urls:
        if parsed_url.port is None:
            if (parsed_url.host, "443") not in targets:
                targets.append((parsed_url.host, "443"))
        else:
            if (parsed_url.host, str(parsed_url.port)) not in targets:
                targets.append((parsed_url.host, str(parsed_url.port)))
    targets.sort(key=lambda x: x[0])

    return targets


def is_additional_path(dirs: List[str], files: List[str]) -> bool:
    for file in files:
        match_config = file_match_expected_patterns(file, dirs, files)
        if match_config is not None:
            return True

    return False


async def generate_configs(
    *,
    group_name: str,
    namespace: str,
    checks: Tuple[str, ...],
    language: LocalesEnum = LocalesEnum.EN,
    working_dir: str = ".",
) -> List[SkimsConfig]:
    additional_paths: List[str] = []
    all_configs: List[SkimsConfig] = []
    for current_dir, dirs, files in os.walk(working_dir):
        if current_dir == working_dir:
            continue
        if is_additional_path(dirs, files):
            additional_paths.append(current_dir.replace(f"{working_dir}/", ""))
    git_root = next(
        (
            root
            for root in (await get_group_roots(group=group_name))
            if root.nickname == namespace
        ),
        None,
    )
    if not git_root:
        return all_configs

    all_configs = await collect(
        (
            generate_config(
                group_name=group_name,
                git_root=git_root,
                checks=checks,
                language=language,
                working_dir=working_dir,
                is_main=True,
                exclude=tuple(additional_paths),
            ),
            *(
                generate_config(
                    group_name=group_name,
                    git_root=git_root,
                    checks=checks,
                    language=language,
                    working_dir=working_dir,
                    is_main=False,
                    include=(path,),
                    exclude=tuple(
                        {
                            (
                                _path
                                if not path.startswith(f"{_path}/")
                                else f"{_path}/*"
                            )
                            for _path in additional_paths
                            if _path != path
                        }
                    ),
                )
                for path in additional_paths
            ),
        )
    )
    return all_configs


async def generate_config(
    *,
    group_name: str,
    git_root: ResultGetGroupRoots,
    checks: Tuple[str, ...],
    language: LocalesEnum = LocalesEnum.EN,
    include: Tuple[str, ...] = (),
    exclude: Tuple[str, ...] = (),
    working_dir: str = ".",
    is_main: bool = True,
) -> SkimsConfig:
    scopes: Set[str] = set()
    urls: List[str] = []
    ssl_targets: List[Tuple[str, str]] = []
    dast_config: Optional[SkimsDastConfig] = None
    namespace = git_root.nickname
    if is_main:
        create_session(os.environ["INTEGRATES_API_TOKEN"])
        scopes = set(git_root.environment_urls)
        secrets = {
            secret["key"]: secret["value"]
            for environment_url in git_root.git_environment_urls
            if environment_url["urlType"] == "CLOUD"  # type: ignore
            for secret in environment_url["secrets"]
        }

        dast_config = SkimsDastConfig(
            aws_credentials=(
                [
                    AwsCredentials(
                        access_key_id=secrets["AWS_ACCESS_KEY_ID"],
                        secret_access_key=secrets["AWS_SECRET_ACCESS_KEY"],
                    )
                ]
                if (
                    "AWS_ACCESS_KEY_ID" in secrets
                    and "AWS_SECRET_ACCESS_KEY" in secrets
                )
                else []
            ),
            http=SkimsHttpConfig(
                include=tuple(urls),
            ),
            ssl=SkimsSslConfig(
                include=tuple(
                    SkimsSslTarget(host=host, port=int(port))
                    for host, port in ssl_targets
                )
            ),
        )
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
        commit=get_repo_head_hash(working_dir),
        dast=dast_config,
        group=group_name,
        language=language,
        namespace=namespace,
        output=None,
        path=SkimsPathConfig(
            include=include if include else (".",),
            exclude=tuple(
                sorted(
                    (
                        "glob(**/.git)",
                        *exclude,
                        *(git_root.gitignore if git_root else []),
                    )
                )
            ),
            lib_path=True,
            lib_root=True,
        ),
        start_dir=os.getcwd(),
        working_dir=os.path.abspath(working_dir),
        execution_id=(
            f"{group_name}"
            f'_{os.environ.get("AWS_BATCH_JOB_ID", uuid.uuid4().hex)}'
            f"_{namespace}"
            f"_{uuid.uuid4().hex[:8]}"
        ),
    )


async def upload_config(config: core_model.SkimsConfig) -> bool:
    file_content = dump_to_yaml(config)
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = f"{tmp_dir}/{config.execution_id}.yaml"
        with open(file_path, "w", encoding="utf-8") as handler:
            handler.write(file_content)
        with open(file_path, "rb") as reader:
            session = aioboto3.Session()
            async with session.resource("s3") as s3_resource:
                bucket = await s3_resource.Bucket("skims.data")
                await bucket.upload_fileobj(
                    reader,
                    f"configs/{config.execution_id}.yaml",
                )
                return True
