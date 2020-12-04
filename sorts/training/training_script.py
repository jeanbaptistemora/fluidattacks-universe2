#!/usr/bin/env python3

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
from sklearn.model_selection import (
    cross_validate,
    learning_curve
)
from sklearn.neural_network import MLPClassifier


ScoreType = Tuple[float, float, float, None]


def is_overfit(train_scores: ndarray, test_scores: ndarray) -> float:
    train_scores_means: ndarray = train_scores.mean(axis=1)
    test_scores_means: ndarray = test_scores.mean(axis=1)
    perc_diff: ndarray = (
        (train_scores_means - test_scores_means) / train_scores_means
    )
    row: int = 0
    tolerance: float = 0.002
    goal: int = 4
    for i in range(len(perc_diff) - 1):
        progress: float = abs(perc_diff[i + 1] - perc_diff[i])
        if progress < tolerance:
            row += 1
        else:
            row = 0
        if row == goal:
            min_overfit: ndarray = perc_diff[i - row - 1:i]
            return float(min_overfit.mean())
    return float(perc_diff.mean())


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

    scores = cross_validate(
        clf,
        train_x,
        train_y,
        scoring=['precision', 'recall', 'f1'],
        n_jobs=-1
    )

    _, train_results, test_results = learning_curve(
        clf,
        train_x,
        train_y,
        scoring='f1',
        n_jobs=-1,
        random_state=42
    )
    overfit = is_overfit(train_results, test_results)

    print(f"Precision: {scores['test_precision'].mean()}%")
    print(f"Recall: {scores['test_recall'].mean()}%")
    print(f"F1-Score: {scores['test_f1'].mean()}%")
    print(f"Overfit: {overfit*100:.0f}%")

    # Export the trained model to S3
    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))
