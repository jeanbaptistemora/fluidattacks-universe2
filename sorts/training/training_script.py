#!/usr/bin/env python3

# Standard Libraries
import argparse
import csv
import os
import time
from itertools import combinations
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union
)

# Third-party Libraries
import boto3
import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    cross_validate,
    learning_curve
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC


# Type Constants
ScoreType = Tuple[float, float, float, None]
ModelType = Union[
    MLPClassifier,
    RandomForestClassifier,
    LinearSVC,
    KNeighborsClassifier
]

# Contants
FEATURES_DICTS: Dict[str, str] = {
    'num_commits': 'CM',
    'num_unique_authors': 'AU',
    'file_age': 'FA',
    'midnight_commits': 'MC',
    'risky_commits': 'RC',
    'seldom_contributors': 'SC',
    'num_lines': 'LC',
    'busy_file': 'BF',
    'commit_frequency': 'CF'
}
RESULT_HEADERS: List[str] = [
    'Model',
    'Features',
    'Precision',
    'Recall',
    'F1',
    'Overfit'
]


def get_features_combinations(features: List[str]) -> List[Tuple[str, ...]]:
    feature_combinations: List[Tuple[str, ...]] = []
    for idx in range(len(features) + 1):
        feature_combinations += list(combinations(features, idx))
    return feature_combinations


def get_model_metrics(
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


def load_training_data(training_dir: str) -> DataFrame:
    """Load a DataFrame with the training data in CSV format stored in S3"""
    input_files: List[str] = [
        os.path.join(training_dir, file) for file in os.listdir(training_dir)
    ]
    raw_data: List[DataFrame] = [
        pd.read_csv(file, engine="python") for file in input_files
    ]
    return pd.concat(raw_data)


def split_training_data(
    training_df: DataFrame,
    feature_list: Tuple[str, ...]
) -> Tuple[DataFrame, DataFrame]:
    """Read the training data in two DataFrames for training purposes"""
    # Separate the labels from the features in the training data
    labels: DataFrame = training_df.iloc[:, 0]
    features_df: DataFrame = training_df.iloc[:, 1:]
    features_df = pd.concat(
        [
            features_df.loc[:, feature_list],
            # Include all extensions
            features_df.loc[:, 'extension_0':]  # type: ignore
        ],
        axis=1)
    return features_df, labels


def train_model(model_class: ModelType, training_dir: str) -> List[List[str]]:
    all_combinations = get_features_combinations(
        list(FEATURES_DICTS.keys())
    )
    training_data: DataFrame = load_training_data(training_dir)
    training_output: List[List[str]] = [RESULT_HEADERS]

    # Train the model
    for combination in filter(None, all_combinations):
        start_time: float = time.time()
        train_x, train_y = split_training_data(training_data, combination)

        default_args: Dict[str, int] = {}
        if model_class != KNeighborsClassifier:
            default_args = {'random_state': 42}
        model = model_class(**default_args)

        precision, recall, f1_score, overfit = get_model_metrics(
            model,
            train_x,
            train_y
        )

        print(f'Training time: {time.time() - start_time:.2f}')
        print(f'Features: {combination}')
        print(f'Precision: {precision}%')
        print(f'Recall: {recall}%')
        print(f'F1-Score: {f1_score}%')
        print(f'Overfit: {overfit}%')
        training_output.append([
            model.__class__.__name__,
            ' '.join(FEATURES_DICTS[x] for x in combination),
            f'{precision:.1f}',
            f'{recall:.1f}',
            f'{f1_score:.1f}',
            f'{overfit:.1f}'
        ])
    return training_output


def main() -> None:
    parser = argparse.ArgumentParser()
    # Sagemaker specific arguments. Defaults are set in environment variables.
    parser.add_argument(
        '--output-data-dir',
        type=str,
        default=os.environ['SM_OUTPUT_DATA_DIR']
    )
    parser.add_argument(
        '--model-dir',
        type=str,
        default=os.environ['SM_MODEL_DIR']
    )
    parser.add_argument(
        '--train',
        type=str,
        default=os.environ['SM_CHANNEL_TRAIN']
    )
    # Model to train sent as a hyperparamenter
    parser.add_argument('--model', type=str, default='')
    args = parser.parse_args()

    model: str = args.model
    model_class: Optional[ModelType] = globals().get(model)
    if model_class:
        results_filename: str = f'{model.lower()}_train_results.csv'
        training_output = train_model(model_class, args.train)
        with open(results_filename, 'w', newline='') as results_file:
            csv_writer = csv.writer(results_file)
            csv_writer.writerows(training_output)
        boto3.Session().resource('s3').Bucket('sorts')\
            .Object(f'training-output/{results_filename}')\
            .upload_file(results_filename)


if __name__ == '__main__':
    main()
