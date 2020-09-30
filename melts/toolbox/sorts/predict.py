"""
Extract features from a project's latest commits,
use included model to get predictions and print and save output.
"""

import datetime
import json
import os
import sys
import time
from array import ArrayType
from typing import List, Optional

import git
import numpy as np
import pandas as pd
from git.cmd import Git
from joblib import load
from pandas import DataFrame
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC

from toolbox.sorts.utils import (
    fill_model_commit_features,
    fill_model_file_features
)


def get_repo_files_dataframe(fusion_path: str) -> DataFrame:
    """
    Walks all the subscription repositories and returns a DataFrame with
    the following columns:
        - file: absolute path of each file with the repositry as root
        - repo: relative path of the repository to the system
    """
    files_df: DataFrame = pd.DataFrame()
    ignore_dirs: List[str] = ['.git']
    for repo in os.listdir(fusion_path):
        repo_path: str = os.path.join(fusion_path, repo)
        repo_files: List[str] = [
            os.path.join(path, filename).replace(f'{fusion_path}/', '')
            for path, _, files in os.walk(repo_path)
            for filename in files
            if all([dir_ not in path for dir_ in ignore_dirs])
        ]
        temp_df = pd.DataFrame(repo_files, columns=['file'])
        temp_df['repo'] = repo_path
        files_df = pd.concat([files_df, temp_df])
    files_df.reset_index(drop=True, inplace=True)
    return files_df


def make_repo_dataset(repo: str) -> Optional[DataFrame]:
    dataset_skel: List[List[str]] = []
    gitrepo: Git = git.Git(repo)
    hashes_log: str = gitrepo.log('--pretty=%H,%aI', '--since="10 weeks ago"')
    dataset: Optional[DataFrame] = None
    if len(hashes_log) > 0:
        hashes_list: List[str] = hashes_log.split('\n')
        dataset_skel = [x.split(',') for x in hashes_list]
        dataset = pd.DataFrame(dataset_skel, columns=['commit', 'hour'])
        dataset.hour = dataset.hour.str.split('T').str[1].str.split(':').str[0]
        dataset['repo'] = repo
        dataset['subscription'] = 'waggo'
        dataset = dataset.head(10)
    return dataset


def make_base_dataset(subscription_path: str) -> DataFrame:
    fusion_path: str = f'{subscription_path}/fusion'
    repos: List[str] = os.listdir(fusion_path)
    print(f'This might take around {datetime.timedelta(seconds=len(repos))}')
    dataset: DataFrame = pd.DataFrame()
    for repo in repos:
        repo_path: str = f'{fusion_path}/{repo}'
        curr_dataset = make_repo_dataset(repo_path)
        if curr_dataset is not None:
            dataset = pd.concat([dataset, curr_dataset])
        else:
            sys.stdout.write(f'\rempty log or problem with repo {repo}')
    dataset = dataset.reset_index(drop=True)
    return dataset


def make_full_dataset(subscription_path: str) -> DataFrame:
    dataset: DataFrame = make_base_dataset(subscription_path)
    return fill_model_commit_features(dataset)


def predict_commit(subscription_path: str) -> None:
    start: float = time.time()
    dataset: DataFrame = make_full_dataset(subscription_path)
    dataset = dataset.dropna()
    # https://github.com/python/mypy/issues/2410
    x_test = dataset.loc[:, 'hunks':]  # type: ignore
    model = LinearSVC()
    with open(f'{os.path.dirname(__file__)}/model_parameters.json', 'r') \
            as modfile:
        params = json.load(modfile)
    model.coef_ = np.array(params['coef'])
    model.intercept_ = np.array(params['intercept'])
    model.classes_ = np.array(params['classes'])
    y_pred: ArrayType = model.predict(x_test)
    # pylint: disable=protected-access
    probs = pd.DataFrame(
        model._predict_proba_lr(x_test),
        columns=['prob_not', 'prob_vuln']
    )
    preds = pd.DataFrame(y_pred, columns=['prediction'])
    tog: DataFrame = pd.concat([probs, preds], axis=1)
    recom_commmits: DataFrame = tog[tog.prediction == 1]
    output: DataFrame = recom_commmits.join(dataset)[
        ['repo', 'commit', 'prob_vuln']
    ]
    output['repo'] = output.repo.str.split('/').str[-1]
    output['commit'] = output.commit.str[:10]
    errort: float = 5 + 5 * np.random.rand(len(output), )
    output['prob_vuln'] = round(output.prob_vuln * 100 - errort, 1)
    output.to_csv('sorts_results.csv', index=False)
    output = output.sort_values(by='prob_vuln', ascending=False)
    output = output.reset_index(drop=True)
    print('\nActually took', datetime.timedelta(seconds=time.time() - start))
    print('Top recommended commits to look for vulnerabilities:')
    print(output.to_string(index=False,
                           float_format=lambda x: str(x) + '%'))
    print('This table was written to sorts_results.csv')


def predict_file(subscription_path: str) -> None:
    """
    Extracts features from the files of the defined subscription and uses
    the ML model to sort the files according to the likelihood of having
    vulnerabilities
    """
    fusion_path: str = os.path.join(
        os.path.normpath(subscription_path),
        'fusion'
    )
    files_df = get_repo_files_dataframe(fusion_path)
    features_df = fill_model_file_features(files_df)
    input_data = features_df[
        ['midnight_commits', 'num_lines', 'commit_frequency']
    ]
    model: MLPClassifier = load(
        os.path.join(os.path.dirname(__file__), 'neural_network.joblib')
    )
    prediction_df: DataFrame = pd.DataFrame(
        model.predict(input_data),
        columns=['pred']
    )
    probability_df: DataFrame = pd.DataFrame(
        model.predict_proba(input_data),
        columns=['prob_safe', 'prob_vuln']
    )
    output_df: DataFrame = pd.concat(
        [files_df[['file']], probability_df, prediction_df],
        axis=1
    )
    errort: float = 5 + 5 * np.random.rand(len(output_df), )
    output_df['prob_vuln'] = round(output_df.prob_vuln * 100 - errort, 1)
    sorted_files: DataFrame = output_df[output_df.pred == 1]\
        .sort_values(by='prob_vuln', ascending=False)\
        .reset_index(drop=True)[['file', 'prob_vuln']]
    sorted_files.to_csv('sorts_results.csv', index=False)
    print('Results saved in sorts_results.csv')
    print('Top recommended files to look for vulnerabilities:')
    print(sorted_files.to_string(index=False, float_format=lambda x: f'{x}%'))
