from botocore.exceptions import (
    ClientError,
)
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
    S3_BUCKET,
)
from sorts.features.file import (
    extract_features,
)
from sorts.integrates.dal import (
    get_toe_lines_sorts,
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
import tempfile
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


def remove_toe_lines(
    toe_lines: ToeLines, toe_lines_list: List[ToeLines]
) -> None:
    try:
        toe_lines_list.remove(toe_lines)
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
                        sorts_risk_level_date=toe_lines.sorts_risk_level_date,
                    )
                )
                remove_toe_lines(toe_lines, skipped_toes)
                break
    for toe_lines in skipped_toes:
        if toe_lines.sorts_risk_level_date == "1970-01-01T00:00:00+00:00":
            remove_toe_lines(toe_lines, skipped_toes)

    return toes_to_update, skipped_toes


def update_integrates_toes(
    group_name: str, csv_name: str, current_date: str
) -> bool:
    success: bool = False
    group_toe_lines: List[ToeLines] = get_toe_lines_sorts(
        group_name  # type: ignore
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_file: str = os.path.join(tmp_dir, csv_name)
        try:
            S3_BUCKET.Object(
                f"sorts-execution-results/{csv_name}"
            ).download_file(local_file)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                log(
                    "error",
                    f"There is no {group_name} file in S3",
                )
                return success

        with open(local_file, "r", encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)
            toes_to_update, skipped_toes = get_toes_to_update(
                group_toe_lines, reader
            )
            with ThreadPoolExecutor(max_workers=8) as executor:
                for skipped_toe in skipped_toes:
                    executor.submit(
                        update_toe_lines_sorts,
                        group_name,
                        skipped_toe.root_nickname,
                        skipped_toe.filename,
                        "1970-01-01",
                    )
            with ThreadPoolExecutor(max_workers=8) as executor:
                for toe_lines in toes_to_update:
                    executor.submit(
                        update_toe_lines_sorts,
                        group_name,
                        toe_lines.root_nickname,
                        toe_lines.filename,
                        current_date,
                        toe_lines.sorts_risk_level,  # type: ignore
                    )
            log("info", f"ToeLines's sortsFileRisk for {group_name} updated")
            success = True

    return success


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
            S3_BUCKET.Object(
                f"sorts-execution-results/{csv_name}"
            ).upload_file(csv_name)
            display_results(csv_name)
    else:
        log(
            "error",
            "There is no 'fusion' folder in the path %s",
            subscription_path,
        )

    return success
