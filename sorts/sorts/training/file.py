from integrates.dal import (
    get_toe_lines_sorts,
)
from integrates.domain import (
    get_vulnerable_files,
    get_vulnerable_lines,
)
from integrates.typing import (
    ToeLines,
    VulnerabilityKindEnum,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
)
import random
from sorts.features.file import (
    extract_features,
)
from sorts.utils.logs import (
    log,
)
from sorts.utils.repositories import (
    get_bad_repos,
)
from sorts.utils.static import (
    read_allowed_names,
)
import time
from typing import (
    List,
    Set,
)

# Constants
FILE_MAX_RETRIES: int = 15


def build_training_df(group: str, fusion_path: str) -> DataFrame:
    """Creates a training DataFrame with vulnerable and safe files"""
    ignore_repos: List[str] = get_bad_repos(fusion_path)
    vuln_files: List[str] = get_vulnerable_files(group, ignore_repos)
    safe_files = get_safe_files(vuln_files, ignore_repos, fusion_path)

    training_df = pd.concat(
        [
            pd.DataFrame(
                map(lambda x: (x, 1), vuln_files), columns=["file", "is_vuln"]
            ),
            pd.DataFrame(
                map(lambda x: (x, 0), safe_files), columns=["file", "is_vuln"]
            ),
        ]
    )
    training_df["repo"] = training_df["file"].apply(
        lambda filename: os.path.join(
            fusion_path, filename.split(os.path.sep)[0]
        )
    )
    training_df.reset_index(drop=True, inplace=True)
    return training_df


def get_subscription_file_metadata(subscription_path: str) -> bool:
    """Creates a CSV with the file features from the subscription"""
    success: bool = True
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, "fusion")
    if os.path.exists(fusion_path):
        training_df: DataFrame = build_training_df(group, fusion_path)
        if training_df.empty:
            success = False
            log(
                "warning",
                'Group %s does not have any vulnerabilities of type "lines"',
                group,
            )
        else:
            success = extract_features(training_df)
            if success:
                csv_name: str = f"{group}_files_features.csv"
                training_df.to_csv(csv_name, index=False)
                log("info", "Features extracted succesfully to %s", csv_name)
    else:
        success = False
        log("error", "Fusion folder for group %s does not exist", group)
    return success


def get_verified_safe_files(group: str) -> List[str]:
    """Gets the filenames of a group
    that haven't had any vulnerabilities ever since they were created
    and have been completely attacked"""
    group_toe_lines: List[ToeLines] = get_toe_lines_sorts(
        group  # type: ignore
    )

    attacked_files = [
        f"{file.root_nickname}/{file.filename}"
        for file in group_toe_lines
        if file.attacked_lines == file.loc
    ]

    all_vulnerable_files = {
        vuln.where
        for vuln in get_vulnerable_lines(group)
        if vuln.kind.value == VulnerabilityKindEnum.LINES.value
    }

    verified_safe_files = [
        filename
        for filename in attacked_files
        if filename not in all_vulnerable_files
    ]

    return verified_safe_files


def get_safe_files(
    vuln_files: List[str], ignore_repos: List[str], fusion_path: str
) -> List[str]:
    """Fetches random files that do not have any vulnerability reported"""
    timer: float = time.time()
    safe_files: Set[str] = set()
    retries: int = 0

    verified_safe_files = get_verified_safe_files(fusion_path.split("/")[-2])
    extensions, composites = read_allowed_names()
    allowed_repos: List[str] = [
        repo for repo in os.listdir(fusion_path) if repo not in ignore_repos
    ]
    if allowed_repos:
        while len(safe_files) < len(vuln_files):
            if retries > FILE_MAX_RETRIES:
                log(
                    "warning",
                    "Could not find enough safe files to balance the "
                    "vulnerable ones",
                )
                break

            if verified_safe_files:
                file_name: str = random.choice(verified_safe_files)
                file_extension: str = (
                    os.path.splitext(file_name)[1].strip(".").lower()
                )
                if (
                    file_name not in vuln_files
                    and file_name not in safe_files
                    and (
                        file_name in composites or file_extension in extensions
                    )
                ):
                    safe_files.add(file_name)
                    retries = 0
            retries += 1
        log(
            "info",
            "Safe files extracted after %.2f secods",
            time.time() - timer,
        )
    return sorted(safe_files)
