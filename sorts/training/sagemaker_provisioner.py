#!/usr/bin/env python3

from sagemaker.sklearn import SKLearn
from sagemaker.sklearn.estimator import SKLearn as SKLearnEstimator

if __name__ == '__main__':
    sklearn_estimator: SKLearnEstimator = SKLearn(
        entry_point='training/training_script.py',
        framework_version='0.23-1',
        instance_type="ml.m5.2xlarge",
        instance_count=1,
        role='arn:aws:iam::205810638802:role/sorts_sagemaker',
        output_path='s3://sorts/training-output',
        base_job_name='sorts-training-test',
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
