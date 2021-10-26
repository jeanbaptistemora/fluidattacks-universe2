from binaryornot.check import (
    is_binary,
)
import csv
from git import (
    Repo,
)
from git.exc import (
    InvalidGitRepositoryError,
)
import glob
from multiprocessing import (
    cpu_count,
)
from multiprocessing.pool import (
    ThreadPool,
)
import os
import sys
from toolbox.resources import (
    fluidcounts,
)
from typing import (
    Iterator,
    Tuple,
)


def command(cmd: str) -> None:
    """Execute a command"""
    if os.system(cmd):
        raise Exception(f"CRITICAL: `{cmd}` return a non-zero status code.")


def get_files_in_head(repo_path: str) -> Iterator[str]:
    """Get all files in the head in the repo."""
    repo = None
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print(f"Skiping {repo_path} Invalid git repository")
        return False
    trees = repo.head.commit.tree.traverse()
    filepaths = fluidcounts(repo_path)
    for tree in trees:
        path = f"{repo_path[7:]}/{tree.path}"
        if (
            tree.type == "blob"
            and os.path.exists(os.path.join("fusion", path))
            and not os.path.islink(os.path.join("fusion", path))
            and path not in filepaths
        ):
            yield path
    print(f"Finished getting the paths {repo_path}")

    return True


def get_last_hash(repo: Repo, file_path: str) -> str:
    """Get last hash of a file in the repo."""
    return repo.git.log(
        "--max-count", "1", "--format=%H", "--", f"{file_path}"
    )


def get_last_date(repo: Repo, file_path: str) -> str:
    """Get last modified date of a file in the repo."""
    return repo.git.log("--max-count", "1", "--format=%cI", "--", file_path)[
        0:10
    ]


def get_lines_count(file_path: str) -> int:
    """Get the number of lines in a file if is non binary."""
    if not is_binary(file_path):
        with open(file_path, encoding="latin-1") as content:
            num_lines = len(content.readlines())
        return num_lines
    return 0


def do_apply_config(file_path: str) -> None:
    """apply config in the git repository"""
    current_path = os.getcwd()
    os.chdir(file_path)
    command("git config core.quotepath off")
    os.chdir(current_path)


def parse_path(path: str) -> Tuple[str, str]:
    """Get the repo path and the file path"""
    path_to_list = path.split("/")
    file_path = ""
    for i in range(1, len(path_to_list)):
        file_path += path_to_list[i] + "/"
    return "fusion/" + path.split("/")[0], file_path[:-1]


def do_print_line(path: str) -> None:
    """Print a line on a csv"""
    repo_path, file_path = parse_path(path)
    repo: str = Repo(repo_path)
    file_lines = get_lines_count(f"{repo_path}/{file_path}")
    file_last_date = get_last_date(repo, file_path)
    file_last_hash = get_last_hash(repo, file_path)
    # have at least 1 loc
    # filename,loc,tested-lines,modified-date,modified-commit,tested-date,
    # comments
    row = [
        f"{repo_path[7:]}/{file_path}",
        file_lines,
        0,
        file_last_date,
        file_last_hash,
        "2000-01-01",
        "",
    ]
    with open("toe/snapshot", "a", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(row)


def do_gen_stats() -> None:
    """print all files in the fusion repositories"""
    repos = glob.glob("fusion/*")
    # Touch the file if it does not exist
    for repo_path in repos:
        if not os.path.isdir(repo_path):
            sys.exit(f"{repo_path} Not dir")
        do_apply_config(repo_path)
        with ThreadPool(processes=cpu_count()) as worker:
            worker.map(do_print_line, get_files_in_head(repo_path))
