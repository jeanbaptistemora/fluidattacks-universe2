# Standard libraries
import csv
import os
import tempfile
from typing import (
    List,
    Tuple
)

# Third party libraries
from botocore.exceptions import ClientError
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import (
    cross_validate,
    learning_curve
)


# Local libraries
from sorts.typings import Model as ModelType
from training.constants import S3_BUCKET


def is_overfit(train_results: ndarray, test_results: ndarray) -> float:
    """Calculate how much the model got biased by the training data"""
    train_results_means: ndarray = train_results.mean(axis=1)
    test_results_means: ndarray = test_results.mean(axis=1)
    perc_diff: ndarray = (
        (train_results_means - test_results_means) / train_results_means
    )
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
            min_overfit: ndarray = perc_diff[i - row - 1:i]
            return float(min_overfit.mean())

    return float(perc_diff.mean())


def get_model_performance_metrics(
    model: ModelType,
    features: DataFrame,
    labels: DataFrame
) -> Tuple[float, float, float, float]:
    """Get performance metrics to compare different models"""
    scores = cross_validate(
        model,
        features,
        labels,
        scoring=['precision', 'recall', 'f1'],
        n_jobs=-1
    )
    _, train_results, test_results = learning_curve(
        model,
        features,
        labels,
        scoring='f1',
        train_sizes=np.linspace(0.1, 1, 30),
        n_jobs=-1,
        random_state=42
    )

    return (
        scores['test_precision'].mean() * 100,
        scores['test_recall'].mean() * 100,
        scores['test_f1'].mean() * 100,
        is_overfit(train_results, test_results) * 100
    )


def split_training_data(
    training_df: DataFrame,
    feature_list: Tuple[str, ...]
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
                :,
                training_df.columns.str.startswith('extension_')
            ]
        ],
        axis=1)
    filtered_df.dropna(inplace=True)

    return filtered_df.iloc[:, 1:], filtered_df.iloc[:, 0]


def get_previous_training_results(results_filename: str) -> List[List[str]]:
    previous_results: List[List[str]] = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_file: str = os.path.join(tmp_dir, results_filename)
        remote_file: str = f'training-output/{results_filename}'
        try:
            S3_BUCKET.Object(remote_file).download_file(local_file)
            with open(local_file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                previous_results.extend(csv_reader)
        except ClientError:
            pass

    return previous_results
