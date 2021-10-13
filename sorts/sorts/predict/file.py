from concurrent.futures import (
    ThreadPoolExecutor,
)
import csv
import os
import pandas as pd
from pandas import (
    DataFrame,
)
from sorts.features.file import (
    extract_features,
)
from sorts.integrates.dal import (
    get_toe_lines_sorts,
    ToeLines,
    update_toe_lines_sorts,
)
from sorts.utils.logs import (
    log,
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
) -> List[ToeLines]:
    toes_to_update: List[ToeLines] = []
    pred_range_lim = 3
    for predicted_file in predicted_files:
        predicted_file_filename = predicted_file["file"]
        predicted_file_prob = int(float(predicted_file["prob_vuln"]))
        for toe_lines in group_toe_lines:
            if (
                toe_lines.filename == predicted_file_filename
                and predicted_file_prob
                not in range(
                    toe_lines.sorts_risk_level - pred_range_lim,
                    toe_lines.sorts_risk_level + pred_range_lim,
                )
            ):
                toes_to_update.append(
                    ToeLines(
                        filename=predicted_file_filename,
                        sorts_risk_level=predicted_file_prob,
                    )
                )
                break

    return toes_to_update


def update_integrates_toes(group_name: str, csv_name: str) -> None:
    group_toe_lines: List[ToeLines] = get_toe_lines_sorts(group_name)
    with open(csv_name, "r", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file)
        toes_to_update = get_toes_to_update(group_toe_lines, reader)
        with ThreadPoolExecutor(max_workers=8) as executor:
            for toe_lines in toes_to_update:
                executor.submit(
                    update_toe_lines_sorts,
                    group_name,
                    toe_lines.filename,
                    toe_lines.sorts_risk_level,
                )
        log("info", f"ToeLines's sortsFileRisk for {group_name} updated")


def prioritize(subscription_path: str) -> bool:
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
            update_integrates_toes(group, csv_name)
            display_results(csv_name)
    else:
        log(
            "error",
            "There is no 'fusion' folder in the path %s",
            subscription_path,
        )

    return success
