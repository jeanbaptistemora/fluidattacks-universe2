#!/usr/bin/env python3

# Standard libraries
import os
import tempfile

# Third party libraries
from sagemaker.sklearn.estimator import SKLearn as SKLearnEstimator
from sagemaker.tuner import HyperparameterTuner

# Local libraries
from evaluate_results import get_best_model_name
from training.constants import MODEL_HYPERPARAMETERS
from sagemaker_provisioner import get_estimator


def deploy_hyperparameter_tuning_job() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name_file: str = os.path.join(tmp_dir, 'best_model.txt')
        model: str = get_best_model_name(model_name_file)
        model = model.split('-')[0]
    estimator: SKLearnEstimator = get_estimator(
        model,
        training_script='training/training_script/tune.py'
    )

    tuner = HyperparameterTuner(
        estimator,
        max_jobs=12,
        max_parallel_jobs=3,
        metric_definitions=[
            {'Name': 'precision', 'Regex': 'Precision: (.*?)%'},
            {'Name': 'recall', 'Regex': 'Recall: (.*?)%'},
            {'Name': 'fscore', 'Regex': 'F1-Score: (.*?)%'},
            {'Name': 'overfit', 'Regex': 'Overfit: (.*?)%'}
        ],
        objective_metric_name='fscore',
        objective_type='Maximize',
        hyperparameter_ranges=MODEL_HYPERPARAMETERS[model]
    )

    tuner.fit({
        'train': 's3://sorts/training/binary_encoded_training_data.csv'
    })

    # Here we get the best hyperparameters combination.
    # We can evaluate them and make desitions from here.
    _ = tuner.best_estimator().hyperparameters()


if __name__ == '__main__':
    deploy_hyperparameter_tuning_job()
