from _pytest.logging import (
    LogCaptureFixture,
)
from datetime import (
    datetime,
)
from features.file import (
    encode_extensions,
    extract_features as extract_file_features,
    FILE_FEATURES,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
)
import pytest
import pytz
from typing import (
    List,
)

DATA_PATH: str = f"{os.path.dirname(__file__)}/data"


@pytest.mark.usefixtures("test_clone_repo")
def test_bad_dataframe(caplog: LogCaptureFixture) -> None:
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, "test_repo_files.csv")
    )
    extract_file_features(training_df)
    assert "Exception: KeyError" in caplog.text


def test_extract_file_features(test_clone_repo: str) -> None:
    creation_dates: List[str] = [
        "2011-05-14T14:21:42-04:00",
        "2011-10-23T10:56:04-04:00",
        "2011-05-20T18:20:17+02:00",
        "2011-08-15T16:01:26-04:00",
        "2011-08-17T01:23:49-04:00",
    ]
    training_df: DataFrame = pd.read_csv(
        os.path.join(DATA_PATH, "test_repo_files.csv")
    )
    training_df["repo"] = training_df["file"].apply(
        lambda x: f"{test_clone_repo}/requests"
    )
    extract_file_features(training_df)
    file_ages: List[int] = [
        (datetime.now(pytz.utc) - datetime.fromisoformat(date)).days
        for date in creation_dates
    ]
    assert training_df[FILE_FEATURES].values.tolist() == [
        [
            137,
            53,
            file_ages[0],
            25,
            0,
            49,
            161,
            round(137 / file_ages[0], 4),
            1,
            "py",
        ],
        [
            116,
            48,
            file_ages[1],
            12,
            0,
            38,
            305,
            round(116 / file_ages[1], 4),
            1,
            "py",
        ],
        [
            46,
            19,
            file_ages[2],
            7,
            0,
            16,
            123,
            round(46 / file_ages[2], 4),
            1,
            "py",
        ],
        [
            323,
            102,
            file_ages[3],
            46,
            0,
            98,
            769,
            round(323 / file_ages[3], 4),
            1,
            "py",
        ],
        [
            251,
            90,
            file_ages[4],
            44,
            0,
            77,
            982,
            round(251 / file_ages[4], 4),
            1,
            "py",
        ],
    ]


def test_encode_extensions() -> None:
    training_df: DataFrame = pd.DataFrame(
        ["py", "java", "md", "cs", "go"], columns=["extension"]
    )
    encode_extensions(training_df)
    assert training_df.loc[0].values.tolist() == [
        "py",
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
    ]
    assert training_df.loc[1].values.tolist() == [
        "java",
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
    ]
    assert training_df.loc[2].values.tolist() == [
        "md",
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
    ]
    assert training_df.loc[3].values.tolist() == [
        "cs",
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ]
    assert training_df.loc[4].values.tolist() == [
        "go",
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
    ]
