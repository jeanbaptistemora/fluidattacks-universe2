import csv
from joblib import (
    dump,
)
import numpy as np
from numpy import (
    ndarray,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
)
from sklearn.model_selection import (
    cross_validate,
    learning_curve,
)
from sorts.typings import (
    Model as ModelType,
)
import tempfile
import time
from training.constants import (
    FEATURES_DICTS,
    S3_BUCKET,
)
from training.evaluate_results import (
    get_best_model_name,
)
from training.redshift import (
    db as redshift,
)
from typing import (
    Dict,
    List,
    Tuple,
)


def is_overfit(train_results: ndarray, test_results: ndarray) -> float:
    """Calculate how much the model got biased by the training data"""
    train_results_means: ndarray = train_results.mean(axis=1)
    test_results_means: ndarray = test_results.mean(axis=1)
    perc_diff: ndarray = (
        train_results_means - test_results_means
    ) / train_results_means
    row: int = 0
    tolerance: float = 0.002
    goal: int = 4
    for i in range(len(perc_diff) - 1):
        progress: float = abs(perc_diff[i + 1] - perc_diff[i])
        if progress < tolerance:
            row += 1
        else:
            row = 0
        if row == goal:
            min_overfit: ndarray = perc_diff[i - row - 1 : i]
            return float(min_overfit.mean())

    return float(perc_diff.mean())


def get_model_performance_metrics(
    model: ModelType, features: DataFrame, labels: DataFrame
) -> Tuple[float, float, float, float]:
    """Get performance metrics to compare different models"""
    scores = cross_validate(
        model,
        features,
        labels,
        scoring=["precision", "recall", "f1"],
        n_jobs=-1,
    )
    _, train_results, test_results = learning_curve(
        model,
        features,
        labels,
        scoring="f1",
        train_sizes=np.linspace(0.1, 1, 30),
        n_jobs=-1,
        random_state=42,
    )

    return (
        scores["test_precision"].mean() * 100,
        scores["test_recall"].mean() * 100,
        scores["test_f1"].mean() * 100,
        is_overfit(train_results, test_results) * 100,
    )


def split_training_data(
    training_df: DataFrame, feature_list: Tuple[str, ...]
) -> Tuple[DataFrame, DataFrame]:
    """Read the training data in two DataFrames for training purposes"""
    # Separate the labels from the features in the training data
    filtered_df = pd.concat(
        [
            # Include labels
            training_df.iloc[:, 0],
            # Include features
            training_df.loc[:, feature_list],
            # Include all extensions
            training_df.loc[
                :, training_df.columns.str.startswith("extension_")
            ],
        ],
        axis=1,
    )
    filtered_df.dropna(inplace=True)

    return filtered_df.iloc[:, 1:], filtered_df.iloc[:, 0]


def get_previous_training_results(results_filename: str) -> List[List[str]]:
    previous_results: List[List[str]] = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_file: str = os.path.join(tmp_dir, results_filename)
        remote_file: str = f"training-output/results/{results_filename}"
        S3_BUCKET.Object(remote_file).download_file(local_file)
        with open(local_file, "r", encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            previous_results.extend(csv_reader)

    return previous_results


def get_current_model_features() -> Tuple[str, ...]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, "best_model.txt")
        best_model: str = get_best_model_name(model_name_file)
        inv_features_dict: Dict[str, str] = {
            value: key for key, value in FEATURES_DICTS.items()
        }

        return tuple(
            inv_features_dict[key.upper()]
            for key in best_model.split("-")[2:]
            if len(key) == 2
        )


def load_training_data(training_dir: str) -> DataFrame:
    """Load a DataFrame with the training data in CSV format stored in S3"""
    input_files: List[str] = [
        os.path.join(training_dir, file) for file in os.listdir(training_dir)
    ]
    raw_data: List[DataFrame] = [
        pd.read_csv(file, engine="python") for file in input_files
    ]

    return pd.concat(raw_data)


def update_results_csv(filename: str, results: List[List[str]]) -> None:
    with open(filename, "w", newline="", encoding="utf8") as results_file:
        csv_writer = csv.writer(results_file)
        csv_writer.writerows(results)
    S3_BUCKET.Object(f"training-output/results/{filename}").upload_file(
        filename
    )


def set_sagemaker_extra_envs(extra_sm_envs: str) -> None:
    envs = {
        env_key.split("=")[0]: env_key.split("=")[1]
        for env_key in extra_sm_envs.split(",")
    }
    for env_key, value in envs.items():
        os.environ[env_key] = value


def save_model_to_s3(model: ModelType, model_name: str) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_file: str = os.path.join(tmp_dir, f"{model_name}.joblib")
        dump(model, local_file)
        S3_BUCKET.Object(f"training-output/{model_name}.joblib").upload_file(
            local_file
        )


def train_combination(
    model: ModelType,
    training_data: DataFrame,
    model_features: Tuple[str, ...],
    tuned_hyperparameters: str = "n/a",
) -> List[str]:
    start_time: float = time.time()

    train_x, train_y = split_training_data(training_data, model_features)

    metrics = get_model_performance_metrics(model, train_x, train_y)

    training_time = time.time() - start_time
    print(f"Training time: {training_time:.2f}")
    print(f"Features: {model_features}")
    print(f"Precision: {metrics[0]}%")
    print(f"Recall: {metrics[1]}%")
    print(f"F1-Score: {metrics[2]}%")
    print(f"Overfit: {metrics[3]}%")
    combination_train_results = dict(
        model=model.__class__.__name__,
        features=" ".join(
            FEATURES_DICTS[feature] for feature in model_features
        ),
        precision=round(metrics[0], 1),
        recall=round(metrics[1], 1),
        f_score=round(metrics[2], 1),
        overfit=round(metrics[3], 1),
        tuned_parameters=tuned_hyperparameters,
        training_time=training_time,
    )
    training_output = list(combination_train_results.values())
    redshift.insert("training", combination_train_results)

    return training_output


def get_best_combination(
    training_results: List[List[str]],
) -> Tuple[Tuple[str, ...], str]:
    inv_features_dict: Dict[str, str] = {
        v: k for k, v in FEATURES_DICTS.items()
    }

    # Sort results in descending order by F1 and Overfit
    sorted_results: List[List[str]] = sorted(
        training_results[1:],
        key=lambda results_row: (float(results_row[4]), float(results_row[5])),
        reverse=True,
    )
    best_f1_score: float = float(sorted_results[0][4])
    overfit_limit: float = 8.0
    best_combination_candidates: List[List[str]] = []
    for results_row in sorted_results:
        f1_score = float(results_row[4])
        overfit = float(results_row[5])
        if overfit < overfit_limit and f1_score >= best_f1_score:
            best_f1_score = f1_score
            best_combination_candidates.append(results_row)

    best_features: Tuple[str, ...] = tuple()
    best_f1: str = ""
    min_overfit: float = overfit_limit
    for candidate in best_combination_candidates:
        overfit = float(candidate[5])
        if overfit < min_overfit:
            best_features = tuple(
                [
                    inv_features_dict[feature]
                    for feature in candidate[1].split(" ")
                ]
            )
            best_f1 = str(float(candidate[4]))
            min_overfit = overfit

    return best_features, best_f1
