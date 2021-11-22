#!/usr/bin/env python3


from concurrent.futures import (
    ThreadPoolExecutor,
)
import os
from sagemaker.sklearn import (
    SKLearn,
)
from sagemaker.sklearn.estimator import (
    SKLearn as SKLearnEstimator,
)
import time
from training.constants import (
    DATASET_PATH,
    MODELS,
    SAGEMAKER_METRIC_DEFINITIONS,
)
from typing import (
    Dict,
    List,
)


def get_train_extra_envs() -> Dict[str, str]:
    return dict(
        REDSHIFT_DATABASE=os.environ["REDSHIFT_DATABASE"],
        REDSHIFT_HOST=os.environ["REDSHIFT_HOST"],
        REDSHIFT_PASSWORD=os.environ["REDSHIFT_PASSWORD"],
        REDSHIFT_PORT=os.environ["REDSHIFT_PORT"],
        REDSHIFT_USER=os.environ["REDSHIFT_USER"],
    )


def get_estimator(
    model: str,
    training_script: str = "training/training_script/train.py",
) -> SKLearnEstimator:
    sklearn_estimator: SKLearnEstimator = SKLearn(
        entry_point=training_script,
        dependencies=["sorts", "training", "training/requirements.txt"],
        framework_version="0.23-1",
        instance_type="ml.m5.2xlarge",
        instance_count=1,
        role="arn:aws:iam::205810638802:role/sorts_prod",
        output_path="s3://sorts/training-output",
        base_job_name=f"sorts-training-test-{model.lower()}",
        hyperparameters={"model": model, "envs": get_train_extra_envs()},
        metric_definitions=SAGEMAKER_METRIC_DEFINITIONS,
        debugger_hook_config=False,
        use_spot_instances=True,
        max_wait=86400,
        tags={
            "management:area": "cost",
            "management:type": "product",
        },
    )

    return sklearn_estimator


def deploy_training_job(model: str, delay: int) -> None:
    # Incremental delay since SageMaker does not seem to process some
    # training jobs when requested near the same time.
    time.sleep(delay)

    print(f"Deploying training job for {model}...")
    sklearn_estimator: SKLearnEstimator = get_estimator(model)
    sklearn_estimator.fit({"train": DATASET_PATH})


if __name__ == "__main__":
    models_to_train: List[str] = list(MODELS.keys())
    with ThreadPoolExecutor(max_workers=len(models_to_train)) as executor:
        executor.map(
            lambda x: deploy_training_job(*x),
            zip(models_to_train, range(len(models_to_train))),
        )
