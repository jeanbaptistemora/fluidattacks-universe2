#!/usr/bin/env python3

# Standard libraries
import os
import tempfile

# Third party libraries
from sagemaker.sklearn.estimator import SKLearn as SKLearnEstimator
from sagemaker.tuner import (
    CategoricalParameter,
    HyperparameterTuner
)

# Local libraries
from evaluate_results import get_best_model_name
from sagemaker_provisioner import get_estimator


def deploy_hyperparameter_tuning_job() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        model: str = get_best_model_name(model_name_file)
    estimator: SKLearnEstimator = get_estimator(
        model,
        training_script='training/training_script_tuning.py'
    )

    tuner = HyperparameterTuner(
        estimator,
        metric_definitions=[
            {'Name': 'precision', 'Regex': 'Precision: (.*?)%'},
            {'Name': 'recall', 'Regex': 'Recall: (.*?)%'},
            {'Name': 'fscore', 'Regex': 'F1-Score: (.*?)%'},
            {'Name': 'overfit', 'Regex': 'Overfit: (.*?)%'}
        ],
        objective_metric_name='fscore',
        objective_type='Maximize',
        hyperparameter_ranges={
            'activation': CategoricalParameter(['tanh', 'relu'])
        }
    )

    tuner.fit({
        'train': 's3://sorts/training/binary_encoded_training_data.csv'
    })


if __name__ == '__main__':
    deploy_hyperparameter_tuning_job()
