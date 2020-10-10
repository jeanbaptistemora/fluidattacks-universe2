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
from features.file import (
    FILE_FEATURES,
    extract_features,
)


DATA_PATH: str = f'{os.path.dirname(__file__)}/data'


def test_bad_dataframe(caplog: LogCaptureFixture,test_clone_repo: str) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    extract_features(training_df)
    assert 'Exception: KeyError' in caplog.text


def test_extract_features(test_clone_repo: str) -> None:
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
    extract_features(training_df)
    file_ages: List[int] = [
        (datetime.now(pytz.utc) - datetime.fromisoformat(date)).days
        for date in creation_dates
    ]
    assert training_df[FILE_FEATURES].values.tolist() == [
        [
            1,
            round(137/file_ages[0], 4),
            file_ages[0],
            25,
            137,
            55,
            0,
            49
        ],
        [
            1,
            round(116/file_ages[1], 4),
            file_ages[1],
            12,
            116,
            49,
            0,
            38
        ],
        [
            1,
            round(46/file_ages[2], 4),
            file_ages[2],
            7,
            46,
            21,
            0,
            16
        ],
        [
            1,
            round(323/file_ages[3], 4),
            file_ages[3],
            46,
            323,
            105,
            0,
            98
        ],
        [
            1,
            round(251/file_ages[4], 4),
            file_ages[4],
            44,
            251,
            95,
            0,
            77
        ]
    ]
