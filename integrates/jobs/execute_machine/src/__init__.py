# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
import argparse
import json
import os
import re
import subprocess
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
import uuid
import yaml  # type: ignore

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


def get_repo_head_hash(path: str) -> str:
    with subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path) as executor:
        _stdout, _ = executor.communicate()
        return _stdout.decode()


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


def is_additional_path(dirs: List[str], files: List[str]) -> bool:
    for file in files:
        match_config = file_match_expected_patterns(file, dirs, files)
        if match_config is not None:
            return True

    return False


def generate_configs(
    *,
    group_name: str,
    namespace: str,
    checks: Tuple[str, ...],
    language: str = "EN",
    working_dir: str = ".",
) -> List[Dict[str, Any]]:
    additional_paths: List[str] = []
    all_configs: List[Dict[str, Any]] = []
    for current_dir, dirs, files in os.walk(working_dir):
        if current_dir == working_dir:
            continue
        if is_additional_path(dirs, files):
            additional_paths.append(current_dir.replace(f"{working_dir}/", ""))
    commit = ""
    all_configs = [
        generate_config(
            group_name=group_name,
            git_root=namespace,
            checks=checks,
            language=language,
            working_dir=working_dir,
            exclude=tuple(additional_paths),
            commit=commit,
        ),
        *(
            generate_config(
                group_name=group_name,
                git_root=namespace,
                checks=checks,
                language=language,
                working_dir=working_dir,
                include=(path,),
                commit=commit,
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
    ]

    return all_configs


def generate_config(
    *,
    group_name: str,
    git_root: str,
    checks: Tuple[str, ...],
    commit: str,
    language: str = "EN",
    include: Tuple[str, ...] = (),
    exclude: Tuple[str, ...] = (),
    working_dir: str = ".",
) -> Dict[str, Any]:
    execution_id = (
        f"{group_name}"
        f'_{os.environ.get("AWS_BATCH_JOB_ID", uuid.uuid4().hex)}'
        f"_{git_root}"
        f"_{uuid.uuid4().hex[:8]}"
    )
    return {
        "apk": {
            "exclude": [],
            "include": ["glob(**/*.apk)"],
        },
        "checks": list(checks),
        "commit": commit,
        "dast": None,
        "language": language,
        "namespace": git_root,
        "output": {
            "file_path": os.path.abspath(
                f"{working_dir}/execution_results/{execution_id}.sarif"
            ),
            "format": "SARIF",
        },
        "execution_id": execution_id,
        "path": {
            "include": include if include else ["."],
            "exclude": list(
                sorted(
                    (
                        "glob(**/.git)",
                        *exclude,
                    )
                )
            ),
            "lib_path": True,
            "lib_root": True,
        },
        "working_dir": os.path.abspath(working_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute machine for a root")
    parser.add_argument("--group-name", type=str, required=True)
    parser.add_argument(
        "--language",
        type=str,
        required=False,
        default="EN",
        choices=["EN", "ES"],
    )
    parser.add_argument("--root-nickname", type=str, required=True)
    parser.add_argument("--checks", type=str, required=True)
    parser.add_argument("--working-dir", type=str, required=True, default=".")
    args = parser.parse_args()

    configs = generate_configs(
        group_name=args.group_name,
        namespace=args.root_nickname,
        checks=json.loads(args.checks),
        language=args.language,
        working_dir=args.working_dir,
    )
    os.makedirs(f"{args.working_dir}/execution_configs", exist_ok=True)
    os.makedirs(f"{args.working_dir}/execution_results", exist_ok=True)
    print(os.getcwd())
    print(len(configs))
    for config in configs:
        with open(
            (
                f"{args.working_dir}/execution_configs"
                f"/{config['execution_id']}.yaml"
            ),
            "w",
            encoding="utf-8",
        ) as handler:
            yaml.safe_dump(config, handler)


if __name__ == "__main__":
    main()
