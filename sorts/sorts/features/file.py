from category_encoders import (
    BinaryEncoder,
)
from cryptography.fernet import (
    Fernet,
)
from datetime import (
    datetime,
)
from functools import (
    partial,
)
import os
import pandas as pd
from pandas import (
    DataFrame,
    Series,
)
import pytz  # type: ignore
from sorts.utils.logs import (
    log,
    log_exception,
)
from sorts.utils.repositories import (
    get_log_file_metrics,
    get_repositories_log,
    GitMetrics,
    parse_git_shortstat,
)
from sorts.utils.static import (
    get_extensions_list,
)
import tempfile
import time
from tqdm import (
    tqdm,
)
from typing import (
    List,
    NamedTuple,
    Set,
)

FILE_FEATURES = [
    "num_commits",
    "num_unique_authors",
    "file_age",
    "midnight_commits",
    "risky_commits",
    "seldom_contributors",
    "num_lines",
    "commit_frequency",
    "busy_file",
    "extension",
]


class FileFeatures(NamedTuple):
    num_commits: int
    num_unique_authors: int
    file_age: int
    midnight_commits: int
    risky_commits: int
    seldom_contributors: int
    num_lines: int
    commit_frequency: float
    busy_file: int
    extension: str


def encode_extensions(training_df: DataFrame) -> None:
    extensions: List[str] = get_extensions_list()
    extensions_df: DataFrame = pd.DataFrame(extensions, columns=["extension"])
    encoder: BinaryEncoder = BinaryEncoder(cols=["extension"], return_df=True)
    encoder.fit(extensions_df)
    encoded_extensions = encoder.transform(training_df[["extension"]])
    training_df[
        encoded_extensions.columns.tolist()
    ] = encoded_extensions.values.tolist()


def get_features(  # pylint: disable=too-many-locals
    row: Series, logs_dir: str
) -> FileFeatures:
    # Use -1 as default value to avoid ZeroDivisionError
    file_age: int = -1
    midnight_commits: int = -1
    num_commits: int = -1
    num_lines: int = -1
    risky_commits: int = -1
    seldom_contributors: int = -1
    unique_authors: List[str] = []
    extension: str = ""
    try:
        repo_path: str = row["repo"]
        repo_name: str = os.path.basename(repo_path)
        file_relative: str = row["file"].replace(f"{repo_name}/", "", 1)
        git_metrics: GitMetrics = get_log_file_metrics(
            logs_dir, repo_name, file_relative
        )
        file_age = get_file_age(git_metrics)
        midnight_commits = get_midnight_commits(git_metrics)
        num_commits = get_num_commits(git_metrics)
        num_lines = get_num_lines(os.path.join(repo_path, file_relative))
        risky_commits = get_risky_commits(git_metrics)
        seldom_contributors = get_seldom_contributors(git_metrics)
        unique_authors = get_unique_authors(git_metrics)
        extension = file_relative.split(".")[-1].lower()
    except FileNotFoundError as exc:
        log_exception(
            "warning",
            exc,
            message=f"Log file for repo {repo_name} does not exist",
        )
    except IndexError as exc:
        log_exception(
            "warning",
            exc,
            message=(
                f"File {os.path.join(repo_name, file_relative)} "
                "has no git history"
            ),
        )
    return FileFeatures(
        num_commits=num_commits,
        num_unique_authors=len(unique_authors),
        file_age=file_age,
        midnight_commits=midnight_commits,
        risky_commits=risky_commits,
        seldom_contributors=seldom_contributors,
        num_lines=num_lines,
        commit_frequency=(
            round(num_commits / file_age, 4) if file_age else num_commits
        ),
        busy_file=1 if len(unique_authors) > 9 else 0,
        extension=extension,
    )


