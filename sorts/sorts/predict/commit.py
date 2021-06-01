import git
from git.cmd import (
    Git,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
)
from sorts.features.commit import (
    COMMIT_FEATURES,
    extract_features,
)
from sorts.utils.logs import (
    log,
)
from sorts.utils.predict import (
    display_results,
    predict_vuln_prob,
)
from sorts.utils.repositories import (
    get_latest_commits,
)
from typing import (
    Dict,
    List,
)


def get_subscription_commits_df(fusion_path: str) -> DataFrame:
    """Returns a DataFrame with commits to prioritize"""
    repo_commits: Dict[str, List[str]] = {}
    for repo in os.listdir(fusion_path):
        repo_path: str = os.path.join(fusion_path, repo)
        git_repo: Git = git.Git(repo_path)
        commit_list: List[str] = get_latest_commits(git_repo, "10 weeks ago")
        repo_commits.update({repo: commit_list})
    predict_df: DataFrame = pd.concat(
        [
            pd.DataFrame({"repo": repo, "commit": commits})
            for repo, commits in repo_commits.items()
        ]
    )
    predict_df.reset_index(drop=True, inplace=True)
    return predict_df


def prioritize(subscription_path: str) -> bool:
    """Prioritizes commits due to the chance of finding a vulnerability"""
    scope: str = "commit"
    success: bool = False
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, "fusion")
    if os.path.exists(fusion_path):
        predict_df: DataFrame = get_subscription_commits_df(fusion_path)
        success = extract_features(predict_df, fusion_path)
        if success:
            csv_name: str = f"{group}_sorts_results_{scope}.csv"
            predict_vuln_prob(predict_df, COMMIT_FEATURES, csv_name, scope)
            display_results(csv_name)
    else:
        log(
            "error",
            "There is no 'fusion' folder in the path %s",
            subscription_path,
        )
    return success
