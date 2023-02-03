#!/usr/bin/env python3

import argparse
from itertools import (
    combinations,
)
import os
from pandas import (
    DataFrame,
)
from sklearn.naive_bayes import (
    BernoulliNB,
)
from sklearn.neighbors import (
    KNeighborsClassifier,
)
from sorts.typings import (
    Model as ModelType,
)
from training.constants import (
    FEATURES_DICTS,
    MODELS,
    MODELS_DEFAULTS,
    RESULT_HEADERS,
)
from training.training_script.utils import (
    get_best_combination,
    load_training_data,
    save_model_to_s3,
    split_training_data,
    train_combination,
    update_results_csv,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


def get_features_combinations(features: List[str]) -> List[Tuple[str, ...]]:
    feature_combinations: List[Tuple[str, ...]] = []
    for idx in range(len(features) + 1):
        feature_combinations += list(combinations(features, idx))
    return list(filter(None, feature_combinations))


def get_model_instance(model_class: ModelType) -> ModelType:
    default_args: Dict[str, Any] = {}
    if model_class not in (BernoulliNB, KNeighborsClassifier):
        default_args = {"random_state": 42}
        model_defaults = MODELS_DEFAULTS.get(model_class, {})
        default_args.update(model_defaults)

    return model_class(**default_args)


def get_tried_combinations(
    previous_results: List[List[str]],
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
                tuple(  # pylint: disable=consider-using-generator
                    [
                        inv_features_dict[feature]
                        for feature in features_tried.split(" ")
                    ]
                )
            )
    return tried_combinations


def save_model(
    model_class: ModelType,
    training_dir: str,
    training_results: List[List[str]],
) -> None:
    best_features, best_f1 = get_best_combination(training_results)

    if best_features:
        training_data: DataFrame = load_training_data(training_dir)
        shuffled_training_data = training_data.sample(
            frac=1, random_state=42
        ).reset_index(drop=True)
        train_x, train_y = split_training_data(
            shuffled_training_data, best_features
        )
        model = get_model_instance(model_class)
        model.fit(train_x, train_y)
        model_file_name: str = "-".join(
            [type(model).__name__.lower(), best_f1]
            + [FEATURES_DICTS[feature].lower() for feature in best_features]
        )
        model.feature_names = list(best_features)
        model.precision = training_results[-1][2]
        model.recall = training_results[-1][3]
        save_model_to_s3(model, model_file_name)


def train_model(
    model_class: ModelType,
    training_dir: str,
) -> List[List[str]]:
    all_combinations = get_features_combinations(list(FEATURES_DICTS.keys()))
    training_data: DataFrame = load_training_data(training_dir)
    shuffled_training_data = training_data.sample(
        frac=1, random_state=42
    ).reset_index(drop=True)
    training_output: List[List[str]] = [RESULT_HEADERS]

    # Train the model
    for combination in all_combinations:
        model = get_model_instance(model_class)
        training_combination_output: List[str] = train_combination(
            model, shuffled_training_data, combination
        )
        training_output.append(training_combination_output)

    return training_output


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    # Sagemaker specific arguments. Defaults are set in environment variables.
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ["SM_OUTPUT_DATA_DIR"]
    )
    parser.add_argument(
        "--model-dir", type=str, default=os.environ["SM_MODEL_DIR"]
    )
    parser.add_argument(
        "--train", type=str, default=os.environ["SM_CHANNEL_TRAIN"]
    )

    # Model to train sent as a hyperparamenter
    parser.add_argument("--model", type=str, default="")

    return parser.parse_args()


def main() -> None:
    args = cli()

    model_name: str = args.model
    model_class: ModelType = MODELS[model_name]

    # Start training process
    if model_class:
        results_filename: str = f"{model_name}_train_results.csv"
        training_output = train_model(model_class, args.train)
        update_results_csv(results_filename, training_output)
        save_model(model_class, args.train, training_output)


if __name__ == "__main__":
    main()