def get_file_age(git_metrics: GitMetrics) -> int:
    """Gets the number of days since the file was created"""
    today: datetime = datetime.now(pytz.utc)
    commit_date_history: List[str] = git_metrics["date_iso_format"]
    file_creation_date: str = commit_date_history[-1]
    return (today - datetime.fromisoformat(file_creation_date)).days


def get_num_commits(git_metrics: GitMetrics) -> int:
    """Gets the number of commits that have modified a file"""
    commit_history: List[str] = git_metrics["commit_hash"]
    return len(commit_history)


def get_num_lines(file_path: str) -> int:
    """Gets the numberr of lines that a file has"""
    result: int = 0
    try:
        file = open(file_path, "rb")
        bufgen = iter(partial(file.raw.read, 1024 * 1024), b"")  # type: ignore
        result = sum(buf.count(b"\n") for buf in bufgen)
    except FileNotFoundError:
        log("warning", "File %s not found", file_path)
    return result


def get_midnight_commits(git_metrics: GitMetrics) -> int:
    """Gets the number of times a file was modified between 0 AM -6 AM"""
    commit_date_history: List[str] = git_metrics["date_iso_format"]
    commit_hour_history: List[int] = [
        datetime.fromisoformat(date).hour for date in commit_date_history
    ]
    return sum([1 for hour in commit_hour_history if 0 <= hour < 6])


def get_risky_commits(git_metrics: GitMetrics) -> int:
    """Gets the number of commits which had more than 200 deltas"""
    risky_commits: int = 0
    commit_stat_history: List[str] = git_metrics["stats"]
    for stat in commit_stat_history:
        insertions, deletions = parse_git_shortstat(stat.replace("--", ", "))
        if insertions + deletions > 200:
            risky_commits += 1
    return risky_commits


def get_seldom_contributors(git_metrics: GitMetrics) -> int:
    """Gets the number of authors that contributed below the average"""
    seldom_contributors: int = 0
    authors_history: List[str] = git_metrics["author_email"]
    unique_authors: Set[str] = set(authors_history)
    avg_commit_per_author: float = round(
        len(authors_history) / len(unique_authors), 4
    )
    for author in unique_authors:
        commits: int = authors_history.count(author)
        if commits < avg_commit_per_author:
            seldom_contributors += 1
    return seldom_contributors


def get_unique_authors(git_metrics: GitMetrics) -> List[str]:
    """Gets the list of unique authors that modified a file"""
    authors_history: List[str] = list(set(git_metrics["author_email"]))
    authors_history_names: List[str] = [
        author.split("@")[0] for author in authors_history
    ]
    for index, author_name in enumerate(authors_history_names):
        if authors_history_names.count(author_name) > 1:
            del authors_history[index]
            del authors_history_names[index]

    return authors_history


def encrypt_column_values(value: str) -> str:
    fernet = Fernet(Fernet.generate_key())

    return fernet.encrypt(value.encode()).decode()


def extract_features(training_df: DataFrame) -> bool:
    """Extract features from the file Git history and add them to the DF"""
    success: bool = True
    try:
        timer: float = time.time()
        with tempfile.TemporaryDirectory() as tmp_dir:
            get_repositories_log(tmp_dir, training_df["repo"].unique())
            tqdm.pandas()
            training_df[FILE_FEATURES] = training_df.progress_apply(
                get_features, args=(tmp_dir,), axis=1, result_type="expand"
            )
            training_df.drop(
                training_df[training_df["file_age"] == -1].index, inplace=True
            )
            training_df.reset_index(inplace=True, drop=True)
            encode_extensions(training_df)

            training_df["file"] = training_df["file"].apply(
                encrypt_column_values
            )
            training_df["repo"] = training_df["repo"].apply(
                encrypt_column_values
            )

            log(
                "info",
                "Features extracted after %.2f seconds",
                time.time() - timer,
            )
    except KeyError as exc:
        log_exception(
            "error",
            exc,
            message=(
                "DataFrame does not have one of the required keys "
                "'file'/'repo'"
            ),
        )
        success = False
    return success
