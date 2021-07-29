import argparse
import os
from pandas import (
    DataFrame,
)
from sorts.typings import (
    Model as ModelType,
)
import tempfile
from training.constants import (
    FEATURES_DICTS,
    MODEL_HYPERPARAMETERS,
    MODELS,
    RESULT_HEADERS,
)
from training.evaluate_results import (
    get_best_model_name,
)
from training.training_script.utils import (
    get_previous_training_results,
    load_training_data,
    save_model_to_s3,
    set_sagemaker_extra_envs,
    train_combination,
    update_results_csv,
)
from typing import (
    Dict,
    List,
    Tuple,
)


def get_model_features() -> Tuple[str, ...]:
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


def train_model(
    model: ModelType,
    model_features: Tuple[str, ...],
    training_dir: str,
    previous_results: List[List[str]],
    tuned_hyperparameters: str,
) -> List[List[str]]:
    training_data: DataFrame = load_training_data(training_dir)
    training_output: List[List[str]] = (
        previous_results if previous_results else [RESULT_HEADERS]
    )
    training_combination_output: List[str] = train_combination(
        model, training_data, model_features, tuned_hyperparameters
    )
    training_output.append(training_combination_output)

    return training_output


def save_model(
    model: ModelType,
    f1_score: float,
    model_features: Tuple[str, ...],
    tuned_hyperparameters: List[str],
) -> None:
    model_file_name: str = "-".join(
        [
            type(model).__name__.lower(),
            str(f1_score),
            "-".join(
                [FEATURES_DICTS[feature].lower() for feature in model_features]
            ),
            "tune",
            "-".join(
                list(str(parameter) for parameter in tuned_hyperparameters)
            ),
        ]
    )
    save_model_to_s3(model, model_file_name)


def get_model_hyperparameters(
    model_name: str, args: Dict[str, str]
) -> Dict[str, str]:
    model_hyperparameters = list(MODEL_HYPERPARAMETERS[model_name].keys())

    return {parameter: args[parameter] for parameter in model_hyperparameters}


def display_model_hyperparameters(
    model_name: str, hyperaparameters_list: Dict[str, str]
) -> None:
    print(
        f"We have the following hyperparameters "
        f"for our {model_name.upper()} model tuning:"
    )
    for parameter, value in hyperaparameters_list.items():
        print(f"{parameter}: {value}")


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
    parser.add_argument("--model", type=str, default="")

    # MLPCLassifier parameters to tune
    parser.add_argument("--activation", type=str, default="")
    parser.add_argument("--solver", type=str, default="")

    # XGBoost parameters to tune
    parser.add_argument("--criterion", type=str, default="friedman_mse")
    parser.add_argument("--loss", type=str, default="deviance")
    parser.add_argument("--max_depth", type=int, default=3)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--learning_rate", type=float, default=0.1)

    # Extra args that SageMaker excution may need (fex. ENVS)
    parser.add_argument("--envs", type=str, default="")

    return parser.parse_args()


def main() -> None:
    args = cli()

    model_name: str = args.model.split("-")[0]
    model_features: Tuple[str, ...] = get_model_features()

    # Set necessary env vars that SageMaker environment needs
    set_sagemaker_extra_envs(args.envs)

    hyperparameters_to_tune = get_model_hyperparameters(model_name, vars(args))
    display_model_hyperparameters(model_name, hyperparameters_to_tune)
    model_class: ModelType = MODELS[model_name]
    model: ModelType = model_class(**hyperparameters_to_tune)

    results_filename: str = f"{model_name}_train_results.csv"
    previous_results = get_previous_training_results(results_filename)

    # Start training process
    hyperparameters_to_tune_list = ", ".join(
        list(str(parameter) for parameter in hyperparameters_to_tune.values())
    )
    training_output = train_model(
        model,
        model_features,
        args.train,
        previous_results,
        hyperparameters_to_tune_list,
    )
    training_output[-1] += [hyperparameters_to_tune_list]

    update_results_csv(results_filename, training_output)
    save_model(
        model,
        float(training_output[-1][4]),
        model_features,
        list(hyperparameters_to_tune.values()),
    )


if __name__ == "__main__":
    main()
