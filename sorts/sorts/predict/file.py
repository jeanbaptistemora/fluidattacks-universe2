from concurrent.futures import (
    ThreadPoolExecutor,
)
import csv
from integrates.typing import (
    ToeLines,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
)
from sorts.constants import (
    FERNET,
)
from sorts.features.file import (
    extract_features,
)
from sorts.integrates.dal import (
    get_toe_lines_sorts,
    RateLimitedWorker,
    update_toe_lines_sorts,
)
from sorts.utils.logs import (
    log,
    log_exception,
)
from sorts.utils.predict import (
    display_results,
    predict_vuln_prob,
)
from sorts.utils.repositories import (
    get_repository_files,
)
from sorts.utils.static import (
    get_extensions_list,
    read_allowed_names,
)
from typing import (
    List,
    Tuple,
)


def get_subscription_files_df(fusion_path: str) -> DataFrame:
    """Builds the basic DF with all the files from every repository"""
    files: List[str] = []
    extensions, composites = read_allowed_names()
    for repo in os.listdir(fusion_path):
        repo_files = get_repository_files(os.path.join(fusion_path, repo))
        allowed_files = list(
            filter(
                lambda x: (
                    x in composites or x.split(".")[-1].lower() in extensions
                ),
                repo_files,
            )
        )
        if allowed_files:
            files.extend(allowed_files)
    files_df: DataFrame = pd.DataFrame(files, columns=["file"])
    files_df["repo"] = files_df["file"].apply(
        lambda x: os.path.join(fusion_path, x.split("/")[0])
    )
    return files_df


def get_toes_to_update(
    group_toe_lines: List[ToeLines], predicted_files: csv.DictReader
) -> Tuple[List[ToeLines], List[ToeLines]]:
    toes_to_update: List[ToeLines] = []
    skipped_toes = group_toe_lines.copy()
    for predicted_file in predicted_files:
        decryped_filepath = FERNET.decrypt(
            predicted_file["file"].encode()
        ).decode()
        predicted_nickname, predicted_file_filename = decryped_filepath.split(
            "/", 1
        )
        predicted_file_prob = int(float(predicted_file["prob_vuln"]))
        for toe_lines in group_toe_lines:
            if (
                toe_lines.filename == predicted_file_filename
                and toe_lines.root_nickname == predicted_nickname
            ):
                toes_to_update.append(
                    ToeLines(
                        attacked_lines=toe_lines.attacked_lines,
                        filename=predicted_file_filename,
                        loc=toe_lines.loc,
                        root_nickname=predicted_nickname,
                        sorts_risk_level=predicted_file_prob,  # type: ignore
                    )
                )
                try:
                    skipped_toes.remove(toe_lines)
                except ValueError as exc:
                    log_exception(
                        "warning",
                        exc,
                        message=(
                            "Couldn't remove file "
                            f"{toe_lines.root_nickname}/{toe_lines.filename} "
                            "from skipped ToEs"
                        ),
                    )
                break

    return toes_to_update, skipped_toes


def update_integrates_toes(
    group_name: str, csv_name: str, current_date: str
) -> None:
    group_toe_lines: List[ToeLines] = get_toe_lines_sorts(
        group_name  # type: ignore
    )
    with open(csv_name, "r", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file)
        toes_to_update, skipped_toes = get_toes_to_update(
            group_toe_lines, reader
        )
        skipped_toes_worker = RateLimitedWorker()
        with ThreadPoolExecutor(max_workers=8) as executor:
            for skipped_toe in skipped_toes:
                executor.submit(
                    update_toe_lines_sorts,
                    group_name,
                    skipped_toe.root_nickname,
                    skipped_toe.filename,
                    "1970-01-01",
                    skipped_toes_worker,
                )
        toes_to_update_worker = RateLimitedWorker()
        with ThreadPoolExecutor(max_workers=8) as executor:
            for toe_lines in toes_to_update:
                executor.submit(
                    update_toe_lines_sorts,
                    group_name,
                    toe_lines.root_nickname,
                    toe_lines.filename,
                    current_date,
                    toes_to_update_worker,
                    toe_lines.sorts_risk_level,  # type: ignore
                )
        log("info", f"ToeLines's sortsFileRisk for {group_name} updated")


def prioritize(subscription_path: str, current_date: str) -> bool:
    """Prioritizes files according to the chance of finding a vulnerability"""
    success: bool = False
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, "fusion")
    if os.path.exists(fusion_path):
        predict_df: DataFrame = get_subscription_files_df(fusion_path)
        success = extract_features(predict_df)
        if success:
            extensions: List[str] = get_extensions_list()
            num_bits: int = len(extensions).bit_length()
            csv_name: str = f"{group}_sorts_results_file.csv"
            predict_vuln_prob(
                predict_df,
                [f"extension_{num}" for num in range(num_bits + 1)],
                csv_name,
            )
            update_integrates_toes(group, csv_name, current_date)
            display_results(csv_name)
    else:
        log(
            "error",
            "There is no 'fusion' folder in the path %s",
            subscription_path,
        )

    return success
