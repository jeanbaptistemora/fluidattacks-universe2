# Standard libraries
import os

# Third-party libraries
import pandas as pd
from pandas import DataFrame
from _pytest.logging import LogCaptureFixture

# Local libraries
from features.file import extract_features


DATA_PATH: str = f'{os.path.dirname(__file__)}/data'


def test_bad_dataframe(caplog: LogCaptureFixture,test_clone_repo: str) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    extract_features(training_df)
    assert 'Exception: KeyError' in caplog.text
    assert "'feature': 'num_commits'" in caplog.text


def test_extract_features(test_clone_repo: str) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, 'test_repo_files.csv')
    )
    training_df['repo'] = training_df['file'].apply(
        lambda x: f'{test_clone_repo}/requests'
    )
    extract_features(training_df)
    assert training_df[['num_commits']].values.tolist() == [
        [137],
        [116],
        [46],
        [323],
        [251]
    ]
