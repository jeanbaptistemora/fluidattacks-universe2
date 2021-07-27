#!/usr/bin/env python3


import argparse
from itertools import (
    combinations,
)
from joblib import (
    dump,
)
from lightgbm import (
    LGBMClassifier,
)
import os
from pandas import (
    DataFrame,
)
from sklearn.linear_model import (
    LogisticRegression,
)
from sklearn.neighbors import (
    KNeighborsClassifier,
)
from sklearn.neural_network import (
    MLPClassifier,
)
from sorts.typings import (
    Model as ModelType,
)
import tempfile
import time
from training.constants import (
    FEATURES_DICTS,
    MODELS,
    RESULT_HEADERS,
    S3_BUCKET,
)
from training.redshift import (
    db as redshift,
)
from training.training_script.utils import (
    get_model_performance_metrics,
    get_previous_training_results,
    load_training_data,
    set_sagemaker_extra_envs,
    split_training_data,
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
    if model_class != KNeighborsClassifier:
        default_args = {"random_state": 42}
        if model_class in [MLPClassifier, LogisticRegression]:
            default_args.update({"max_iter": 500})
        elif model_class == LGBMClassifier:
            default_args.update({"learning_rate": 0.05, "max_depth": 5})
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
                tuple(
                    [
                        inv_features_dict[feature]
                        for feature in features_tried.split(" ")
                    ]
                )
            )
    return tried_combinations


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


def save_best_model_to_s3(
    model_class: ModelType,
    training_dir: str,
    training_results: List[List[str]],
) -> None:
    best_features, best_f1 = get_best_combination(training_results)

    if best_features:
        training_data: DataFrame = load_training_data(training_dir)
        train_x, train_y = split_training_data(training_data, best_features)
        model = get_model_instance(model_class)
        model.fit(train_x, train_y)
        model.feature_names = list(best_features)
        model.precision = training_results[-1][2]
        model.recall = training_results[-1][3]

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_name: str = "-".join(
                [type(model).__name__.lower(), best_f1]
                + [
                    FEATURES_DICTS[feature].lower()
                    for feature in best_features
                ]
            )
            local_file: str = os.path.join(tmp_dir, f"{model_name}.joblib")
            dump(model, local_file)
            S3_BUCKET.Object(
                f"training-output/{model_name}.joblib"
            ).upload_file(local_file)


def train_model(  # pylint: disable=too-many-locals
    model_class: ModelType,
    training_dir: str,
    previous_results: List[List[str]],
) -> List[List[str]]:
    all_combinations = get_features_combinations(list(FEATURES_DICTS.keys()))
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
        metrics = get_model_performance_metrics(model, train_x, train_y)

        training_time = time.time() - start_time
        print(f"Training time: {training_time:.2f}")
        print(f"Features: {combination}")
        print(f"Precision: {metrics[0]}%")
        print(f"Recall: {metrics[1]}%")
        print(f"F1-Score: {metrics[2]}%")
        print(f"Overfit: {metrics[3]}%")
        combination_train_results = dict(
            model=model.__class__.__name__,
            features=" ".join(
                FEATURES_DICTS[feature] for feature in combination
            ),
            precision=round(metrics[0], 1),
            recall=round(metrics[1], 1),
            f_score=round(metrics[2], 1),
            overfit=round(metrics[3], 1),
            tuned_parameters="n/a",
            training_time=training_time,
        )
        training_output.append(list(combination_train_results.values()))
        redshift.insert("training", combination_train_results)

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

    # Extra args that SageMaker excution may need (fex. ENVS)
    parser.add_argument("--envs", type=str, default="")

    return parser.parse_args()


def main() -> None:
    args = cli()

    model_name: str = args.model.lower()
    model_class: ModelType = MODELS[model_name]

    # Set necessary env vars that SageMaker environment needs
    set_sagemaker_extra_envs(args.envs)

    # Start training process
    if model_class:
        results_filename: str = f"{model_name}_train_results.csv"
        previous_results = get_previous_training_results(results_filename)
        training_output = train_model(
            model_class, args.train, previous_results
        )
        update_results_csv(results_filename, training_output)
        save_best_model_to_s3(model_class, args.train, training_output)


if __name__ == "__main__":
    main()
