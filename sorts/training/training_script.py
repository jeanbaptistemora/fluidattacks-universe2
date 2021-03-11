#!/usr/bin/env python3

# Standard Libraries
import argparse
import csv
import os
import tempfile
import time
from itertools import combinations
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

# Third-party Libraries
import boto3
import numpy as np
import pandas as pd
from botocore.exceptions import ClientError
from joblib import dump
from numpy import ndarray
from pandas import DataFrame
from sklearn.model_selection import (
    cross_validate,
    learning_curve
)
from sklearn.neighbors import KNeighborsClassifier

# Local libraries
from sorts.typings import Model as ModelType

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
S3_BUCKET = boto3.Session().resource('s3').Bucket('sorts')


def get_features_combinations(features: List[str]) -> List[Tuple[str, ...]]:
    feature_combinations: List[Tuple[str, ...]] = []
    for idx in range(len(features) + 1):
        feature_combinations += list(combinations(features, idx))
    return list(filter(None, feature_combinations))


def get_model_instance(model_class: ModelType) -> ModelType:
    default_args: Dict[str, int] = {}
    if model_class != KNeighborsClassifier:
        default_args = {'random_state': 42}
    return model_class(**default_args)


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


def get_tried_combinations(
    previous_results: List[List[str]]
) -> List[Tuple[str, ...]]:
    """Analyze results to see which combinations have already been tried"""
    tried_combinations: List[Tuple[str, ...]] = []
    inv_features_dict: Dict[str, str] = {
        v: k for k, v in FEATURES_DICTS.items()
    }
    if previous_results:
        # The first element is the header, so we can skip it
        for result in previous_results[1:]:
            features_tried: str = result[1]
            tried_combinations.append(
                tuple([
                    inv_features_dict[feature]
                    for feature in features_tried.split(' ')
                ])
            )
    return tried_combinations


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


def save_best_model_to_s3(
    model_class: ModelType,
    training_dir: str,
    training_results: List[List[str]]
) -> None:
    inv_features_dict: Dict[str, str] = {
        v: k for k, v in FEATURES_DICTS.items()
    }

    # Sort results in descending order by F1 and Overfit
    sorted_results: List[List[str]] = sorted(
        training_results[1:],
        key=lambda x: (float(x[-2]), float(x[-1])),
        reverse=True
    )
    best_features: Tuple[str, ...] = tuple()
    best_f1: str = ''
    for result in sorted_results:
        if float(result[-1]) < 5:
            best_features = tuple([
                inv_features_dict[feature]
                for feature in result[1].split(' ')
            ])
            best_f1 = f'{float(result[-2]):.0f}'
            break
    if best_features:
        training_data: DataFrame = load_training_data(training_dir)
        train_x, train_y = split_training_data(training_data, best_features)
        model = get_model_instance(model_class)
        model.fit(train_x, train_y)
        model.feature_names = list(best_features)

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_name: str = '-'.join(
                [type(model).__name__.lower(), best_f1] +
                [FEATURES_DICTS[feature].lower() for feature in best_features]
            )
            local_file: str = os.path.join(tmp_dir, f'{model_name}.joblib')
            dump(model, local_file)
            S3_BUCKET.Object(
                f'training-output/{model_name}.joblib'
            ).upload_file(local_file)


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


def train_model(
    model_class: ModelType,
    training_dir: str,
    previous_results: List[List[str]]
) -> List[List[str]]:
    all_combinations = get_features_combinations(
        list(FEATURES_DICTS.keys())
    )
    training_data: DataFrame = load_training_data(training_dir)
    training_output: List[List[str]] = (
        previous_results if previous_results else [RESULT_HEADERS]
    )

    # Get previously tried combinations to avoid duplicating work
    tried_combinations = get_tried_combinations(previous_results)
    valid_combinations: List[Tuple[str, ...]] = [
        combination
        for combination in all_combinations
        if combination not in tried_combinations
    ]

    # Train the model
    for combination in valid_combinations:
        start_time: float = time.time()
        train_x, train_y = split_training_data(training_data, combination)

        model = get_model_instance(model_class)
        metrics = get_model_metrics(
            model,
            train_x,
            train_y
        )

        print(f'Training time: {time.time() - start_time:.2f}')
        print(f'Features: {combination}')
        print(f'Precision: {metrics[0]}%')
        print(f'Recall: {metrics[1]}%')
        print(f'F1-Score: {metrics[2]}%')
        print(f'Overfit: {metrics[3]}%')
        training_output.append([
            model.__class__.__name__,
            ' '.join(FEATURES_DICTS[x] for x in combination),
            f'{metrics[0]:.1f}',
            f'{metrics[1]:.1f}',
            f'{metrics[2]:.1f}',
            f'{metrics[3]:.1f}'
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
        previous_results = get_previous_training_results(results_filename)
        training_output = train_model(
            model_class,
            args.train,
            previous_results
        )
        with open(results_filename, 'w', newline='') as results_file:
            csv_writer = csv.writer(results_file)
            csv_writer.writerows(training_output)
        S3_BUCKET\
            .Object(f'training-output/{results_filename}')\
            .upload_file(results_filename)
        save_best_model_to_s3(model_class, args.train, training_output)


if __name__ == '__main__':
    main()
