import os
import shutil
from toolbox.utils.file import (
    _iter_full_paths,
)


def test_iter_full_paths() -> None:
    os.makedirs("test_iter_full_paths", exist_ok=True)
    expected = [
        "test_iter_full_paths/test_0/",
        "test_iter_full_paths/test_1/",
        "test_iter_full_paths/test_2/",
        "test_iter_full_paths/test_3/",
    ]
    for num in range(4):
        os.makedirs(f"test_iter_full_paths/test_{num}", exist_ok=True)

    result = list(sorted(_iter_full_paths("test_iter_full_paths")))

    assert result == expected

    shutil.rmtree("test_iter_full_paths")
