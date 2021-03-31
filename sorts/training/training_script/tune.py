# Standard libraries
import argparse
import os
import csv
import tempfile
import time
from typing import (
    Dict,
    List,
    Tuple
)

# Third party Libraries
from joblib import dump
from pandas import DataFrame

# Local libraries
from sorts.typings import Model as ModelType
from training.constants import (
    FEATURES_DICTS,
    MODELS,
    RESULT_HEADERS,
    S3_BUCKET
)
from training.evaluate_results import get_best_model_name
from training.training_script.utils import (
    get_model_performance_metrics,
    get_previous_training_results,
    load_training_data,
    split_training_data
)


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


def train_model(
    model: ModelType,
    model_features: Tuple[str, ...],
    training_dir: str,
    previous_results: List[List[str]]
) -> List[List[str]]:
    start_time: float = time.time()

    training_data: DataFrame = load_training_data(training_dir)
    training_output: List[List[str]] = (
        previous_results if previous_results else [RESULT_HEADERS]
    )
    train_x, train_y = split_training_data(training_data, model_features)

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
    training_output.append([
        model.__class__.__name__,
        ' '.join(FEATURES_DICTS[feature] for feature in model_features),
        f'{metrics[0]:.1f}',
        f'{metrics[1]:.1f}',
        f'{metrics[2]:.1f}',
        f'{metrics[3]:.1f}'
    ])

    return training_output


def update_results_csv(filename: str, results: List[List[str]]) -> None:
    with open(filename, 'w', newline='') as results_file:
        csv_writer = csv.writer(results_file)
        csv_writer.writerows(results)
    S3_BUCKET \
        .Object(f'training-output/{filename}')\
        .upload_file(filename)


def save_model(
    model: ModelType,
    f1_score: float,
    model_features: Tuple[str, ...],
    activation: str
) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_list = [
            type(model).__name__.lower(),
            f'{f1_score:.0f}',
            '-'.join([
                FEATURES_DICTS[feature].lower() for feature in model_features
            ]),
            'tune',
            activation
        ]
        model_file_name: str = '-'.join(model_name_list)
        local_file: str = os.path.join(tmp_dir, f'{model_file_name}.joblib')
        dump(model, local_file)
        S3_BUCKET.Object(
            f'training-output/{model_file_name}.joblib'
        ).upload_file(local_file)


def main() -> None:  # pylint: disable=too-many-locals
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

    # We compile here all hyperparameters selected for tuning
    hyperparameters_to_tune: List[str] = [args.activation]

    model_name: str = args.model.split('-')[0]
    model_features: Tuple[str, ...] = get_model_features()
    model_class: ModelType = MODELS[model_name]
    model: ModelType = model_class(activation=args.activation)

    results_filename: str = f'{model_name}_train_results.csv'
    previous_results = get_previous_training_results(results_filename)

    training_output = train_model(
        model,
        model_features,
        args.train,
        previous_results
    )
    training_output[-1] += [', '.join(hyperparameters_to_tune)]

    update_results_csv(results_filename, training_output)
    save_model(
        model,
        float(training_output[-1][4]),
        model_features,
        args.activation
    )


if __name__ == '__main__':
    main()
