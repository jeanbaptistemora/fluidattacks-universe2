#!/usr/bin/env python3

from evaluate_results import (
    get_best_model_name,
)
import os
from sagemaker.sklearn.estimator import (
    SKLearn as SKLearnEstimator,
)
from sagemaker.tuner import (
    HyperparameterTuner,
)
from sagemaker_provisioner import (
    get_estimator,
)
import tempfile
from training.constants import (
    DATASET_PATH,
    MODEL_HYPERPARAMETERS,
    SAGEMAKER_METRIC_DEFINITIONS,
)
from training.redshift import (
    db as redshift,
)
from training.training_script.utils import (
    get_previous_training_results,
)


def deploy_hyperparameter_tuning_job() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, "best_model.txt")
        model: str = get_best_model_name(model_name_file)
        model = model.split("-")[0]
    estimator: SKLearnEstimator = get_estimator(
        model, training_script="training/training_script/tune.py"
    )

    tuner = HyperparameterTuner(
        estimator,
        max_jobs=250,
        max_parallel_jobs=8,
        metric_definitions=SAGEMAKER_METRIC_DEFINITIONS,
        objective_metric_name="fscore",
        objective_type="Maximize",
        hyperparameter_ranges=MODEL_HYPERPARAMETERS[model],
        tags=[
            {"Key": "management:area", "Value": "cost"},
            {"Key": "management:product", "Value": "sorts"},
            {"Key": "management:type", "Value": "product"},
        ],
    )

    tuner.fit({"train": DATASET_PATH})

    results_filename: str = f"{model}_tune_results.csv"
    previous_results = get_previous_training_results(results_filename)
    for result in previous_results[1:]:
        combination_train_results = dict(
            model=result[0],
            features=result[1],
            precision=result[2],
            recall=result[3],
            f_score=result[4],
            overfit=result[6],
            tuned_parameters=result[7],
            training_time=result[8],
        )
        redshift.insert("training", combination_train_results)

    # Here we get the best hyperparameters combination.
    # We can evaluate them and make desitions from here.
    _ = tuner.best_estimator().hyperparameters()


if __name__ == "__main__":
    deploy_hyperparameter_tuning_job()
