#!/usr/bin/env python3

import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from sagemaker.sklearn import SKLearn
from sagemaker.sklearn.estimator import SKLearn as SKLearnEstimator


def deploy_training_job(model: str, delay: int) -> None:
    # Incremental delay since SageMaker does not seem to process some
    # training jobs when requested near the same time.
    time.sleep(delay)

    print(f'Deploying training job for {model}...')
    sklearn_estimator: SKLearnEstimator = SKLearn(
        entry_point='training/training_script.py',
        framework_version='0.23-1',
        instance_type="ml.m5.2xlarge",
        instance_count=1,
        role='arn:aws:iam::205810638802:role/sorts_sagemaker',
        output_path='s3://sorts/training-output',
        base_job_name='sorts-training-test',
        hyperparameters={'classifier': model},
        metric_definitions=[
            {'Name': 'precision', 'Regex': 'Precision: (.*?)%'},
            {'Name': 'recall', 'Regex': 'Recall: (.*?)%'},
            {'Name': 'fscore', 'Regex': 'F1-Score: (.*?)%'},
            {'Name': 'overfit', 'Regex': 'Overfit: (.*?)%'}
        ]
    )
    sklearn_estimator.fit({
        'train': 's3://sorts/training/binary_encoded_training_data.csv'
    })


if __name__ == '__main__':
    models_to_train: List[str] = [
        'MLPClassifier',
        'RandomForestClassifier',
        'KNeighborsClassifier',
        'LinearSVC'
    ]
    with ThreadPoolExecutor(max_workers=len(models_to_train)) as executor:
        executor.map(
            lambda x: deploy_training_job(*x),
            zip(models_to_train, range(len(models_to_train)))
        )
