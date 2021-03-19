# Standard libraries
import argparse
import csv
import os
import tempfile
import time
from typing import (
    Dict,
    List,
    Optional,
    Tuple
)

# Third party Libraries
import numpy as np
from botocore.exceptions import ClientError
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import (
    cross_validate,
    learning_curve
)

# Local libraries
from sorts.constants import ModelType
from training.constants import S3_BUCKET
from training.evaluate_results import get_best_model_name
from training.training_script import is_overfit

# Constants
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


def get_model_features() -> Tuple[str, ...]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        best_model: str = get_best_model_name(model_name_file)
        inv_features_dict: Dict[str, str] = {
            value: key for key, value in FEATURES_DICTS.items()
        }
        return tuple(
            inv_features_dict[key]
            for key in best_model.upper().split('.')[0].split('-')[2:5]
        )


def get_model_performance_metrics(
    model: ModelType,
    features: DataFrame,
    labels: DataFrame
) -> Tuple[float, float, float, float]:
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


def load_training_data(training_dir: str) -> DataFrame:
    """Load a DataFrame with the training data in CSV format stored in S3"""
    input_files: List[str] = [
        os.path.join(training_dir, file) for file in os.listdir(training_dir)
    ]
    raw_data: List[DataFrame] = [
        pd.read_csv(file, engine="python") for file in input_files
    ]
    return pd.concat(raw_data)


def train_model(
    model_class: ModelType,
    training_dir: str
) -> List[List[str]]:
    model_features: Tuple[str, ...] = get_model_features()
    start_time: float = time.time()

    training_data: DataFrame = load_training_data(training_dir)
    train_x, train_y = split_training_data(training_data, model_features)

    model = model_class()
    metrics = get_model_performance_metrics(
        model,
        train_x,
        train_y
    )

    print(f'Training time: {time.time() - start_time:.2f}')
    print(f'Features: {model_features}')
    print(f'Precision: {metrics[0]}%')
    print(f'Recall: {metrics[1]}%')
    print(f'F1-Score: {metrics[2]}%')
    print(f'Overfit: {metrics[3]}%')
    training_output = [
        model.__class__.__name__,
        ' '.join(FEATURES_DICTS[feature] for feature in model_features),
        f'{metrics[0]:.1f}',
        f'{metrics[1]:.1f}',
        f'{metrics[2]:.1f}',
        f'{metrics[3]:.1f}'
    ]
    return training_output


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


def main() -> None:
    parser = argparse.ArgumentParser()
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
    parser.add_argument('--model', type=str, default='')
    parser.add_argument('--activation', type=str, default='')
    args = parser.parse_args()

    model: str = args.model
    model_class: Optional[ModelType] = globals().get(model)
    _ = train_model(
        model_class,
        args.train
    )


if __name__ == '__main__':
    main()
