# Standard libraries
import os
from datetime import datetime

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
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    training_df['repo'] = training_df['file'].apply(
        lambda x: f'{test_clone_repo}/requests'
    )
    extract_features(training_df)
    assert training_df[FILE_FEATURES].values.tolist() == [
        [
            (
                datetime.now(pytz.utc) -
                datetime.fromisoformat('2011-05-14T14:21:42-04:00')
            ).days,
            137,
            55,
            25
        ],
        [
            (
                datetime.now(pytz.utc) -
                datetime.fromisoformat('2011-10-23T10:56:04-04:00')
            ).days,
            116,
            49,
            12
        ],
        [
            (
                datetime.now(pytz.utc) -
                datetime.fromisoformat('2011-05-20T18:20:17+02:00')
            ).days,
            46,
            21,
            7
        ],
        [
            (
                datetime.now(pytz.utc) -
                datetime.fromisoformat('2011-08-15T16:01:26-04:00')
            ).days,
            323,
            105,
            46
        ],
        [
            (
                datetime.now(pytz.utc) -
                datetime.fromisoformat('2011-08-17T01:23:49-04:00')
            ).days,
            251,
            95,
            44
        ]
    ]
