# Standard libraries
import os
from datetime import datetime
from typing import List

# Third-party libraries
import pandas as pd
import pytz
from pandas import DataFrame
from _pytest.logging import LogCaptureFixture

# Local libraries
from features.commit import (
    COMMIT_FEATURES,
    extract_features as extract_commit_features,
)
from features.file import (
    FILE_FEATURES,
    extract_features as extract_file_features,
)


DATA_PATH: str = f'{os.path.dirname(__file__)}/data'


def test_bad_dataframe(caplog: LogCaptureFixture,test_clone_repo: str) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    extract_file_features(training_df)
    assert 'Exception: KeyError' in caplog.text


def test_extract_commit_features(test_clone_repo: str) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_commits.csv')
    )
    training_df['repo'] = f'requests'
    extract_commit_features(training_df, test_clone_repo)
    assert training_df[COMMIT_FEATURES].values.tolist() == [
        [
            3,
            5,
            4,
            1,
            9
        ],
        [
            1,
            5,
            2,
            3,
            7
        ],
        [
            4,
            12,
            3,
            9,
            15
        ],
        [
            4,
            3,
            4,
            -1,
            7
        ],
        [
            19,
            63,
            14,
            49,
            77
        ]
    ]


def test_extract_file_features(test_clone_repo: str) -> None:
    creation_dates: List[str] = [
        '2011-05-14T14:21:42-04:00',
        '2011-10-23T10:56:04-04:00',
        '2011-05-20T18:20:17+02:00',
        '2011-08-15T16:01:26-04:00',
        '2011-08-17T01:23:49-04:00'
    ]
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    training_df['repo'] = training_df['file'].apply(
        lambda x: f'{test_clone_repo}/requests'
    )
    extract_file_features(training_df)
    file_ages: List[int] = [
        (datetime.now(pytz.utc) - datetime.fromisoformat(date)).days
        for date in creation_dates
    ]
    assert training_df[FILE_FEATURES].values.tolist() == [
        [
            137,
            55,
            file_ages[0],
            25,
            0,
            49,
            161,
            round(137/file_ages[0], 4),
            1,
        ],
        [
            116,
            49,
            file_ages[1],
            12,
            0,
            38,
            305,
            round(116/file_ages[1], 4),
            1,
        ],
        [
            46,
            21,
            file_ages[2],
            7,
            0,
            16,
            123,
            round(46/file_ages[2], 4),
            1,
        ],
        [
            323,
            105,
            file_ages[3],
            46,
            0,
            98,
            769,
            round(323/file_ages[3], 4),
            1,
        ],
        [
            251,
            95,
            file_ages[4],
            44,
            0,
            77,
            982,
            round(251/file_ages[4], 4),
            1
        ]
    ]
