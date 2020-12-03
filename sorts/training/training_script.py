#!/usr/bin/env python3
# -.- coding: utf-8 -.-

# Standard Libraries
import argparse
import os
from typing import (
    List,
    Tuple
)

# Third-party Libraries
import joblib
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neural_network import MLPClassifier


ScoreType = Tuple[float, float, float, None]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Sagemaker specific arguments. Defaults are set in environment variables.
    parser.add_argument(
        '--output-data-dir',
        type=str,
        default=os.environ['SM_OUTPUT_DATA_DIR']
    )
    parser.add_argument(
        '--model-dir',
        type=str,
        default=os.environ['SM_MODEL_DIR']
    )
    parser.add_argument(
        '--train',
        type=str,
        default=os.environ['SM_CHANNEL_TRAIN']
    )
    parser.add_argument(
        '--test',
        type=str,
        default=os.environ['SM_CHANNEL_TEST']
    )

    args = parser.parse_args()

    # Take the set of files and read them into a single pandas dataframe
    input_files: List[str] = [
        os.path.join(args.train, file) for file in os.listdir(args.train)
    ]
    raw_data: List[DataFrame] = [
        pd.read_csv(file, engine="python") for file in input_files
    ]
    train_data: DataFrame = pd.concat(raw_data)

    # Separate the labels from the features in the training data
    train_y: DataFrame = train_data.iloc[:, 0]
    train_x: DataFrame = train_data.iloc[:, 1:]
    train_x = train_x.drop(columns=['extension'])

    # Train the model
    clf = MLPClassifier(random_state=42)
    clf.fit(train_x, train_y)

    # Take the set of test files and read them into a single pandas dataframe
    test_files: List[str] = [
        os.path.join(args.test, file) for file in os.listdir(args.test)
    ]
    raw_data = [
        pd.read_csv(file, engine="python") for file in test_files
    ]
    test_data: DataFrame = pd.concat(raw_data)

    # Separate the labels from the features in the test data
    test_y: DataFrame = test_data.iloc[:, 0]
    test_x: DataFrame = test_data.iloc[:, 1:]
    test_x = test_x.drop(columns=['extension'])

    # Get performance scores
    pred: ndarray = clf.predict(test_x)
    performance: ScoreType = precision_recall_fscore_support(
        test_y,
        pred,
        average='binary'
    )
    print(f'Precision: {performance[0]}%')
    print(f'Recall: {performance[1]}%')
    print(f'F1-Score: {performance[2]}%')

    # Export the trained model to S3
    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))
