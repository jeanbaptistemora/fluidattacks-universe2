"""Extract features from a project's latest commits,
use included model to get predictions and print and save output.
"""

import datetime
import json
import os
import sys
import time

import git
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC

from toolbox.sorts.utils import df_get_deltas, df_get_files, df_get_hunks


def make_repo_dataset(repo):
    dataset_skel = []
    gitrepo = git.Git(repo)
    hashes_log = gitrepo.log('--pretty=%H,%aI', '--since="10 weeks ago"')
    dataset = None
    if len(hashes_log) > 0:
        hashes_list = hashes_log.split('\n')
        dataset_skel = [x.split(',') for x in hashes_list]
        dataset = pd.DataFrame(dataset_skel, columns=['commit', 'hour'])
        dataset.hour = dataset.hour.str.split('T').str[1].str.split(':').str[0]
        dataset['repo'] = repo
        dataset['subscription'] = 'waggo'
        dataset = dataset.head(10)
    return dataset


def make_base_dataset(subs):
    subs_dir = f'groups/{subs}/fusion'
    repos = os.listdir(subs_dir)
    print(f'This might take around {datetime.timedelta(seconds=len(repos))}')
    dataset = pd.DataFrame()
    for repo in repos:
        repo_path = f'{subs_dir}/{repo}'
        curr_dataset = make_repo_dataset(repo_path)
        if curr_dataset is not None:
            dataset = pd.concat([dataset, curr_dataset])
        else:
            sys.stdout.write(f'\rempty log or problem with repo {repo}')
    dataset = dataset.reset_index(drop=True)
    return dataset


def make_full_dataset(subs):
    dataset = make_base_dataset(subs)
    dataset['hunks'] = dataset.apply(df_get_hunks, axis=1)
    dataset[['additions', 'deletions', 'deltas', 'touched']] = dataset.apply(
        df_get_deltas, axis=1, result_type='expand'
    )
    files_df = dataset.apply(df_get_files, axis=1)
    dataset['touched_files'] = files_df.apply(len)
    dataset['max_other_touchers'] = files_df.apply(
        lambda x: max(x) if x.size else 0
    )
    dataset['touches_busy_file'] = dataset.max_other_touchers.apply(
        lambda x: 1 if x > 9 else 0
    )
    dataset['authored_hour'] = dataset['hour']
    return dataset


def predict(subs):
    start = time.time()
    dataset = make_full_dataset(subs)
    dataset = dataset.dropna()
    x_test = dataset.loc[:, 'hunks':]
    model = LinearSVC()
    with open('toolbox/toolbox/sorts/model_parameters.json', 'r') as modfile:
        params = json.load(modfile)
    model.coef_ = np.array(params['coef'])
    model.intercept_ = np.array(params['intercept'])
    model.classes_ = np.array(params['classes'])
    y_pred = model.predict(x_test)
    # pylint: disable=protected-access
    probs = pd.DataFrame(model._predict_proba_lr(x_test),
                         columns=['prob_not', 'prob_vuln'])
    preds = pd.DataFrame(y_pred, columns=['prediction'])
    tog = pd.concat([probs, preds], axis=1)
    recom_commmits = tog[tog.prediction == 1]
    output = recom_commmits.join(dataset)[['repo', 'commit', 'prob_vuln']]
    output['repo'] = output.repo.str.split('/').str[-1]
    output['commit'] = output.commit.str[:10]
    errort = 5 + 5 * np.random.rand(len(output), )
    output['prob_vuln'] = round(output.prob_vuln * 100 - errort, 1)
    output.to_csv('sorts_results.csv', index=False)
    output = output.sort_values(by='prob_vuln', ascending=False)
    output = output.reset_index(drop=True)
    end = time.time()
    sec = end - start
    print('\nActually took', datetime.timedelta(seconds=sec))
    print('Top recommended commits to look for vulnerabilities:')
    print(output.to_string(index=False,
                           float_format=lambda x: str(x) + '%'))
    print('This table was written to sorts_results.csv')
