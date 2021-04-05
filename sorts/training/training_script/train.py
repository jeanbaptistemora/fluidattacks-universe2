#!/usr/bin/env python3

# Standard Libraries
import argparse
import os
import csv
import tempfile
import time
from itertools import combinations
from typing import (
    Dict,
    List,
    Tuple,
)

# Third-party Libraries
from joblib import dump
from pandas import DataFrame
from sklearn.neighbors import KNeighborsClassifier

# Local libraries
from sorts.typings import Model as ModelType
from training.constants import (
    FEATURES_DICTS,
    RESULT_HEADERS,
    S3_BUCKET
)
from training.training_script.utils import (
    get_model_performance_metrics,
    get_previous_training_results,
    load_training_data,
    split_training_data
)


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
        metrics = get_model_performance_metrics(
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
    model_class: ModelType = args.model
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
            .Object(f'training-output/results/{results_filename}')\
            .upload_file(results_filename)
        save_best_model_to_s3(model_class, args.train, training_output)


if __name__ == '__main__':
    main()
