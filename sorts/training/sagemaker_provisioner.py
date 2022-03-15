#!/usr/bin/env python3


from concurrent.futures import (
    ThreadPoolExecutor,
)
from sagemaker.sklearn import (
    SKLearn,
)
from sagemaker.sklearn.estimator import (
    SKLearn as SKLearnEstimator,
)
import time
from training.constants import (
    DATASET_PATH,
    INC_TRAINING_MODELS,
    MODELS,
    SAGEMAKER_METRIC_DEFINITIONS,
)
from training.redshift import (
    db as redshift,
)
from training.training_script.utils import (
    get_previous_training_results,
)
from typing import (
    List,
)

JOB_CREATION_DELAY_MULTIPLIER: int = 30

ON_DEMAND_NEEDED: List[str] = [
    "gradientboostingclassifier",
    "kneighborsclassifier",
    "mlpclassifier",
]

INCMODELS_S3PATH: str = "s3://sorts/incremental-training-output/"


def get_estimator(
    model: str,
    training_script: str = "training/training_script/train.py",
) -> SKLearnEstimator:
    model_uri = f"{INCMODELS_S3PATH}{model.split(':')[0]}-inc-training.joblib"
    if ":inctraining" not in model:
        kwargs = (
            dict(
                instance_type="ml.m5.2xlarge",
                use_spot_instances=True,
                max_wait=86400,
            )
            if model not in ON_DEMAND_NEEDED
            else dict(instance_type="ml.m5.4xlarge")
        )
    else:
        kwargs = (
            dict(
                instance_type="ml.m5.2xlarge",
                use_spot_instances=True,
                max_wait=86400,
                model_uri=model_uri,
            )
            if model.split(":")[0] not in ON_DEMAND_NEEDED
            else dict(
                instance_type="ml.m5.4xlarge",
                model_uri=model_uri,
            )
        )
    sklearn_estimator: SKLearnEstimator = SKLearn(
        entry_point=training_script,
        dependencies=["sorts", "training", "training/requirements.txt"],
        framework_version="0.23-1",
        instance_count=1,
        role="arn:aws:iam::205810638802:role/prod_sorts",
        output_path="s3://sorts/training-output",
        base_job_name=f"sorts-training-test-{model.split(':')[0].lower()}",
        hyperparameters={"model": model.split(":")[0]},
        metric_definitions=SAGEMAKER_METRIC_DEFINITIONS,
        debugger_hook_config=False,
        tags=[
            {"Key": "management:area", "Value": "cost"},
            {"Key": "management:product", "Value": "sorts"},
            {"Key": "management:type", "Value": "product"},
        ],
        **kwargs,
    )

    return sklearn_estimator


def deploy_training_job(model: str, delay: int) -> None:
    # Incremental delay since SageMaker does not seem to process some
    # training jobs when requested near the same time.
    # Additionally, it may fail to create jobs if requested in
    # too short an interval
    time.sleep(delay * JOB_CREATION_DELAY_MULTIPLIER)

    print(f"Deploying training job for {model}...")
    sklearn_estimator: SKLearnEstimator = get_estimator(model)
    sklearn_estimator.fit({"train": DATASET_PATH})
    results_filename: str = f"{model}_train_results.csv"
    previous_results = get_previous_training_results(results_filename)
    for result in previous_results[1:]:
        combination_train_results = dict(
            model=result[0],
            features=result[1],
            precision=result[2],
            recall=result[3],
            f_score=result[4],
            overfit=result[5],
            tuned_parameters=result[6],
            training_time=result[7],
        )
        redshift.insert("training", combination_train_results)


if __name__ == "__main__":
    models_to_train: List[str] = list(MODELS.keys())
    models_to_retrain: List[str] = [
        s + ":inctraining" for s in list(INC_TRAINING_MODELS.keys())
    ]
    model_list_len = len(models_to_train + models_to_retrain)
    with ThreadPoolExecutor(max_workers=model_list_len) as executor:
        executor.map(
            lambda x: deploy_training_job(*x),
            zip(models_to_train + models_to_retrain, range(model_list_len)),
        )
