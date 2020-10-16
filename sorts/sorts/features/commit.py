# Standard libraries
import os
import time
from typing import (
    List,
    NamedTuple,
)

# Third-party libraries
from pandas import (
    DataFrame,
    Series,
)

# Local libraries
from utils.logs import (
    log,
    log_exception,
)
from utils.repositories import get_commit_hunks


COMMIT_FEATURES: List[str] = [
    'hunks'
]


class CommitFeatures(NamedTuple):
    hunks: int


def get_features(row: Series, fusion_path: str) -> CommitFeatures:
    hunks: int = 0
    try:
        repo: str = row['repo']
        commit: str = row['commit']
        repo_path: str = os.path.join(fusion_path, repo)
        hunks = get_commit_hunks(repo_path, commit)
    except KeyError as exc:
        log_exception('info', exc, row=row)
    return CommitFeatures(
        hunks=hunks
    )


def extract_features(training_df: DataFrame, fusion_path: str) -> bool:
    """Extract features from the commit Git stats and add them to the DF"""
    success: bool = True
    try:
        timer: float = time.time()
        training_df[COMMIT_FEATURES] = training_df.apply(
            get_features,
            args=(fusion_path,),
            axis=1,
            result_type='expand'
        )
        log(
            'info',
            'Features extracted after %.2f seconds',
            time.time() - timer
        )
    except KeyError:
        success = False
    return success
