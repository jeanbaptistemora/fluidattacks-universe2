# Standard libraries
import os
from typing import List

# Third-party libraries
import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sklearn.neural_network import MLPClassifier

# Local libraries
from features.file import extract_features
from utils.logs import log
from utils.repositories import get_repository_files
from utils.static import load_neural_network


FILE_PREDICT_FEATURES = ['midnight_commits', 'num_lines', 'commit_frequency']


def get_subscription_files_df(fusion_path: str) -> DataFrame:
    """Builds the basic DF with all the files from every repository"""
    files: List[str] = []
    for repo in os.listdir(fusion_path):
        files.extend(get_repository_files(os.path.join(fusion_path, repo)))
    files_df: DataFrame = pd.DataFrame(files, columns=['file'])
    files_df['repo'] = files_df['file'].apply(
        lambda x: os.path.join(fusion_path, x.split('/')[0])
    )
    return files_df


def predict_vuln_likelihood(predict_df: DataFrame, group: str) -> None:
    input_data: DataFrame = predict_df[FILE_PREDICT_FEATURES]
    model: MLPClassifier = load_neural_network()
    class_prediction: ndarray = model.predict(input_data)
    probability_prediction: ndarray = model.predict_proba(input_data)
    merged_predictions: ndarray = np.column_stack([
        class_prediction,
        probability_prediction
    ])
    result_df: DataFrame = pd.concat(
        [
            predict_df[['file']],
            pd.DataFrame(
                merged_predictions,
                columns=['pred', 'prob_safe', 'prob_vuln']
            )
        ],
        axis=1
    )
    errort: float = 5 + 5 * np.random.rand(len(result_df), )
    result_df['prob_vuln'] = round(result_df.prob_vuln * 100 - errort, 1)
    sorted_files: DataFrame = result_df[result_df.pred == 1]\
        .sort_values(by='prob_vuln', ascending=False)\
        .reset_index(drop=True)[['file', 'prob_vuln']]
    csv_name: str = f'{group}_sorts_results.csv'
    sorted_files.to_csv(csv_name, index=False)
    log('info', 'Results saved to file %s', csv_name)


def prioritize(subscription_path: str) -> bool:
    """Prioritizes files according to the chance of finding a vulnerability"""
    success: bool = False
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    if os.path.exists(fusion_path):
        predict_df: DataFrame = get_subscription_files_df(fusion_path)
        success = extract_features(predict_df)
        if success:
            predict_df.drop(
                predict_df[predict_df['file_age'] == -1].index,
                inplace=True
            )
            predict_df.reset_index(inplace=True, drop=True)
            predict_vuln_likelihood(predict_df, group)
    else:
        log(
            'error',
            "There is no 'fusion' folder in the path %s",
            subscription_path
        )
    return success
